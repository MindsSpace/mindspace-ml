from fastapi import FastAPI
import tensorflow as tf
import pickle
import json
from symspellpy.symspellpy import SymSpell
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.initializers import Orthogonal
import numpy as np

app = FastAPI()

# Load the trained model
model = tf.keras.models.load_model("model/chatbot_engmodel.h5")

# Load the tokenizer and label encoder
with open("util/tokenizer.pickle", "rb") as handle:
    tokenizer = pickle.load(handle)
with open("util/label_encoder.pickle", "rb") as enc_file:
    lbl_encoder = pickle.load(enc_file)
with open("data/engdataset.json", "r") as data_file:
    data1 = json.load(data_file)


# Initialize SymSpell for typo correction
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)


def correct_typo(input_text):
    suggestions = sym_spell.lookup_compound(input_text, max_edit_distance=2)
    # Return the corrected input if any suggestions exist
    if suggestions:
        return suggestions[0].term
    return input_text


@app.post("/")
def chat(input_text: str):
    # Correct typos in user input
    corrected_input = correct_typo(input_text)

    # Process the corrected input
    result = model.predict(
        pad_sequences(
            tokenizer.texts_to_sequences([corrected_input]),
            truncating="post",
            maxlen=18,
        )
    )
    tag = lbl_encoder.inverse_transform([np.argmax(result)])

    for intent in data1["intents"]:
        if intent["tag"] == tag:
            resp = np.random.choice(intent["responses"])
            print("Chatbot: ", resp)
            return {"response": resp}

    return {"response": ""}
