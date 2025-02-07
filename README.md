## Opper: 
Tekniskt test måndag. Kolla APIet. Samt: 
https://gist.github.com/gsandahl/f3c0938801534bcf4b375774ad28af3c
Gör en cool agent med APIet och sätt upp en free tier.

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
