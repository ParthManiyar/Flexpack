from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .serializer import RegisterSerializer, UserSerializer
from .models import CustomUser
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

#Register API

def Login(request):
    return render(request,'jwt_auth_login_register/index.html')

def Signup(request):
    return render(request,'jwt_auth_login_register/register.html')

#@login_required(login_url="/account/login/")
def home(request):
    return render(request,'jwt_auth_login_register/home.html')

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        data={}
        if serializer.is_valid():
            user = serializer.save()
            data['status'] = 200
            data["user"] =  UserSerializer(user,context=self.get_serializer_context()).data;
            data["message"] = "User Created Successfully.  Now perform Login to get your token";  
        else:
            data = serializer.errors
            data['status']=400
        return Response(data)


Register = RegisterAPI.as_view();

