"""
    Rule interface
"""
from functools import reduce
from typing import List, Set

import pyspark
from pydantic import BaseModel, Field, field_validator
from pyspark.sql.functions import when

from stickler.action import Action, ActionConfig
from stickler.condition import Condition, ConditionConfig
from stickler.config.consts import (
    ACTIONS,
    CASCADE_GROUP,
    CONDITIONS,
    EXECUTION_TYPE,
    RULE_NAME,
)
from stickler.enums.rule_type_enum import ExecutionType
from stickler.utils.logger import logger


class RuleConfig(BaseModel):
    """
    Rule configuration class.

    Each rule is of the form:
    {
        "RULE_NAME": "rule_name",
        "EXECUTION_TYPE": "cascade"/"accumulative",
        "CASCADE_GROUP": int/[int],
        "CONDITIONS": [
            {
                ConditionConfig (can be empty)
            },
            ...
        ],
        "ACTIONS": [
            {
                ActionConfig
            },
            ...
        ]
    }
    """

    rule_name: str = Field(alias=RULE_NAME)
    execution_type: ExecutionType = Field(
        alias=EXECUTION_TYPE, default=ExecutionType.ACCUMULATIVE
    )
    cascade_group: List[int] = Field(alias=CASCADE_GROUP, default=[0])
    conditions: List[ConditionConfig] = Field(alias=CONDITIONS, default=[])
    actions: List[ActionConfig] = Field(alias=ACTIONS)

    @field_validator(EXECUTION_TYPE, mode="before")
    @classmethod
    def parse_execution_type(cls, value):
        """
        Converts the execution type string to the corresponding ExecutionType enum.

        Args:
            value(str): The execution type as a string.

        Returns:
            ExecutionType: The corresponding ExecutionType enum.

        Raises:
            ValueError: If the string does not match "cascade" or "accumulative".
        """
        if isinstance(value, str):
            value = value.strip().lower()
            if value == "cascade":
                return ExecutionType.CASCADE
            if value == "accumulative":
                return ExecutionType.ACCUMULATIVE
        raise ValueError(
            f"Invalid execution type: {value}. Must be 'cascade' or 'accumulative'."
        )

    @field_validator(ACTIONS)
    @classmethod
    def check_non_empty_actions(cls, value):
        """
        Checks if the list of actions is not empty.

        Args:
            cls(RuleConfig): Rule configuration class.
            value(list[ActionConfig]): List of actions to be checked.

        Raises:
            ValueError: If the list of actions is empty.
        """
        if not value:  # If list is empty
            raise ValueError(f"{ACTIONS} must contain at least one action.")
        return value

    @field_validator(CASCADE_GROUP, mode="before")
    @classmethod
    def ensure_list_cascade_group(cls, value):
        """Ensures that cascade_group is always a list."""
        return [value] if isinstance(value, int) else value


class Rule:
    """
    Rule class.
    Each rule consists of a name, a list of conditions and a list of actions.

    Attributes:
        rule_name(str): Name of the rule.
        execution_type(ExecutionType): Type of the rule (Cascade/Accumulative).
        cascade_group(list[int]): List of groups to which the rule belongs.
        conditions(list[Condition]): List of conditions that must be met to apply the rule.
        actions(list[Action]): List of actions that will be applied if the conditions are met.
    """

    def __init__(
        self,
        rule_config: RuleConfig,
    ):
        """
        Initializes a Rule with conditions and actions.

        Args:
            rule_config(RuleConfig): Rule configuration. It's a dictionary
            with the rule name, a list of conditions and a list of actions.
        """
        self.rule_name = rule_config.rule_name

        self.execution_type = rule_config.execution_type
        self.cascade_group = rule_config.cascade_group

        if rule_config.conditions == []:
            # If no conditions are provided, it means that the rule will be applied to all the data,
            # so we add a default condition that will always be true.
            self.conditions = [Condition(ConditionConfig())]
        else:
            self.conditions = [
                Condition(condition) for condition in rule_config.conditions
            ]

        self.actions = [
            Action(action, self.rule_name, self.execution_type)
            for action in rule_config.actions
        ]

        logger.debug(
            "Rule %s initialized with %d conditions and %d actions.",
            self.rule_name,
            len(self.conditions),
            len(self.actions),
        )

    def evaluate_rule_conditions(self) -> pyspark.sql.column.Column:
        """
        Calls every evaluate method of the conditions and returns the final set of conditions,
        from which the dataframe will be filtered.

        Returns:
            set_conditions(pyspark.sql.column.Column): Final conditions for filtering.
        """
        logger.debug("Evaluating conditions for rule: %s", self.rule_name)

        check_conditions = []

        for condition in self.conditions:
            check_conditions.append(condition.evaluate())

        set_conditions = reduce(lambda x, y: x & y, check_conditions)

        logger.debug("Conditions evaluated for rule: %s", self.rule_name)

        return set_conditions

    def evaluate_cascade_conditions(
        self, applied_rules_in_groups: Set[str]
    ) -> pyspark.sql.column.Column:
        """
        Evaluates cascade conditions for the rule.

        If the rule is of accumulative type, it returns a column with all values set to False.
        Otherwise, it evaluates the cascade conditions based on the applied rules in
        the cascade group.

        Returns:
            pyspark.sql.column.Column: A column representing the cascade conditions.
        """
        if self.execution_type == ExecutionType.ACCUMULATIVE:
            return pyspark.sql.functions.lit(False)

        cascade_blocked = reduce(
            lambda x, y: x | y,
            [
                pyspark.sql.functions.col(rule_name)
                for rule_name in applied_rules_in_groups
            ],
            pyspark.sql.functions.lit(False),
        )
        return cascade_blocked

    def apply(
        self, df: pyspark.sql.DataFrame, applied_rules_in_groups: Set[str]
    ) -> pyspark.sql.DataFrame:
        """
        Applies the rule to the dataframe, calling the execute method of each action.

        Args:
            df(pyspark.sql.DataFrame): data to which the rule will be applied.
            applied_rules_in_groups(Set[str]): Set of rules that have been applied in
            the cascade group.

        Returns:
            resultant_df(pyspark.sql.DataFrame): Resultant dataframe after applying the rule.
            It also adds the history column that determines if the rule was applied or not.
        """
        logger.debug("Applying rule: %s", self.rule_name)
        set_conditions = self.evaluate_rule_conditions()

        cascade_blocked = self.evaluate_cascade_conditions(applied_rules_in_groups)

        resultant_df = df.select("*")
        for action in self.actions:
            resultant_df = action.execute(resultant_df, set_conditions, cascade_blocked)

        logger.debug("Rule %s applied successfully.", self.rule_name)

        return resultant_df.withColumn(
            self.rule_name,
            when(set_conditions & ~cascade_blocked, True).otherwise(False),
        )

    def __str__(self) -> str:
        """
        Example of the string representation of a rule:
        Rule rule_name
        Conditions
        Condition1, Condition2, ...
        Actions
        Action1, Action2, ...

        Returns:
            str: String representation of the rule.
        """
        return (
            f"Rule {self.rule_name}\n"
            f"Conditions\n{', '.join(str(condition) for condition in self.conditions)}\n"
            f"Actions\n{', '.join(str(action) for action in self.actions)}"
        )
