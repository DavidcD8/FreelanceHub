# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:service_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:service_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-quantity/<int:service_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.cancel_view, name='cancel'),
    path('cart/create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),

]
