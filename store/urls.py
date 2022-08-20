from store import views
from django.contrib import admin
from django.urls import path

app_name='store'
urlpatterns = [

   path('', views.HomeListView.as_view(),name='index'),
   path('product/<slug:slug>' , views.ProductDetailView.as_view(), name='product-details')

]






