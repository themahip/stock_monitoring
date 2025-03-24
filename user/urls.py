from django.urls import path
from user.views.auth import UserRegisterView, UserLoginView


api_paths=[
    path("api/auth/register", UserRegisterView.as_view(), name="register"),
    path("api/auth/login", UserLoginView.as_view(), name="login" )
]

urlpatterns=api_paths