from django.test import TestCase
# Create your tests here.
from passlib.hash import pbkdf2_sha256
from random import choice
from jwt_auth_login_register.models import User
from .token import Token

#en = pbkdf2_sha256.hash(None)
#print (en);

def generate_random_username(length=16, chars=ascii_lowercase+digits, split=4, delimiter='-'):
    
    username = ''.join([choice(chars) for i in range(length)])
    
    if split:
        username = delimiter.join([username[start:start+split] for start in range(0, len(username), split)])
    
    try:
        User.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
    except User.DoesNotExist:
        return username;

#print(generate_random_username(chars = "parthmaniyar90"))

#tok  = Token()
#payload={"email":"parthmaniyar90@gmail.com"}
#token = tok.get_access_token_for_first_time(payload,1,1)
#print(token)

