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
enModel = tf.keras.models.load_model("model/chatbot_engmodel.h5")
idModel = tf.keras.models.load_model("model/chatbot_indomodel.h5")

# Load the tokenizer and label encoder
with open("util/en_tokenizer.pickle", "rb") as handle:
    en_tokenizer = pickle.load(handle)
with open("util/en_label_encoder.pickle", "rb") as enc_file:
    en_lbl_encoder = pickle.load(enc_file)
with open("util/id_tokenizer.pickle", "rb") as handle2:
    id_tokenizer = pickle.load(handle2)
with open("util/id_label_encoder.pickle", "rb") as enc_file2:
    id_lbl_encoder = pickle.load(enc_file2)
with open("data/engdataset.json", "r") as data1_file:
    enData = json.load(data1_file)
with open("data/indodataset.json", "r") as data2_file:
    idData = json.load(data2_file)


# Initialize SymSpell for typo correction
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)


def correct_typo(input):
    suggestions = sym_spell.lookup_compound(input, max_edit_distance=2)
    # Return the corrected input if any suggestions exist
    if suggestions:
        return suggestions[0].term
    return input


@app.post("/")
def chat(language: str, input: str):
    # Correct typos in user input
    corrected_input = correct_typo(input)

    if language == "id":
        # Process the corrected input
        result = idModel.predict(
            pad_sequences(
                id_tokenizer.texts_to_sequences([corrected_input]),
                truncating="post",
                maxlen=6,
            )
        )
        tag = id_lbl_encoder.inverse_transform([np.argmax(result)])

        for intent in idData["intents"]:
            if intent["tag"] == tag:
                resp = np.random.choice(intent["responses"])
                print("Chatbot: ", resp)
                return {"response": resp}
    else:
        # Process the corrected input
        result = enModel.predict(
            pad_sequences(
                en_tokenizer.texts_to_sequences([corrected_input]),
                truncating="post",
                maxlen=18,
            )
        )
        tag = en_lbl_encoder.inverse_transform([np.argmax(result)])

        for intent in enData["intents"]:
            if intent["tag"] == tag:
                resp = np.random.choice(intent["responses"])
                print("Chatbot: ", resp)
                return {"response": resp}

    return {"response": ""}
