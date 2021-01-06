from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('api/register', views.Register),
    path('login/', views.Login),
    path('signup/', views.Signup),
    path('home/',views.home),

]