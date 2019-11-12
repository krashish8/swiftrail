from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db import connection
from collections import namedtuple
from django.views.decorators.csrf import csrf_exempt

from datetime import date, datetime

cursor = connection.cursor()

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

weekdays = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

def index(request):
    return render(request, app_name + 'index.html')


def pnr_status(request):
    context = {'is_submit': False}
    if request.method == "POST":
        pnr = request.POST.get('pnr')
        cursor.execute(f"SELECT * FROM `website_ticket` INNER JOIN `website_train` ON (`website_ticket`.`train_id` = `website_train`.`train_no`) WHERE `pnr` = '{pnr}'")
        ticket_obj = namedtuplefetchall(cursor)
        if not ticket_obj:
            messages.error(request, 'The given PNR Number does not exist.')
        else:
            context['is_submit'] = True
            ticket_obj = ticket_obj[0]
            train_no = ticket_obj.train_id
            
            context['ticket'] = ticket_obj
            
            cursor.execute(f"SELECT * FROM `website_passenger` WHERE `ticket_id` = '{ticket_obj.pnr}'")
            passenger_obj = namedtuplefetchall(cursor)
            context['passengers'] = passenger_obj
    return render(request, app_name + 'pnr-status.html', context=context)


def train_enquiry(request):
    return render(request, app_name + 'train-enquiry.html')


def train_schedule(request):
    context = {'is_submit': False}
    if request.method == "POST":
        train_no = request.POST.get('train-no')
        cursor.execute(f"SELECT * FROM `website_train` WHERE `train_no`='{train_no}'")
        train_obj = namedtuplefetchall(cursor)
        if not train_obj:
            messages.error(request, 'The given Train Number does not exist.')
        else:
            context['is_submit'] = True
            train_obj = train_obj[0]
            cursor.execute(f"SELECT * FROM `website_trainschedule` INNER JOIN `website_station` ON (`website_trainschedule`.`station_id` =`website_station`.`station_code`) WHERE `train_id`='{train_no}' ORDER BY distance ASC")
            schedule_obj = namedtuplefetchall(cursor)
            context['train'] = train_obj
            context['schedules'] = schedule_obj
    return render(request, app_name + 'train-schedule.html', context=context)


def train_search(request):
    return render(request, app_name + 'train-search.html')

def book_ticket(request):
    context = {"is_submit": False, "flexible":False, "train_search_page": True}


    if request.method == "POST" and request.POST.get("passenger_detail_page") != "True":
        print(1)
        journey_date = request.POST.get("date")
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        flexible = request.POST.get("flexible")

        if flexible == "yes":
            context['flexible'] = True

        day_number_source = datetime.strptime(journey_date, "%Y-%m-%d").weekday()  #Day Number for searched date

        cursor.execute(f"SELECT T1.train_id, T1.day FROM website_trainschedule as T1, website_trainschedule as T2 WHERE T1.station_id='{source}' AND T2.station_id='{destination}' AND T1.distance < T2.distance AND T1.train_id=T2.train_id")
        search_flexible = namedtuplefetchall(cursor)

        # Splitting search_flexible in two parts, each storing train number
        search_with_date = []
        search_without_date = []
        for s in search_flexible:
            day_number_train = (day_number_source - s.day + 7) % 7
            day_train = weekdays[day_number_train]
            cursor.execute(f"SELECT train_no FROM website_train WHERE train_no='{s.train_id}' AND run_days LIKE '%{day_train}%'")
            try:
                search_with_date += cursor.fetchone()
            except:
                pass
            cursor.execute(f"SELECT train_no FROM website_train WHERE train_no='{s.train_id}' AND run_days NOT LIKE '%{day_train}%'")
            try:
                search_without_date += cursor.fetchone()
            except:
                pass
        
        # Complete detail of train
        trains_obj_with_date = []
        trains_obj_without_date = []
        traintime_with_date = []
        traintime_without_date = []

        seat_availability_with_date = []
        seat_availability_without_date = []

        for train_no in search_with_date:
            cursor.execute(f"SELECT * FROM `website_train` WHERE `train_no`='{train_no}'")
            trains_obj_with_date += namedtuplefetchall(cursor)
            l = {}
            cursor.execute(f"SELECT `arrival`, `day` FROM `website_trainschedule` WHERE `train_id`='{train_no}' AND `station_id`='{source}'")
            l['source'] = cursor.fetchone()
            cursor.execute(f"SELECT `arrival`, `day` FROM `website_trainschedule` WHERE `train_id`='{train_no}' AND `station_id`='{destination}'")
            l['destination'] = cursor.fetchone()
            traintime_with_date.append(l)

            cursor.execute(f"SELECT * FROM `website_trainseatchart` WHERE `train_id`='{train_no}' AND `journey_date`='{journey_date}'")
            seat_chart = namedtuplefetchall(cursor)
            seat_availability_with_date += seat_chart


        for train_no in search_without_date:
            cursor.execute(f"SELECT * FROM `website_train` WHERE `train_no`='{train_no}'")
            trains_obj_without_date += namedtuplefetchall(cursor)
            l = {}
            cursor.execute(f"SELECT `arrival`, `day` FROM `website_trainschedule` WHERE `train_id`='{train_no}' AND `station_id`='{source}'")
            l['source'] = cursor.fetchone()
            cursor.execute(f"SELECT `arrival`, `day` FROM `website_trainschedule` WHERE `train_id`='{train_no}' AND `station_id`='{destination}'")
            l['destination'] = cursor.fetchone()
            traintime_without_date.append(l)

            cursor.execute(f"SELECT * FROM website_trainseatchart WHERE `train_id`='{train_no}' AND `journey_date`='{journey_date}'")
            seat_chart = namedtuplefetchall(cursor)
            seat_availability_without_date += seat_chart
        if not trains_obj_with_date and not trains_obj_without_date:
            messages.error(request, 'No Trains Found.')
        else:
            context['t1'] = zip(trains_obj_with_date, traintime_with_date, seat_availability_with_date)
            context['t2'] = zip(trains_obj_without_date, traintime_without_date, seat_availability_without_date)
            context['t3'] = zip(trains_obj_with_date, traintime_with_date, seat_availability_with_date)
            context['t4'] = zip(trains_obj_without_date, traintime_without_date, seat_availability_without_date)
            context['is_t1'] = trains_obj_with_date
            context['is_t2'] = trains_obj_without_date
            context['source'] = source
            context['destination'] = destination
            context['journey_date'] = journey_date
        print(context)

    elif request.method == "POST" and request.POST.get("passenger_detail_page") == "True":
        print(1)
        context['passenger_detail_page'] = True
        context['train_search_page'] = False
        train_no = request.POST.get("train_no")
        journey_date = request.POST.get("journey_date")
        class_type = request.POST.get("class_type")
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        travel_time = request.POST.get("travel_time")
        context = {
            'train_no': train_no,
            'journey_date': journey_date,
            'class_type': class_type,
            'source': source,
            'destination': destination,
            'travel_time': travel_time
        }
        cursor.execute(f"SELECT * FROM website_train WHERE train_no='{train_no}'")
        train_obj = namedtuplefetchall(cursor)
        cursor.execute(f"SELECT * FROM website_trainschedule WHERE train_id='{train_no}' AND station_id='{source}'")
        schedule_source_obj = namedtuplefetchall(cursor)
        cursor.execute(f"SELECT * FROM website_trainschedule WHERE train_id='{train_no}' AND station_id='{destination}'")
        schedule_destination_obj = namedtuplefetchall(cursor)
        context['train'] = train_obj
        context['schedule_source'] = schedule_source_obj
        context['schedule_destination'] = schedule_destination_obj

    return render(request, app_name + 'book-ticket.html', context=context)

def book_now(request):
    context = {}
    if request.method == "POST":
        train_no = request.POST.get("train_no")
        journey_date = request.POST.get("journey_date")
        class_type = request.POST.get("class_type")
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        travel_time = request.POST.get("travel_time")
        context = {
            'train_no': train_no,
            'journey_date': journey_date,
            'class_type': class_type,
            'source': source,
            'destination': destination,
            'travel_time': travel_time
        }
        cursor.execute(f"SELECT * FROM website_train WHERE train_no='{train_no}'")
        train_obj = namedtuplefetchall(cursor)
        cursor.execute(f"SELECT * FROM website_trainschedule WHERE train_id='{train_no}' AND station_id='{source}'")
        schedule_source_obj = namedtuplefetchall(cursor)
        cursor.execute(f"SELECT * FROM website_trainschedule WHERE train_id='{train_no}' AND station_id='{destination}'")
        schedule_destination_obj = namedtuplefetchall(cursor)
        context['train'] = train_obj
        context['schedule_source'] = schedule_source_obj
        context['schedule_destination'] = schedule_destination_obj
    
    print(context)
    
    return render(request, app_name + 'book-now.html', context=context)
    # else:
    #     return redirect('book-ticket')

def transaction_success(request):
    return render(request, app_name + 'transaction-success.html')