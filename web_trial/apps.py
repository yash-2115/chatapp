from django.apps import AppConfig
from django.conf import settings

from keras.models import load_model
from tensorflow.keras.models import model_from_json


import nltk, pickle, os, json
from nltk.stem import WordNetLemmatizer


class WebTrialConfig(AppConfig):
    name = 'web_trial'

    # file_name = os.path.dirname(__file__) + 'chatbot_model.h5'
    path = os.path.join(settings.MODELS, "chatbot_model.h5")
    path1 = os.path.join(settings.MODELS, "classes.pkl")
    path2 = os.path.join(settings.MODELS, "dialogue.json")
    path3 = os.path.join(settings.MODELS, "words.pkl")


    lemmatizer = WordNetLemmatizer()

    model = load_model(path)

    intents = json.loads(open(path2).read())
    words = pickle.load(open(path3, 'rb'))
    classes = pickle.load(open(path1, 'rb'))

