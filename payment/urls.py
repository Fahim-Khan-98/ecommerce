
from django.urls import path
from payment import views
from . import views

app_name='payment'
urlpatterns = [
      path('checkout/', views.CheckoutTemplateView.as_view(), name="checkout"),
      path('paypal/',views.paypalPaymentMethod, name="paypal_payment"),


]
