from django.shortcuts import redirect, render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User,Role,Box,BoxPrice, Purchase, Order
from .serializer import UserSerializer, BoxSerializer, BoxPriceSerializer, PurchaseSerializer, OrderSerializer, PurchaseReadSerializer,OrderReadSerializer
from passlib.hash import pbkdf2_sha256
from .utils import generate_random_username
from .google_authentication import Google_Authentication
from .token import Token
from rest_framework import status
from .mailer import Mailer
from django.db.models import RestrictedError

def home(request):
    return render(request,'jwt_auth_login_register/home.html')

def box_test(request):
    return render(request,'jwt_auth_login_register/box_test.html')

def login(request):
    return render(request,'jwt_auth_login_register/index.html')

def signup(request):
    return render(request,'jwt_auth_login_register/register.html')

def contact(request):
    return render(request,'jwt_auth_login_register/contact.html')

def about(request):
    return render(request,'jwt_auth_login_register/about.html')

def boxDesign(request):
    return render(request,'jwt_auth_login_register/boxDesign.html')

def savedDesign(request):
    return render(request,'jwt_auth_login_register/savedDesign.html')

def editBox(request,uuid):
    return render(request,'jwt_auth_login_register/boxDesign.html')

def cart(request):
    return render(request,'jwt_auth_login_register/cart.html')

def checkout(request,uuid):
    return render(request,'jwt_auth_login_register/checkout.html')

def main2(request):
    return render(request,'jwt_auth_login_register/main2.html')

def admin(request):
    return render(request,'jwt_auth_login_register/dashboard.html')

def updateOrder(request,uuid):
    return render(request,'jwt_auth_login_register/order_form.html')

def customer(request,uuid):
    return render(request,'jwt_auth_login_register/customer.html')

def profile(request):
    return render(request,'jwt_auth_login_register/profile.html')

def orders(request):
    return render(request,'jwt_auth_login_register/orders.html')

def logout(request):
    return render(request,'jwt_auth_login_register/logout.html')

def box_preview(request,uuid):
    return render(request,'jwt_auth_login_register/box_preview.html')

def googleAuthentication(request):
    auth_code = request.GET.get('code')
    google = Google_Authentication()
    oauth_details = google.get_google_access_token(auth_code)
    response = google.fetch_user_details_google(oauth_details['access_token'])
    if(not User.objects.filter(email = response['email']).exists()):
        user={}
        user['first_name'] = response['given_name']
        user['last_name'] = response['family_name']
        user['email'] = response['email']
        user['provider'] = 'google'
        if(not Role.objects.filter(name = "end_user").exists()):
            role = Role.objects.create()
            role.name = "end_user"
            role.save()
        user['role'] = Role.objects.get(name = "end_user").id
        user['password']=None
        user['username']=response['email'].split('@')[0]+"_"+generate_random_username()
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    payload={"email":response['email']}   
    tok  = Token()
    token = tok.get_access_token_for_first_time(payload,3600,7)
    return render(request,'jwt_auth_login_register/callback.html',token)

   
class CreateUserAPIView(APIView):
    def post(self, request):
        user = request.data
        user._mutable = True
        if(not Role.objects.filter(name = "end_user").exists()):
            role = Role.objects.create()
            role.name = "end_user"
            role.save()
        user['role'] = Role.objects.get(name = "end_user").id
        user['provider']=""
        user._mutable = False
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

Register = CreateUserAPIView.as_view()


class LoginAPI(APIView):

    def post(self, request, *args, **kwargs):
        
        if "username" not in request.data  :
            return Response({'Error': "Please provide username"}, status=400)

        if "password" not in request.data  :
            return Response({'Error': "Please provide password"}, status=400)
        
        username = request.data['username']
        password = request.data['password']

        if(username is None or username==""):
            return Response({'Error': "Please provide username"}, status=400)

        if(password is None or password==""):
            return Response({'Error': "Please provide password"}, status=400)
        
        try:
            user = User.objects.get(username=username)
            if(user.password is None):
                return Response({'Error':"Invalid password"},status=400)

            if not pbkdf2_sha256.verify(password,user.password):
                return Response({'Error': "Invalid password"}, status=400)

        except User.DoesNotExist:
            return Response({'Error': "Invalid username"}, status=400)

        if user:
            payload={"email":user.email}
            oauth_details = Token.get_access_token_for_first_time(self,payload,3600,7)
            oauth_details['role'] = str(user.role)
            return Response(
              oauth_details,
              status=200,
              content_type="application/json"
            )

        else:
            return Response(
              {'Error': "Invalid credentials"},
              status=400,
              content_type="application/json"
            )

class ValidateTokenAPI(APIView):
    def post(self, request, *args, **kwargs):
        val  = Token()
        if "access_token" not in request.data  :
            print("Valid")
            return Response({'Error': "Please provide acccess_token"}, status=400)
        access_token = request.data['access_token']
        response = {}
        status = 200
        content_type="application/json"
        try:
            val.validate_access_token(access_token)
            response['Validation'] = "Success"
        except Exception as e:
            status = 401
            response['Validation '] = "Failed"
            response['message'] = str(e)

        return Response(response,status = status,content_type = content_type)

class BoxCreateAPI(APIView):
    def post(self, request, *args, **kwargs):
        box = request.data
        access_token = request.META['HTTP_AUTHORIZATION']
        token = Token()
        box._mutable = True
        box['user'] = token.get_user_from_token(access_token).id
        box._mutable = False
        serializer = BoxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetBoxesAPI(APIView):
    def get(self,request, *args, **kwargs):
        token = Token()
        access_token = request.META['HTTP_AUTHORIZATION']
        boxes  = Box.objects.all().filter(user = token.get_user_from_token(access_token))
        serializer = BoxSerializer(boxes,many=True)
        return Response(serializer.data)

class GetBoxAPI(APIView):
    def post(self,request, *args, **kwargs):
        uuid = request.data['uuid']
        try:
            box = Box.objects.get(id=uuid)
        except Box.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BoxSerializer(box)
        return Response(serializer.data)

class EditBoxAPI(APIView):
    def put(self,request, *args, **kwargs):
        uuid = request.data['uuid']
        try:
            box = Box.objects.get(id=uuid)
        except Box.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BoxSerializer(data = request.data,instance=box)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteBoxAPI(APIView):
    def delete(self,request, *args, **kwargs):
        uuid = request.data['uuid']
        try:
            box = Box.objects.get(id=uuid)
        except Box.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            box.delete()
        except RestrictedError:
            return Response(
              {'Error': "Orders are attached with that box so it cannot be deleted"},
              status=status.HTTP_412_PRECONDITION_FAILED,
              content_type="application/json"
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetMaterialPrice(APIView):
     def post(self,request, *args, **kwargs):
         material  = request.data['material']
         try:
             box_price = BoxPrice.objects.get(material = material)
         except BoxPrice.DoesNotExist:
             return Response(status=status.HTTP_404_NOT_FOUND)
         serializer = BoxPriceSerializer(box_price)
         return Response(serializer.data)

class PurchaseAPI(APIView):
    def post(self,request, *args, **kwargs):
        serializer = PurchaseSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUserDetailAPI(APIView):
    def post(self,request, *args, **kwargs):
        uuid = request.data['uuid']
        try:
            user = User.objects.get(id=uuid)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)

class GetPurchaseDetailsAPI(APIView):
    def post(self,request, *args, **kwargs):
        uuid = request.data['uuid']
        try:
            purchase = Purchase.objects.get(id=uuid)
        except Purchase.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        serializer = PurchaseSerializer(purchase)
        return Response(serializer.data)

class MakeOrderAPI(APIView):
    def post(self,request,*args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllUsers(APIView):
    def get(self,request,*args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)

class GetAllOrders(APIView):
    def get(self,request,*args,**kwargs):
        orders = Order.objects.all()
        serializer = OrderReadSerializer(orders,many=True)
        return Response(serializer.data)

class GetAllPurchase(APIView):
    def get(self,request,*args,**kwargs):
        purchase = Purchase.objects.all()
        serializer  = PurchaseReadSerializer(purchase,many = True)
        return Response(serializer.data)

class DeleteOrder(APIView):
    def delete(self,request,*args,**kwargs):
        uuid = request.data['uuid']
        try:
            order = Order.objects.get(id=uuid)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EditOrder(APIView):
    def put(self,request,*args,**kwargs):
        uuid = request.data['uuid']
        try:
            order = Order.objects.get(id=uuid)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(data = request.data,instance=order)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetOrder(APIView):
    def post(self,request,*args,**kwargs):
        uuid = request.data['uuid']
        try:
            order = Order.objects.get(id=uuid)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class GetOrders(APIView):
    def post(self,request,*args,**kwargs):
        uuid = request.data['uuid']
        try:
            orders = Order.objects.filter(user=uuid)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderReadSerializer(orders,many=True)
        return Response(serializer.data)
    
    def get(self,request,*args,**kwargs):
        access_token = request.META['HTTP_AUTHORIZATION']
        token = Token()
        uuid = token.get_user_from_token(access_token).id
        try:
            orders = Order.objects.filter(user=uuid)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderReadSerializer(orders,many=True)
        return Response(serializer.data)

class DeleteUser(APIView):
    def delete(self,request,*args,**kwargs):
        uuid = request.data['uuid']
        try:
            user = User.objects.get(id=uuid)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminValidation(APIView):
    def get(self,request,*args,**kwargs):
        access_token = request.META['HTTP_AUTHORIZATION']
        token = Token()
        role = token.get_user_from_token(access_token).role
        if(str(role)=="admin"):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class SendMail(APIView):
    def post(self,request,*args,**kwargs):
        mail = Mailer()
        mail.send_messages(subject='Thank you for contacting us',
                   template='jwt_auth_login_register/email.html',
                   context={"name":request.data['name'],"message":request.data['message']},
                   to_emails=[request.data['email']])
        mail.send_messages(subject=request.data['subject'],
                   template='jwt_auth_login_register/admin_email.html',
                   context={"name":request.data['name'],"message":request.data['message'],"email":request.data['email']},
                   to_emails=['tvidhi0207@gmail.com','parthmaniyar90@gmail.com'])
        return Response(status=status.HTTP_200_OK)

class GetUserDetailFromToken(APIView):
    def get(self,request,*args,**kwargs):
        access_token = request.META['HTTP_AUTHORIZATION']
        token = Token()
        user = token.get_user_from_token(access_token)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UpdateProfilePic(APIView):
    def patch(self,request,*args,**kwargs):
        access_token = request.META['HTTP_AUTHORIZATION']
        token = Token()
        user = token.get_user_from_token(access_token)
        data = {"profile_pic":request.data['profile_pic']} 
        serializer = UserSerializer(user,data=data,partial = True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
