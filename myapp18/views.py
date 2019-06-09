from random import randint
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import redirect_to_login
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
from django.urls import reverse
from .models import Category, Product, Client, Order
from .forms import OrderForm, InterestForm, UserForm
import datetime
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = str(datetime.datetime.now())
                request.session.set_expiry(3600)
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                else:
                    return HttpResponseRedirect(reverse('myapp18:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp18:index'))


# Create your views here.
def index(request):
        cat_list = Category.objects.all().order_by('id')[:10]
        current_user = request.user
        print(current_user)
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            userName = request.user.username
        else:
            userName = 'Guest'

        return render(request, 'myapp/index0.html',
                      {'last_login': str(request.session.get('last_login')), 'cat_list': cat_list, 'userName': userName,
                       'isUserLoggedIn': request.user.is_authenticated})



def about(request):
    if 'about_visits' in request.COOKIES:
        response = render(request, 'myapp/about0.html', {'about_visits': request.COOKIES['about_visits']})
        about_visits = int(request.COOKIES['about_visits'])+1
        response.set_cookie('about_visits', str(about_visits),max_age=5*60)
    else:
        response = render(request, 'myapp/about0.html', {'about_visits': str(0)})
        response.set_cookie('about_visits',0)
    return response



def detail(request, cat_no):
    warehouse = Category.objects.get(pk=cat_no).warehouse
    name = Category.objects.get(pk=cat_no).name
    prod_list = Product.objects.filter(category=cat_no)
    return render(request, 'myapp/detail0.html', {"prod_list":prod_list,'warehouse': warehouse, 'name': name})


def products(request):
    prodlist = Product.objects.filter(available=True).order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist})


def product_detail(request, prod_id):
    product = Product.objects.get(pk=prod_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['interested'] == '1':
                product.interested = product.interested + form.cleaned_data['quantity']
                product.save()
            return HttpResponseRedirect(reverse('myapp18:index'))
    else:
        form = InterestForm()
    return render(request, 'myapp/product_detail.html', {'form': form, 'product': product})


def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                product = Product.objects.get(pk=order.product.pk)
                product.stock = product.stock - order.num_units
                product.save()
                order.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})

    else:
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            form = OrderForm()
        else:
            msg = 'You are not registered user.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    return render(request, 'myapp/place_order.html', {'form': form, 'msg': msg, 'prodlist': prodlist})

def myorders(request):
    current_user = request.user
    print(current_user)
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        myorder = Order.objects.filter(client=current_user)
        return render(request, 'myapp/myorders.html', {'myorder': myorder})
    else:
        return redirect_to_login('/myapp18/myorders/', '/myapp18/login/')


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('myapp18:index'))
    else:
        form = UserForm()


    return render(request,'myapp/Register.html', {'form': form})

# Create your views here.
def forgotpassword(request):
    print(request.method)
    if request.method == 'POST':
        username = request.POST['username']
        a=User.objects.get(username=username)
        email=a.email
        print(email)
        c=randint(100,999)
        password = User.objects.make_random_password()
        b=str(username+str(c))
        print(settings.EMAIL_HOST_USER)
        a.set_password(b)
        a.save()
        send_mail(
            'New Password',
            'Your new Password is: '+b,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return HttpResponseRedirect(reverse('myapp18:forgotpassword'),{'email': email})
    else:
        return render(request, 'myapp/ForgotPassword.html')

