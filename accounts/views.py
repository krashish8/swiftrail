from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import datetime
from .models import *

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
        print(date_of_birth)

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
            elif not phone_number.isnumeric() or phone_number[0] < '6':
                messages.error(request, 'Enter a valid 10 digit phone number')
            else:
                user = User.objects.create_user(username=username.lower(), password=password1, email=email.lower(), first_name=first_name, last_name=last_name)
                Profile.objects.create(username=user, gender=gender, phone_number=phone_number, date_of_birth=date_of_birth, address=address)
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
        return render(request, app_name + 'register.html', context=context)
    return render(request, app_name + 'register.html', context=context)

def profile(request):
    return render(request, app_name + 'profile.html')

def transactions(request):
    return render(request, app_name + 'transactions.html')

def last_transaction(request):
    return render(request, app_name + 'last-transaction.html')

def booked_history(request):
    return render(request, app_name + 'booked-history.html')

def cancelled_history(request):
    return render(request, app_name + 'cancelled-history.html')