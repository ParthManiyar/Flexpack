from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import User,Box, BoxPrice, Purchase, Order
from passlib.hash import pbkdf2_sha256


# Register serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','first_name', 'last_name','email','role','provider','profile_pic')
        extra_kwargs = {
            'password':{'write_only': True,
                        'required':False,
                        'allow_blank': True},
        }

    def create(self, validated_data):

        if(validated_data['password'] is not None):
            validated_data['password'] = pbkdf2_sha256.hash(validated_data['password'])
        
        if("profile_pic" not in validated_data):
            user = User.objects.create(username=validated_data['username'], 
                                    email = validated_data['email'] ,  
                                    password = validated_data['password'],
                                    first_name=validated_data['first_name'],  
                                    last_name=validated_data['last_name'], 
                                    role=validated_data['role'],
                                    provider = validated_data['provider'])
        else:
            user = User.objects.create(username=validated_data['username'], 
                                    email = validated_data['email'] ,  
                                    password = validated_data['password'],
                                    first_name=validated_data['first_name'],  
                                    last_name=validated_data['last_name'], 
                                    role=validated_data['role'],
                                    provider = validated_data['provider'])

        return user

class BoxSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Box
        fields = ('id',
            'name',
            'width',
            'height',
            'depth',
            'front_texture',
            'top_texture',
            'bottom_texture',
            'back_texture',
            'right_texture',
            'left_texture',
            'preview_image',
            'material',
            'user',
            'description')

class BoxPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxPrice
        fields = ('material','material_price','decoration_price')

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('id','box','quantity','unit_price')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id',
            'purchase',
            'address',
            'state',
            'city',
            'zip_code',
            'status',
            'date',
            'user',
            'total_order',
            'pending_order',
            'delivered_order')

class BoxPreviewSerliazer(serializers.ModelSerializer):
     class Meta:
        model = Box
        fields = ('id',
            'description')

class PurchaseReadSerializer(PurchaseSerializer):
    box = BoxPreviewSerliazer(read_only = True)

class OrderReadSerializer(OrderSerializer):
    purchase = PurchaseReadSerializer(read_only=True)






    