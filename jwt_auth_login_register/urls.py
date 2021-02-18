from django.conf.urls import url
from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('login/', views.login),
    path('signup/', views.signup),
    path('boxdesign/',views.boxDesign),
    path('verify/',views.LoginAPI.as_view()),
    path('google/callback/login/',views.googleAuthentication),
    path('validateToken/',views.ValidateTokenAPI.as_view()),
    path('saveddesign/',views.savedDesign),
    path('boxcreate/',csrf_exempt(views.BoxCreateAPI.as_view())),
    path('getboxes/',csrf_exempt(views.GetBoxesAPI.as_view())),
    path('getbox/',views.GetBoxAPI.as_view()),
    path('editbox/',views.EditBoxAPI.as_view()),
    path('deletebox/',views.DeleteBoxAPI.as_view()),
    path('editbox/<str:uuid>/',views.editBox),
    path('register/',views.Register),
    path('getmaterailprice/',views.GetMaterialPrice.as_view()),
]