import requests
import os
from bardapi import Bard
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


api_key = os.environ.get("BARD_API_KEY")

bard = Bard(token=api_key)



# Create your views here.

def ask_bard(message):
    response = bard.get_answer(message)
    answer = response["content"]
    return answer


def index(request):
    if request.method == "POST":
        message = request.POST.get("message")
        response = ask_bard(message)
        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot/chatbot.html")