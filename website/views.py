from django.shortcuts import render
from django.contrib import messages
from .models import *
from django.db import connection
from collections import namedtuple

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    result = namedtuple('Result', [col[0] for col in desc])
    return [result(*row) for row in cursor.fetchall()]

app_name = 'website/'


def index(request):
    return render(request, app_name + 'index.html')


def pnr_status(request):
    context = {'is_valid_post': False}
    if request.method == "POST":
        pnr = request.POST.get('pnr')
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM `website_ticket` INNER JOIN `website_train` ON (`website_ticket`.`train_id` = `website_train`.`train_no`) WHERE `pnr` = '{pnr}'")
            ticket_obj = namedtuplefetchall(cursor)
        if not ticket_obj:
            messages.error(request, 'The given PNR Number does not exist.')
        else:
            context['is_valid_post'] = True
            ticket_obj = ticket_obj[0]
            train_no = ticket_obj.train_id
            
            context['ticket'] = ticket_obj
            
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM `website_passenger` WHERE `ticket_id` = '{ticket_obj.pnr}'")
                passenger_obj = namedtuplefetchall(cursor)
            context['passengers'] = passenger_obj
    return render(request, app_name + 'pnr-status.html', context=context)


def train_enquiry(request):
    return render(request, app_name + 'train-enquiry.html')


def train_schedule(request):
    context = {'is_valid_post': False}
    if request.method == "POST":
        train_no = request.POST.get('train-no')
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM `website_train` WHERE `train_no`='{train_no}'")
            train_obj = namedtuplefetchall(cursor)
        if not train_obj:
            messages.error(request, 'The given Train Number does not exist.')
        else:
            context['is_valid_post'] = True
            train_obj = train_obj[0]
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM `website_trainschedule` INNER JOIN `website_station` ON (`website_trainschedule`.`station_id` =`website_station`.`station_code`) WHERE `train_id`='{train_no}'")
                schedule_obj = namedtuplefetchall(cursor)
            context['train'] = train_obj
            context['schedules'] = schedule_obj
            print(schedule_obj)
    return render(request, app_name + 'train-schedule.html', context=context)


def train_search(request):
    return render(request, app_name + 'train-search.html')


def book_ticket(request):
    return render(request, app_name + 'book-ticket.html')