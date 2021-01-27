from django.shortcuts import redirect, render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User,Role
from .serializer import RegisterSerializer
from passlib.hash import pbkdf2_sha256
from .utils import generate_random_username
from .google_authentication import Google_Authentication
from .token import Token

def Login(request):
    return render(request,'jwt_auth_login_register/index.html')

def Signup(request):
    return render(request,'jwt_auth_login_register/register.html')

def home(request):
    return render(request,'jwt_auth_login_register/home.html')

   

def google_authentication(request):
    auth_code = request.GET.get('code')
    google = Google_Authentication()
    oauth_details = google.get_google_access_token(auth_code)
    response = google.fetch_user_details_google(oauth_details['access_token'])
    if(not User.objects.filter(email = response['email']).exists()):
        user={}
        user['first_name'] = response['given_name']
        user['last_name'] = response['family_name']
        user['email'] = response['email']
        user['provider'] = 'google'
        user['role'] = Role.objects.get(name = "End user").id
        user['password']=None
        user['username']=response['email'].split('@')[0]+"_"+generate_random_username()
        serializer = RegisterSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    payload={"email":response['email']}   
    tok  = Token()
    token = tok.get_access_token_for_first_time(payload,3600,7)
    return render(request,'jwt_auth_login_register/callback.html',token)
   
    
class CreateUserAPIView(APIView):
    def post(self, request):
        user = request.data
        user._mutable = True
        user['role'] = Role.objects.get(name = "End user").id
        user['provider']=""
        user._mutable = False
        serializer = RegisterSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        if(user['password'] is None or user['password']==""):
            return Response({'Password':"This Field is required"},status=400)
        serializer.save()
        return Response(serializer.data, status=201)

Register = CreateUserAPIView.as_view();


class LoginAPI(APIView):

    def post(self, request, *args, **kwargs):
        
        if "username" not in request.data  :
            return Response({'Error': "Please provide username"}, status=400)

        if "password" not in request.data  :
            return Response({'Error': "Please provide password"}, status=400)
        
        username = request.data['username']
        password = request.data['password']

        if(username is None or username==""):
            return Response({'Error': "Please provide username"}, status=400)

        if(password is None or password==""):
            return Response({'Error': "Please provide password"}, status=400)
        
        try:
            user = User.objects.get(username=username)
            if(user.password is None):
                return Response({'Error':"Invalid password"},status=400)

            if not pbkdf2_sha256.verify(password,user.password):
                return Response({'Error': "Invalid password"}, status=400)

        except User.DoesNotExist:
            return Response({'Error': "Invalid username"}, status=400)

        if user:
            payload={"email":user.email}
            oauth_details = Token.get_access_token_for_first_time(self,payload,3600,7)
            return Response(
              oauth_details,
              status=200,
              content_type="application/json"
            )

        else:
            return Response(
              {'Error': "Invalid credentials"},
              status=400,
              content_type="application/json"
            )

class ValidateTokenAPI(APIView):
    def post(self, request, *args, **kwargs):
        val  = Token()
        access_token = request.data['access_token']
        response = {}
        status = 200
        content_type="application/json"
        try:
            val.validate_access_token(access_token)
            response['Validation'] = "Success"
        except Exception as e:
            status = 401
            response['Validation '] = "Failed"
            response['message'] = str(e)

        return Response(response,status = status,content_type = content_type)


