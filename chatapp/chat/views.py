from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            context = {"error_message": "Incorrect username or password."}
            return render(request, "login.html", context)
    else:
        return render(request, "login.html")

@login_required
def chat_page(request):
    context = {}
    return render(request, "chat/chat_page.html", context)

@login_required
def logout_user(request):
    logout(request)
    return redirect("/")