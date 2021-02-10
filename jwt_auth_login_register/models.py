from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator

class Role(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class User(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254,unique=True) 
    password = models.CharField( ('password') ,max_length=128,null = True)
    provider = models.CharField(max_length=50,null=True)
    role = models.ForeignKey(Role,on_delete=models.CASCADE, null = True)
    
    def __str__(self):
        return self.username

class Box(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=50, default = "default")
    width = models.PositiveIntegerField(validators = [MaxValueValidator(1500),MinValueValidator(50)], default = 500)
    height =  models.PositiveIntegerField(validators = [MaxValueValidator(1500),MinValueValidator(50)],default=500)
    depth = models.PositiveIntegerField(validators = [MaxValueValidator(1500),MinValueValidator(50)],default=500)
    front_texture = models.JSONField()
    top_texture = models.JSONField()
    bottom_texture = models.JSONField()
    back_texture = models.JSONField()
    right_texture = models.JSONField()
    left_texture = models.JSONField()
    preview_image = models.ImageField(upload_to ='uploads/',default = 'uploads/kraft.jpg')
    user = models.ForeignKey(User,on_delete=models.CASCADE,null = True)









    


