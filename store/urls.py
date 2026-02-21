from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('product/<int:product_id>/', views.ProductDetail.as_view(), name='product_detail'),
    path('cart/', views.ShowCart.as_view(), name='show_cart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('orders/', views.Orders.as_view(), name='orders'),
    path('search/', views.Search.as_view(), name='search'),
]
