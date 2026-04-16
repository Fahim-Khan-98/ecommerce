from django.urls import path,include
from account import views


app_name = 'account'
urlpatterns = [
    path('profile/', views.profile_update, name='profile'),
    path('register/', views.register,name="register"),
    path('login/', views.CustomerLogin,name="login"),
    path('logout/', views.CustomerLogout, name="logout"),
   

]

