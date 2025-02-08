from enum import Enum
from typing import List
import streamlit as st
import asyncio


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


class Nodes(Enum):
    NONE = "None"
    TRIGGER = "trigger"
    INPUT = "input"
    REASON = "reason"
    SUMMARY = "summary"
    TRANSLATE = "translate"
    CODE_INTERPRETER = "code_interpreter"

    @classmethod
    def get_values(cls) -> List[str]:
        """Returns a list of trigger type values for dropdown display"""
        ret_val = []
        for node in cls:
            if node.value != "None":
                ret_val.append(node.value)
        return ret_val

    def __str__(self):
        return self.value


@singleton
class Pipeline:
    """
    Class build up a pipeline object. Were we can add a node and each node should have their own little gui to
    configure. We can add objects, and also take the pipeline object and render a python script that can execute the pipeline.
    """
    def __init__(self):
        self.pipeline = []

    @staticmethod
    def new_object(node_id):
        """
        # Display dropdown of objects to select
        :return: streamlit selectbox
        """
        new_node_obj = st.selectbox(
            "Select Operation",
            Nodes.get_values(),
            format_func=str,
            key=node_id,
            index=None,
            )
        return new_node_obj

    def to_python(self):
        """ Creates a python script from the pipeline object that can be executed independently.
        Loops through the pipeline array and looks at all nodes in the pipeline"""
        code = f"""
        import streamlit as st
        from dotenv import load_dotenv
        
        from filip_opper_playground.input import InputType, Input, display_download_pdf, display_uploaded_pdf
        from filip_opper_playground.trigger import Trigger, TriggerType
        from filip_opper_playground.translate import TranslateModel, Translate
        from filip_opper_playground.reason import ReasonModel, Reason
        from filip_opper_playground.summary import Summary, SummaryModel
        from filip_opper_playground.pipieline import Pipeline
        
        # TODO 
        """
        return code

    def render(self):
        """ Loops through all nodes in the pipeline and renders a streamlit graph with all elements in the pipeline array. """
        ret_string = ""
        for node in self.pipeline:
            ret_string += node.name + "  =>  "
        return ret_string

    def add_node(self, node):
        self.pipeline.append(node)

    def execute(self):
        output = None
        for node in self.pipeline:
            if output is None:
                if node.as_coroutine:
                    output = asyncio.run(node.call())
                else:
                    output = node.call()
            else:
                if node.as_coroutine:
                    output = asyncio.run(node.call(output))
                else:
                    output = node.call(output)

        # print(f"Pipeline executed: {output}")
        return output
