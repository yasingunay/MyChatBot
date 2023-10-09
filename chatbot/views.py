import requests
import os
from bardapi import Bard
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from dotenv import load_dotenv
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import User, Chat, ChatSession
import uuid

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


def generate_new_session_id():
    # Implement a function to generate a new unique session_id
    # You can use a library like uuid to generate a unique session_id
    import uuid

    return str(uuid.uuid4())


def index(request):
    chat_history = []

    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            message = request.POST.get("message")

            # Get or create a chat session for the user
            session, created = ChatSession.objects.get_or_create(
                user=user, session_id=request.session.session_key
            )

            response = ask_bard(message)

            chat = Chat(session=session, message=message, response=response)
            chat.save()

            user_sessions = ChatSession.objects.filter(user=user)
            for session in user_sessions:
                session_chats = Chat.objects.filter(session=session)
                chat_history.extend(
                    session_chats.values()
                )  # Append chat data to the history list

            return JsonResponse(
                {"message": message, "response": response, "chat_history": chat_history}
            )
        else:
            # Retrieve chat history for the current user session
            user_sessions = ChatSession.objects.filter(user=request.user)
            for session in user_sessions:
                first_message = (
                    Chat.objects.filter(session=session).order_by("timestamp").first()
                )
                if first_message:
                    chat_history.append(first_message)
                    chat_history.sort(key=lambda x: x.timestamp, reverse=True)

            return render(
                request, "chatbot/chatbot.html", {"chat_history": chat_history}
            )

    return render(request, "chatbot/chatbot.html", {"chat_history": chat_history})


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "chatbot/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "chatbot/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "chatbot/register.html")


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "chatbot/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def history(request, session_id):
    session = get_object_or_404(ChatSession, pk=session_id)
    chats = Chat.objects.filter(session=session)
    return JsonResponse({"chats": list(chats.values())})
