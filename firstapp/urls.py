from django.urls import path
from .import views

urlpatterns = [
    path('product/',views.product_list,name = 'productlist'),
    path('cart/',views.view_cart,name= 'viewcart'),
    path('addcart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('removecart/<int:item_id>/',views.remove_cart,name = 'remove_cart'),
    path('login/',views.login_view, name = 'login'),
    path('logout/',views.logout_view, name = 'logout'),
    path('register/',views.register_view, name = 'register')
]