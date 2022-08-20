from django.urls import path,include
from account import views


app_name = 'account'
urlpatterns = [
    path('register/', views.register,name="register"),
    path('login/', views.CustomerLogin,name="login"),
   

]

