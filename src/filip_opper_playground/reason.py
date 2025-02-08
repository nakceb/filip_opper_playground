from enum import Enum
from typing import List
import streamlit as st
import logging
from opperai import AsyncOpper, trace


class ReasonModel(Enum):
    GROQ_DS_R1_70B = "groq/deepseek-r1-distill-llama-70b"
    FIREWORKS_DEEPSEEK_R1 = "fireworks/deepseek-r1"
    DEFAULT = "DEFAULT"

    @classmethod
    def get_values(cls) -> List[str]:
        """Returns a list of trigger type values for dropdown display"""
        return [key.value for key in cls]

    def __str__(self):
        return self.value

    @staticmethod
    def display():
        defalut_value = Reason(0, ReasonModel.DEFAULT).prompt
        prompt = st.text_input(label="Instruction prompt", value=defalut_value)
        model = st.selectbox(
            "Select Model",
            ReasonModel.get_values(),
            format_func=str
        )
        return model, prompt

class Reason:
    def __init__(
            self,
            node_id: int,
            model: ReasonModel
    ):
        self.name = "Reason"
        self.as_coroutine = True  # expected to be called with asyncio
        self.node_id = node_id
        self.model = model
        self.prompt = ""

    @trace
    async def call(self, text_input) -> bool:
        """
        :return:
        """
        opper = AsyncOpper()

        model = str(self.model)
        if self.model == ReasonModel.DEFAULT:
            model = None
        res, _ = await opper.call(
            name="Reason",
            instructions=self.prompt,
            input=text_input,
            model=model
        )
        return res
