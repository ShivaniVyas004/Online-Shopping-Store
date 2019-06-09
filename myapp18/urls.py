from django.urls import path
from django.urls import include
from myapp18 import views

app_name = 'myapp18'

urlpatterns = [

    path(r'index/', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'<int:cat_no>/', views.detail, name='detail'),
    path(r'place_order/', views.place_order, name='place_order'),
    path(r'products/', views.products, name='products'),
    path(r'products/<int:prod_id>', views.product_detail, name='product_detail'),
    path(r'login/', views.user_login, name='user_login'),
    path(r'logout/', views.user_logout, name='user_logout'),
    path(r'myorders/', views.myorders, name='myorders'),
    path(r'Register/', views.register, name='Register'),
    path(r'forgotpassword/', views.forgotpassword, name='forgotpassword')
]

