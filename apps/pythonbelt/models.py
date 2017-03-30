from django.db import models
from django.contrib.sessions.models import Session
from importlib import import_module
from django.conf import settings
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
from django.shortcuts import render, redirect, reverse
import re, bcrypt, datetime, json
from django.core import serializers

EMAIL_REGEX = re.compile(r'[\w\.+_-]+@[\w\._-]+\.[\w]*$')

def validateEmail(email):
    return EMAIL_REGEX.match(email)
#User Manager Methods
class userManager(models.Model):

    #register user into database
    def register(self, request, first_name, last_name, username, email, birthday, birthmonth, birthyear, password, verify_password, date_hired):
        if request.method == 'POST':
            if (len(first_name) < 3 or len(last_name) < 3):
                request.session['message'] = 'Names must be at least three (3) characters ( I know)'
                return redirect(reverse('index'))
            if User.objects.filter(email=email).exists():
                request.session['message'] = 'Email Theft Alert! '
                return redirect(reverse('index'))
            else:
                if password < 8:
                    request.session['message'] = 'Password must be at least 8 characters long'
                    return redirect(reverse('index'))
                elif(validateEmail(email) and password == verify_password):
                    hashed_password = bcrypt.hashpw(password.encode('UTF_8'), bcrypt.gensalt())
                    if User.objects.filter(username=username).exists():
                        request.session['message'] = 'Username already taken, try another one'
                        return redirect(reverse('index'))
                    User.objects.create(first_name=first_name, last_name=last_name, username=username, password=hashed_password, email=email, date_hired=date_hired)
                    user = User.objects.get(email=email)
                    Birthday.objects.create(user_id=user.id, birthday=birthday, birthmonth=birthmonth, birthyear=birthyear)
                    return userManager().login(request, username, password)
                elif(validateEmail(email) and password != verify_password):
                    request.session['message'] = 'Passwords do not match!'
                    return redirect(reverse('index'))
                else:
                    request.session['message'] = 'Invalid email! Register with a valid email!'
                    return redirect(reverse('index'))
        return redirect(reverse('index'))

    #login user
    def login(self, request, username, password):
        if request.method == 'POST':
            if (User.objects.filter(username=username).exists()):
                user = User.objects.get(username=username)
                if bcrypt.hashpw(password.encode('UTF_8'), user.password.encode('UTF_8')).decode() == user.password:
                    print user
                    #user couldn't be saved into session hence these:
                    request.session['user'] = serializers.serialize("json", User.objects.all())
                    request.session['id'] = user.id
                    request.session['message'] = ''
                    return redirect (reverse('dashboard'))
                else:
                    request.session['message'] = 'Wrong Password'
                    return redirect (reverse('index'))
            else:
                request.session['message'] = 'Username not recognized'
                return redirect (reverse('index'))
        else:
            return redirect(reverse('index'))


class WishManager(models.Model):

    #create wish item
    def create_item(self, request, user_id, wish_item):
        errors = []
        count = 0
        user = User.objects.get(id=user_id)
        if wish_item == '':
            errors.append('Please enter what you wish for, you can not add a blank wish!')
            count += 1
        if len(wish_item) < 4:
            errors.append('Please make what you wish for greater than 3 characters!')
            count += 1
        if count > 0:
            request.session['errors'] = errors
            return redirect(reverse('dashboard'))
        else:
            List.objects.create(creator=user, item=wish_item)
            return redirect(reverse('dashboard'))

    #show wished item
    def wish_items(self, request, id):
        item = List.objects.get(id=id)
        print item.creator.first_name
        context = {
        'creator' : List.objects.get(id=id).creator,
        'co_wishers' : List.objects.get(id=id).co_wishers.all(),
        'item' : item,
        }
        return render(request, 'pythonbelt/wish_item.html', context)

    #add wished item
    def add_item(self, request, id):
        co_wisher = User.objects.get(id=request.session['id'])
        item = List.objects.get(id=id)
        item.co_wishers.add(co_wisher)
        return redirect(reverse('dashboard'))

    #delete wished item
    def delete(self, request, id):
        item = List.objects.get(id=id)
        item.delete()
        request.session['message'] = 'You have successfully deleted that item from your wished list'
        return redirect(reverse('dashboard'))

    #remove co_wished item
    def remove(self, request, id):
        co_wisher = User.objects.get(id=request.session['id'])
        item = List.objects.get(id=id)
        item.co_wishers.remove(co_wisher)
        request.session['message'] = 'You have successfully removed that item from your wished list'
        return redirect(reverse('dashboard'))

#User Model
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length= 30)
    username = models.CharField(max_length= 30)
    email = models.CharField(max_length= 256)
    password = models.CharField(max_length= 256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_hired = models.DateField()

#User birthday
class Birthday(models.Model):
    birthday = models.IntegerField()
    birthmonth = models.IntegerField()
    birthyear = models.IntegerField()
    user = models.ForeignKey(User, related_name = "birthday")

#WishList
class List(models.Model):
    creator = models.ForeignKey(User, related_name = "my_trips")
    item = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    co_wishers = models.ManyToManyField(User)
