from django.shortcuts import render, redirect, reverse
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from models import *
import datetime, bcrypt

def last_years():
    first_year = datetime.datetime.now().year - 100
    return list(range(datetime.datetime.now().year, first_year, -1))

def index(request):
    if not 'message' in request.session:
        request.session['message'] = ''
    li = last_years()
    context = {
    'message' : request.session['message'],
    'last_years' : li,
    'len' : len(li)
    }
    return render(request, 'pythonbelt/index.html', context)

def register(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    birthday = request.POST['birthday']
    birthmonth = request.POST['birthmonth']
    birthyear = request.POST['birthyear']
    password = request.POST['password']
    verify_password = request.POST['verify_password']
    date_hired = request.POST['date_hired']
    return userManager().register(request, first_name, last_name, username, email, birthday, birthmonth, birthyear, password, verify_password, date_hired)

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    return userManager().login(request, username, password)
def logout(request):
    request.session.flush()
    return redirect(reverse('index'))

def dashboard(request):
    user = User.objects.get(id=request.session['id'])
    user_wish_items = List.objects.filter(creator=user)
    users = User.objects.all()
    other_wish_items = List.objects.all().exclude(creator=user).exclude(co_wishers=user)
    context = {
        'user' : user,
        'user_wish_items' : user_wish_items,
        'co_wish_items' : List.objects.filter(co_wishers=user),
        'other_wish_items' : other_wish_items,
        'created_at': List.created_at,
    }
    return render(request, 'pythonbelt/dashboard.html', context)

def create_item(request):
    user_id = request.POST['id']
    wish_item = request.POST['wish_item']
    return WishManager().create_item(request, user_id, wish_item)

def wish_items(request, id):
    return WishManager().wish_items(request, id=id)

def add_new_item(request):
    return render(request, 'pythonbelt/create_item.html')

def add_item(request, id):
    return WishManager().add_item(request, id=id)

def delete(request, id):
    return WishManager().delete(request, id=id)

def remove(request, id):
    return WishManager().remove(request,id=id)
