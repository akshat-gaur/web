from django.urls import path
from .views import *
urlpatterns = [
	path('',login_fun,name='insert'),
	path('home',new_home_fun,name='home'),
	path('products',product_fun,name='products'),
	path('reveiw_api',r_api_fun,name='reveiw_api'),
	path('related_product_api',p_api_fun,name='p_api'),
	path('order',order_api_fun,name='order'),
	path('sign_up',sign_up_fun,name='sign_up'),
	path('product_list',p_list_fun,name='product_list'),
	path('vender',vender_fun,name='vender'),
	path('Browising_history',bh_fun,name='bh'),
	path('order_history',oh_fun,name='oh'),
	path('cart',cart_fun,name='cart'),
	path('vender_login',vs_fun,name='ren')      

	]


	