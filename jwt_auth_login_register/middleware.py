from django.conf import settings
from .token import Token
import re
from django.http import HttpResponse

EXEMPT_URLS = []
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        response = self.get_response(request)
        return response

    def process_view(self,request,view_func,view_args,view_kwargs):
        path = request.path_info.lstrip('/')
        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)
        if(url_is_exempt):
            return None
        try:
            token = Token()
            token.validate_access_token(request.headers['Authorization'])
        except Exception as e:
            return HttpResponse('Unauthorized', status=401)
        return None
        

        