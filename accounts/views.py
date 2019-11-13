from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import datetime
from .models import *
from django.db import connection
from collections import namedtuple

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    result = namedtuple('Result', [col[0] for col in desc])
    return [result(*row) for row in cursor.fetchall()]

app_name = 'accounts/'

def validateEmail(email):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def validateDate(date):
    date_format = '%Y-%m-%d'
    try:
        date_obj = datetime.datetime.strptime(date, date_format)
        return True
    except ValueError:
        return False

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, app_name + 'login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')

def register(request):
    context = {'username': '', 'email': '', 'first_name': '', 'last_name': '', 'gender': 'M', 'date_of_birth': '', 'phone_number': '', 'address': ''}
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        context['username'] = username
        context['email'] = email
        context['first_name'] = first_name
        context['last_name'] = last_name
        context['gender'] = gender
        context['date_of_birth'] = date_of_birth
        context['phone_number'] = phone_number
        context['address'] = address

        if password1 == password2:
            if not username.isalnum():
                messages.error(request, 'Username must not be blank and must contain only letters and numbers')
            elif len(password1) < 6:
                messages.error(request, 'Password length must be atleast 6')
            elif User.objects.filter(username=username.lower()):
                messages.error(request, f'The username {username} is already taken')
            elif not validateEmail(email):
                messages.error(request, f'The email {username} is not valid')
            elif User.objects.filter(email=email.lower()):
                messages.error(request, f'The email {email} is already taken')
            elif first_name == "":
                messages.error(request, 'First name must not be blank')
            elif gender not in ('M', 'F', 'O'):
                messages.error(request, 'Select a valid gender')
            elif not validateDate(date_of_birth):
                messages.error(request, 'Enter a valid Date of Birth')
            elif not phone_number.isnumeric() or phone_number[0] < '6' or len(phone_number) != 10:
                messages.error(request, 'Enter a valid 10 digit phone number')
            else:
                user = User.objects.create_user(username=username.lower(), password=password1, email=email.lower(), first_name=first_name, last_name=last_name)
                with connection.cursor() as cursor:
                    cursor.execute(f"INSERT INTO `accounts_profile` (`user_id`, `gender`, `phone_number`, `date_of_birth`, `address`) VALUES ('{user.id}', '{gender}', '{phone_number}', '{date_of_birth}', '{address}')")
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
        return render(request, app_name + 'register.html', context=context)
    return render(request, app_name + 'register.html', context=context)

def profile(request):
    context = {}
    if request.method == "POST":
        old_password = request.POST['oldpassword']
        new_password1 = request.POST['newpassword1']
        new_password2 = request.POST['newpassword2']
        user = auth.authenticate(request, username=request.user.username, password=old_password)
        if user is not None:
            if new_password1 != new_password2:
                messages.error(request, "Confirmation Password did not match")
            else:
                user.set_password(new_password1)
                user.save()
                messages.success(request, "Password successfully changed")
        else:
            messages.error(request, "Old Password entered is incorrect")
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `accounts_profile` INNER JOIN `auth_user` ON (`accounts_profile`.`user_id` = `auth_user`.`id`) WHERE `auth_user`.`id` = '{request.user.id}'")
        profile_obj = namedtuplefetchall(cursor)
    context['profile'] = profile_obj[0]
    return render(request, app_name + 'profile.html', context=context)

def edit_profile(request):
    return render(request, app_name + 'edit-profile.html')

