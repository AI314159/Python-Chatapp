from django.urls import path, include
from chat import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.index, name="index"),
    path("server/<uuid:server_id>/", views.chat_page, name="chat-page"),
    path("add_server/", views.add_server, name="add-server"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
]