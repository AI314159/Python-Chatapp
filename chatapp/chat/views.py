from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Server, Message

def index(request):
    return render(request, "chat/index.html")

@login_required
def add_server(request):
    if request.method == "POST":
        servername = request.POST["server_name"]
        members = request.POST["members"]
        server = Server(title=servername, owner=request.user)
        server.save()

        members = members.split()
        for member in members:
            try:
                user = User.objects.get(username=member)
            except Exception:
                context = {"error_message": f"Could not add user '{member}'"}
                return render(request, 'chat/new_server.html', context)
            server.members.add(user)

        if request.user.username not in members:
            server.members.add(request.user)

        return redirect(f"/server/{server.id}")
    else:
        return render(request, "chat/new_server.html")

@login_required
def chat_page(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if request.user in server.members.all():
        messages = Message.objects.filter(server=server)
        context = {"server_id": server_id, "server": server, "messages": messages}
        return render(request, "chat/chat_page.html", context)
    else:
        raise Http404
