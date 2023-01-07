from django.urls import path
from .view import users_view, auth_view

urlpatterns = [
    path("login", auth_view.LoginView.as_view()),
    path("self", users_view.SelfUserView.as_view()),
    path("users", users_view.UserViewSet.as_view()),
    path("users/<int:pk>", users_view.UserByPkView.as_view()),
    path("logout", auth_view.LogoutView.as_view()),
    path("register", auth_view.RegisterView.as_view())
]
