from enum import Enum
from typing import List
import streamlit as st
import logging


class TriggerType(Enum):
    MANUAL = "manual"
    SCHEDULE = "schedule"

    @classmethod
    def get_values(cls) -> List[str]:
        """Returns a list of trigger type values for dropdown display"""
        return [trigger.value for trigger in cls]

    def __str__(self):
        return self.value

    @staticmethod
    def display():
        return st.selectbox(
            "Select Trigger",
            TriggerType.get_values(),
            format_func=str
        )

class Trigger:
    def __init__(
            self,
            node_id: int,
            trigger_type: TriggerType,
    ):
        self.name = "Trigger"
        self.as_coroutine = False
        self.node_id = node_id
        self.trigger_type = trigger_type

    def call(self) -> bool:
        """
        :return:
        """
        if self.trigger_type == TriggerType.MANUAL:
            return True
        else:
            logging.warning("Not implemented! Trigger != Manual")
            return True

    @staticmethod
    def display():
        st.selectbox(
            "Select Trigger",
            TriggerType.get_values(),
            format_func=str
        )