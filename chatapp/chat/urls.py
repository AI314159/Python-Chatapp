from django.urls import path, include
from chat import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.chat_page, name="homepage"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
]