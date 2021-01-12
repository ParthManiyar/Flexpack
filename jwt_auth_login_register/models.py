from django.db import models
import uuid

class Role(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class User(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254,unique=True) 
    password = models.CharField( max_length=128,null = True)
    provider = models.CharField(max_length=50,null=True)
    role = models.ForeignKey(Role,on_delete=models.CASCADE, null = True)









    


