from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt,json
from .models import User,Role
from .serializer import RegisterSerializer
from passlib.hash import pbkdf2_sha256
import datetime
import requests
from Flexpack import settings

def get_google_access_token(auth_code):
    url = 'https://oauth2.googleapis.com/token'
    payload={}
    payload['code'] = auth_code
    payload['redirect_uri'] = settings.REDIRECT_URL
    payload['client_id'] = settings.GOOGLE_CLIENT_ID
    payload['client_secret'] = settings.GOOGLE_CLIENT_SECRET
    payload['scope']=''
    payload['grant_type']='authorization_code'
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data = payload,headers = headers)
    oauth_details = json.loads(response.text)
    return oauth_details

def fetch_user_details_google(access_token):
    user_url = "https://www.googleapis.com/userinfo/v2/me"
    headers = {"Authorization": "Bearer "+access_token }
    response = requests.get(user_url,headers=headers)
    response = json.loads(response.text)
    return response

def get_access_token_for_first_time(payload):
    payload["exp"]= datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
    oauth_details={}
    oauth_details['access_token']= jwt.encode(payload, "SECRET_KEY",algorithm="HS256")
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    oauth_details['refersh_token'] = jwt.encode(payload, "SECRET_KEY",algorithm="HS256")
    return oauth_details

def get_access_token_from_refersh_token(refersh_token):
    payload  = jwt.decode(refersh_token,"SECRET_KEY",algorithm="HS256")
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
    access_token = jwt.encode(payload,"SECRET_KEY",algorithm="HS256")
    return access_token

def check_expiry(token):
    payload  = jwt.decode(token,"SECRET_KEY",algorithm="HS256")
    if(payload['exp'] < datetime.datetime.utcnow()):
        return True
    else:
        return False

def refersh_google_access_token(refersh_token):
    url = 'https://oauth2.googleapis.com/token'
    payload={}
    payload['client_id'] = settings.GOOGLE_CLIENT_ID
    payload['client_secret'] = settings.GOOGLE_CLIENT_SECRET
    payload['grant_type']='refresh_token'
    payload['refresh_token'] = refersh_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data = payload,headers = headers)
    oauth_details = json.loads(response.text)
    return oauth_details


def Login(request):
    return render(request,'jwt_auth_login_register/index.html')

def Signup(request):
    return render(request,'jwt_auth_login_register/register.html')

def home(request):
    return render(request,'jwt_auth_login_register/home.html')

def google_authentication(request):
    auth_code = request.GET.get('code')
    oauth_details = get_google_access_token(auth_code)
    response = fetch_user_details_google(oauth_details['access_token'])
    try:
        user={}
        user['first_name'] = response['given_name']
        user['last_name'] = response['family_name']
        user['email'] = response['email']
        user['provider'] = 'google'
        user['role'] = Role.objects.get(name = "End user").id
        user['password']=""
        user['username']=response['email'].split('@')[0]
        serializer = RegisterSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except Exception as e:
        print(e)
    return redirect('/app/home/')
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
            oauth_details = get_access_token_for_first_time(payload)
            return Response(
              oauth_details,
              status=200,
              content_type="application/json"
            )

        else:
            return Response(
              json.dumps({'Error': "Invalid credentials"}),
              status=400,
              content_type="application/json"
            )

