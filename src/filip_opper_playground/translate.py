from enum import Enum
from typing import List
import streamlit as st
import logging
from opperai import AsyncOpper, trace


class TranslateModel(Enum):
    GROQ_DS_R1_70B = "groq/deepseek-r1-distill-llama-70b"
    ANTHROPIC_CLAUDE_3_HAIKU = "anthropic/claude-3-haiku"
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
        defalut_value = Translate(0, TranslateModel.DEFAULT).prompt
        prompt = st.text_input(label="Instruction prompt", value=defalut_value)
        model = st.selectbox(
            "Select Model",
            TranslateModel.get_values(),
            format_func=str
        )
        return model, prompt

class Translate:
    def __init__(
            self,
            node_id: int,
            model: TranslateModel
    ):
        self.name = "Translate"
        self.as_coroutine = True  # expected to be called with asyncio
        self.node_id = node_id
        self.model = model
        self.prompt = "Translate this to english:"

    async def call(self, text_input) -> bool:
        """
        :return:
        """
        opper = AsyncOpper()

        model = str(self.model)
        if self.model == TranslateModel.DEFAULT:
            model = None
        res, _ = await opper.call(
            name="Translate",
            instructions=self.prompt,
            input=text_input,
            model=model
        )
        return res
