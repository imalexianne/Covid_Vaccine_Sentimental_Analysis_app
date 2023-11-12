import os
import gradio as gr
import numpy as np
import pandas as pd
import pickle
import transformers
from transformers import AutoTokenizer, AutoConfig,AutoModelForSequenceClassification,TFAutoModelForSequenceClassification, pipeline
from scipy.special import softmax
from dotenv import load_dotenv, dotenv_values
# from huggingface_hub import login

from huggingface_hub import login

# notebook_login()
load_dotenv()
login(os.getenv("access_token"))
# Requirements
model_path = "imalexianne/distilbert-base-uncased"

tokenizer = AutoTokenizer.from_pretrained(model_path, revision="main")
config = AutoConfig.from_pretrained(model_path, revision="main")
model = AutoModelForSequenceClassification.from_pretrained(model_path, revision="main")

# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for x in text.split(" "):
        x = "@user" if x.startswith("@") and len(x) > 1 else x
        x = "http" if x.startswith("http") else x
        new_text.append(x)
    return " ".join(new_text)

# ---- Function to process the input and return prediction
def sentiment_analysis(text):
    text = preprocess(text)

    encoded_input = tokenizer(text, return_tensors = "pt") # for PyTorch-based models
    output = model(**encoded_input)
    scores_ = output[0][0].detach().numpy()
    scores_ = softmax(scores_)

    # Format output dict of scores
    labels = ["Negative", "Neutral", "Positive"]
    scores = {l:float(s) for (l,s) in zip(labels, scores_) }

    return scores


# ---- Gradio app interface
app = gr.Interface(fn = sentiment_analysis,
                   inputs = gr.Textbox("Write here"),
                   outputs = "label",
                   title = "Sentiment Analysis of Tweets on COVID-19 Vaccines",
                   description  = "Sentiment Analysis of text based on tweets about COVID-19 Vaccines using a fine-tuned 'distilbert-base-uncased' model",

                   examples = [["Covid vaccination has no positive impact"]]
                   )

app.launch(server_name="0.0.0.0", server_port=7860)