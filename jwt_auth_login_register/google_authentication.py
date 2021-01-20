import requests
from Flexpack import settings
import json

class Google_Authentication:
    def get_google_access_token(self,auth_code):
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

    def fetch_user_details_google(self,access_token):
        user_url = "https://www.googleapis.com/userinfo/v2/me"
        headers = {"Authorization": "Bearer "+access_token }
        response = requests.get(user_url,headers=headers)
        response = json.loads(response.text)
        return response


    def refersh_google_access_token(self,refersh_token):
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