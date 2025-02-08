from enum import Enum
from typing import List
import streamlit as st
import logging
from opperai import AsyncOpper, trace


class SummaryModel(Enum):
    OPPER_MISTRAL_NEMO = "opper/mistral-nemo-instruct"
    GROQ_DS_R1_70B = "groq/deepseek-r1-distill-llama-70b"
    FIREWORKS_DEEPSEEK_R1 = "fireworks/deepseek-r1"
    GEMINI_1121 = "gcp/gemini-exp-1121"
    GEMINI_1114 = "gcp/gemini-exp-1114"
    DEFAULT = "DEFAULT"

    @classmethod
    def get_values(cls) -> List[str]:
        """Returns a list of trigger type values for dropdown display"""
        return [key.value for key in cls]

    def __str__(self):
        return self.value

    @staticmethod
    def display():
        return st.selectbox(
            "Select Model",
            SummaryModel.get_values(),
            format_func=str
        )

class Summary:
    def __init__(
            self,
            node_id: int,
            model: SummaryModel
    ):
        self.name = "Summary"
        self.as_coroutine = True  # expected to be called with asyncio
        self.node_id = node_id
        self.model = model
        self.prompt = "Summarize the following text:"

    async def call(self, text_input) -> bool:
        """
        :return:
        """
        opper = AsyncOpper()

        model = str(self.model)
        if self.model == SummaryModel.DEFAULT:
            model = None
        res, _ = await opper.call(
            name="Summary",
            instructions=self.prompt,
            input=text_input,
            model=model
        )
        return res


    @staticmethod
    def display():
        st.selectbox(
            "Select model",
            SummaryModel.get_values(),
            format_func=str
        )