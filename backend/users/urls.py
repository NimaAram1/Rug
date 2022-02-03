from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('register/', views.RegisterationApiView.as_view(), name="registeration"),
    path('login/', views.LoginApiView.as_view(), name="login"),
    path('logout/', views.LogoutApiView.as_view(), name="logout")
]
