import datetime
import jwt
from Flexpack import settings
from jwt_auth_login_register.models import User

class Token:
    def get_access_token_for_first_time(self,payload,time_to_live_access_token,time_to_live_refresh_token):
        payload["type"] = "access"
        payload["exp"]= datetime.datetime.utcnow() + datetime.timedelta(seconds=time_to_live_access_token)
        oauth_details={}
        oauth_details['access_token']= jwt.encode(payload, settings.SECRET_KEY,algorithm="HS256")
        payload["type"] = "refersh"
        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=time_to_live_refresh_token)
        oauth_details['refersh_token'] = jwt.encode(payload, settings.SECRET_KEY,algorithm="HS256")
        return oauth_details

    def get_access_token_from_refersh_token(self,refersh_token,time_to_live_access_token):
        payload  = jwt.decode(refersh_token,settings.SECRET_KEY,algorithms="HS256")

        if(not User.objects.filter(email = payload['email']).exists or payload['type']!="refresh"):
            raise Exception("Invalid Refresh Token")

        now = datetime.datetime.now()
        timestamp = datetime.datetime.timestamp(now)
        if(payload['exp'] < timestamp):
            raise Exception("Refresh Token Expired")
        
        payload['type']   = "access"
        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=time_to_live_access_token)
        access_token = jwt.encode(payload,settings.SECRET_KEY,algorithm="HS256")
        return access_token

    def validate_access_token(self,token):
        try:
            payload  = jwt.decode(token,settings.SECRET_KEY,algorithms="HS256")
        except:
            raise Exception("Invalid Access Token")
    
        if(not User.objects.filter(email = payload['email']).exists or payload['type']!="access"):
            raise Exception("Invalid Access Token")

        now = datetime.datetime.now()
        timestamp = datetime.datetime.timestamp(now)

        if(payload['exp'] < timestamp):
            raise Exception("Token Expired")
        
        return True
    
    def get_user_from_token(self,token):
        payload  = jwt.decode(token,settings.SECRET_KEY,algorithms="HS256")
        if(not User.objects.filter(email = payload['email']).exists or payload['type']!="access"):
            raise Exception("Invalid Access Token")
        user = User.objects.get(email = payload['email'])
        return user