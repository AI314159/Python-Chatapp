from django.urls import path, include
from chat import views

urlpatterns = [
    path("", views.index, name="index"),
    path("server/<uuid:server_id>/", views.chat_page, name="chat-page"),
    path("add_server/", views.add_server, name="add-server"),
]