import streamlit as st
from dotenv import load_dotenv

from filip_opper_playground.input import InputType, Input, display_download_pdf, display_uploaded_pdf
from filip_opper_playground.trigger import Trigger, TriggerType
from filip_opper_playground.translate import TranslateModel, Translate
from filip_opper_playground.reason import ReasonModel, Reason
from filip_opper_playground.summary import Summary, SummaryModel
from filip_opper_playground.pipieline import Pipeline

pipeline = Pipeline()
node_id = 0
load_dotenv()

st.header("Opper - Web GUI concept")
st.text("Showcase how to build a pipeline in the web gui and execute it. "
        "Demonstrating with loading in pdf then summarize then translate with Opper API.")

tab1, tab2, tab3 = st.tabs(["Add Nodes", "Modify pipeline", "Run pipeline"])

with tab1:
    # Add node
    node_selected = pipeline.new_object(node_id=node_id)  # type: st.selectbox
    active_node = None

    if node_selected is not None:
        if node_selected == "trigger":
            # Display trigger type dropdown
            trigger_type = TriggerType.display()

            # If schedule is selected, show additional options
            if trigger_type == TriggerType.SCHEDULE.value:
                st.write("ERRROR: schedule not implemented")

            # If schedule is selected, show additional options
            if trigger_type == TriggerType.MANUAL.value:
                active_node = Trigger(node_id, TriggerType.MANUAL)

        if node_selected == "input":
            # Display trigger type dropdown
            input_type = InputType.display()
            text_content = None

            # If schedule is selected, show additional options
            if input_type == InputType.PDF_READER_DOWNLOAD.value:
                text_content = display_download_pdf()
            elif input_type == InputType.PDF_READER_UPLOAD.value:
                text_content = display_uploaded_pdf()

            if text_content is not None:
                active_node = Input(node_id=node_id)
                active_node.text_content = text_content

        if node_selected == "summary":
            # Display trigger type dropdown
            summary_model_type = SummaryModel.display()

            if summary_model_type is not None:
                active_node = Summary(node_id=node_id, model=summary_model_type)

        if node_selected == "translate":
            # Display trigger type dropdown
            model, prompt = TranslateModel.display()
            if model is not None:
                active_node = Translate(node_id=node_id, model=model)
                active_node.prompt = prompt
            if prompt is not None:
                active_node.prompt = prompt

        if node_selected == "reason":
            # Display trigger type dropdown
            model, prompt = ReasonModel.display()
            if model is not None:
                active_node = Reason(node_id=node_id, model=model)
                active_node.prompt = prompt
            if prompt is not None:
                active_node.prompt = prompt


    if st.button("Add node"):
        if active_node:
            pipeline.add_node(active_node)
            node_id += 1

with tab2:
    if st.button("Clear pipeline"):
        pipeline.pipeline = []
        node_id = 0

with tab3:
    if st.button("RUN PIPELINE"):
        st.write(pipeline.execute())

    if st.toggle("Show as python script"):
        code = st.code(pipeline.to_python())

st.write(pipeline.render())
