from django.conf.urls import url
from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('home/',views.home),
    path('login/', views.login,name='login'),
   
    path('signup/', views.signup),
    path('about/', views.about),
    path('contact/', views.contact),
    path('boxdesign/',views.boxDesign),
    path('verify/',views.LoginAPI.as_view()),
    path('google/callback/login/',views.googleAuthentication),
    path('validateToken/',views.ValidateTokenAPI.as_view()),
    path('saveddesign/',views.savedDesign),
    path('boxcreate/',csrf_exempt(views.BoxCreateAPI.as_view())),
    path('getboxes/',csrf_exempt(views.GetBoxesAPI.as_view())),
    path('getbox/',views.GetBoxAPI.as_view()),
    path('editbox/',views.EditBoxAPI.as_view()),
    path('deletebox/',views.DeleteBoxAPI.as_view()),
    path('editbox/<str:uuid>/',views.editBox),
    path('register/',views.Register),
    path('getmaterailprice/',views.GetMaterialPrice.as_view()),
    path('cart/', views.cart),
    path('checkout/<str:uuid>/', views.checkout),
    path('main2/',views.main2),
    path('purchase/',views.PurchaseAPI.as_view()),
    path('getuserdetails/',views.GetUserDetailAPI.as_view()),
    path('getpurchasedetail/',views.GetPurchaseDetailsAPI.as_view()),
    path('makeorder/', views.MakeOrderAPI.as_view()),
    path('admin/',views.admin),
    path('getallusers/',views.GetAllUsers.as_view()),
    path('getallorders/',views.GetAllOrders.as_view()),
    path('purchases/',views.GetAllPurchase.as_view()),
    path('deleteorder/',views.DeleteOrder.as_view()),
    path('updateorder/<str:uuid>/',views.updateOrder),
    path('update_order/',views.EditOrder.as_view()),
    path('get_order/',views.GetOrder.as_view()),
    path('customer/<str:uuid>/',views.customer),
    path('get_orders/',views.GetOrders.as_view()),
    path('delete_user/',views.DeleteUser.as_view()),
    path('check_role/',views.AdminValidation.as_view()),
    path('logout/',views.logout)
]