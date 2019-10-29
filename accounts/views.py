from django.shortcuts import render

app_name = 'accounts/'

def login(request):
    return render(request, app_name + 'login.html')

def register(request):
    return render(request, app_name + 'register.html')

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