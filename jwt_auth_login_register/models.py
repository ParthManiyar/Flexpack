from django.db import models
from django.contrib.auth.models import User
import uuid

def get_uuid():
    return str(uuid.uuid4())

class Role(models.Model):

    id = models.CharField(max_length=100,default = "", editable=False, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.uuid
        
    


class CustomUser(User):

    class Meta:
        verbose_name = "CustomUser"
        verbose_name_plural = "CustomUsers"

    
    uuid = models.CharField(max_length=100,default = "", editable=False)
    role = models.ForeignKey(Role,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.pk==None:
            self.uuid = get_uuid()
        super(CustomUser, self).save(*args, **kwargs)





    


