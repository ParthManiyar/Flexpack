from django.test import TestCase

# Create your tests here.
from passlib.hash import pbkdf2_sha256

en = pbkdf2_sha256.hash(None)
print (en);