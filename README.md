# Idea:
Ett frontend som hjälper dig bygga upp ett workflow med opper APIet som backend.

## Install:
``` python
# Create venv / conda env
pip install .

touch scripts/.env

# nano scripts/.env
OPPER_API_KEY=<enter your key>
```

## Run application
``` bash
cd scripts
streamlit run main.py
```

### Add-on ideas
* if input tokens set we can estimate each cost of each model through the pipeline.
* fancy edit pipeline, visual rendering.
* support recursion with exit condition for agent logic.
* support branching pipeline.
* visualize output and state of each section in pipeline when rendering