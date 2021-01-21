from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.Register),
    path('login/', views.Login),
    path('signup/', views.Signup),
    path('home/',views.home),
    path('verify/',views.LoginAPI.as_view()),
    path('google/callback/login/',views.google_authentication),
    path('validateToken/',views.ValidateTokenAPI.as_view())
]