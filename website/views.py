from django.shortcuts import render

app_name = 'website/'

def index(request):
    return render(request, app_name + 'index.html')

def pnr_status(request):
    return render(request, app_name + 'pnr-status.html')

def train_enquiry(request):
    return render(request, app_name + 'train-enquiry.html')

def train_schedule(request):
    return render(request, app_name + 'train-schedule.html')

def train_search(request):
    return render(request, app_name + 'train-search.html')

def book_ticket(request):
    return render(request, app_name + 'book-ticket.html')