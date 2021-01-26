from django.shortcuts import render
from rest_framework.decorators import api_view
from django.conf import settings

from .apps import WebTrialConfig

import numpy as np
import nltk
import random


# Create your views here.

from django.views import View
from .models import employee
from .serializers import employeeSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import *



class employeeList(APIView, View,):
    serializer_class = employeeSerializer

    def get(self, request):
        # detail = [{"name": detail.inputs}
        detail = [{"name": employeeList.chatbot_response(detail.inputs)}
        for detail in employee.objects.all()]
        # print(employeeList.chatbot_response('hello'))

        return Response(detail)

    def post(self, request):

        serializer = employeeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


    def clean_up_sentence(sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [WebTrialConfig.lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

    def bow( sentence, words, show_details=True):
        # tokenize the pattern
        sentence_words = employeeList.clean_up_sentence(sentence)
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0]*len(words)
        for s in sentence_words:
            for i,w in enumerate(words):
                if w == s:
                    # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        print ("found in bag: %s" % w)
        return(np.array(bag))

    def predict_class(sentence, model):
        # filter out predictions below a threshold
        p = employeeList.bow(sentence, WebTrialConfig.words,show_details=False)
        res = model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": WebTrialConfig.classes[r[0]], "probability": str(r[1])})
        return return_list

    def getResponse(ints, intents_json):
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if(i['tag']== tag):
                result = random.choice(i['responses'])
                break
        return result

    def chatbot_response(msg):
        ints = employeeList.predict_class(msg, WebTrialConfig.model)
        res = employeeList.getResponse(ints, WebTrialConfig.intents)
        return res