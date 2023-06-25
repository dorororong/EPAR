from django.urls import path
from . import views



app_name = 'login'



urlpatterns=[
    path('',views.login_view, name='login'), #domain.com/my_app
    path('register/', views.register_request, name='register'),   
    path('account_succeed/', views.account_succeed, name='account_succeed') , 
    path('logout/', views.logout_view, name='logout')
         ]


