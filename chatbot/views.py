import requests
import os
from bardapi import Bard
from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("BARD_API_KEY")

bard = Bard(token=token)



# Create your views here.
def ask_bard(message):
    """
    Returns the answer obtained from the bard.get_answer method.

    Args:
        message (str): The message to be passed to the bard.get_answer method.

    Returns:
        str: The content of the response obtained from the bard.get_answer method.
    """
    response = bard.get_answer(message)
    answer = response["content"]
    return answer


def index(request):
    if request.method == "POST":
        message = request.POST.get("message")
        response = ask_bard(message)
        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot/chatbot.html")

# def login(request):
#     return render(request, "chatbot/login.html")