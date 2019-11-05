from django.shortcuts import render
from django.contrib import messages
from .models import *

app_name = 'website/'


def index(request):
    return render(request, app_name + 'index.html')


def pnr_status(request):
    context = {'is_valid_post': False}
    if request.method == "POST":
        pnr = request.POST.get('pnr')
        ticket_obj = Ticket.objects.filter(pnr=pnr)
        if not ticket_obj:
            messages.error(request, 'The given PNR Number does not exist.')
        else:
            context['is_valid_post'] = True
            ticket_obj = ticket_obj[0]
            train_no = ticket_obj.train.train_no
            train_obj = Train.objects.get(train_no=train_no)
            
            context['train'] = train_obj
            context['ticket'] = ticket_obj

            passenger_obj = Passenger.objects.filter(ticket=ticket_obj)
            context['passengers'] = passenger_obj
    return render(request, app_name + 'pnr-status.html', context=context)


def train_enquiry(request):
    return render(request, app_name + 'train-enquiry.html')


def train_schedule(request):
    context = {'is_valid_post': False}
    if request.method == "POST":
        train_no = request.POST.get('train-no')
        train_obj = Train.objects.filter(train_no=train_no)
        if not train_obj:
            messages.error(request, 'The given Train Number does not exist.')
        else:
            context['is_valid_post'] = True
            train_obj = train_obj[0]
            schedule_obj = TrainSchedule.objects.filter(train=train_obj).order_by('distance')
            context['train'] = train_obj
            context['schedules'] = schedule_obj
    return render(request, app_name + 'train-schedule.html', context=context)


def train_search(request):
    return render(request, app_name + 'train-search.html')


def book_ticket(request):
    return render(request, app_name + 'book-ticket.html')