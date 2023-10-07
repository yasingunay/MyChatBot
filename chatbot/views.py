from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    if request.method == "POST":
        message = request.POST.get("message")
        print(message)
        response = "Hello, world!"
        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot/chatbot.html")