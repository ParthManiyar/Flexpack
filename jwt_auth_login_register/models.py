from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

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
    width = models.PositiveIntegerField(validators = [MaxValueValidator(900),MinValueValidator(400)], default = 500)
    height =  models.PositiveIntegerField(validators = [MaxValueValidator(900),MinValueValidator(400)],default=500)
    depth = models.PositiveIntegerField(validators = [MaxValueValidator(900),MinValueValidator(400)],default=500)
    front_texture = models.JSONField()
    top_texture = models.JSONField()
    bottom_texture = models.JSONField()
    back_texture = models.JSONField()
    right_texture = models.JSONField()
    left_texture = models.JSONField()
    preview_image = models.ImageField(upload_to ='uploads/',default = 'uploads/kraft.jpg')
    material = models.CharField(max_length=50, default = "kraft")
    user = models.ForeignKey(User,on_delete=models.CASCADE,null = True)

    def _get__description(self):
        return 'Shipping Box - %s x %s x %s' % (self.width, self.height,self.depth)
    
    description = property(_get__description)

class BoxPrice(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    material = models.CharField(max_length=50)
    material_price = models.FloatField("Material Price per kg in INR")
    decoration_price = models.FloatField("decoration price per m^2 in INR")

class Purchase(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    box = models.ForeignKey(Box,on_delete=models.CASCADE,null = True)
    quantity = models.PositiveIntegerField(validators = [MaxValueValidator(2000)])
    unit_price = models.DecimalField(decimal_places=2,max_digits=10)

class Order(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.PositiveIntegerField()
    status = models.CharField(max_length=100,default = "Pending")
    date = models.DateTimeField(auto_now_add=True)

    @property
    def total_order(self):
        order = Order.objects.count()
        return order

    @property
    def pending_order(self):
        return Order.objects.filter(status="pending").count()
    
    @property
    def delivered_order(self):
        return Order.objects.filter(status="delivered").count()
    




    











    


