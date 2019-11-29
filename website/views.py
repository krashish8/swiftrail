from django.shortcuts import render, redirect, reverse, render_to_response
from django.contrib import messages
from .models import *
from django.db import connection
from collections import namedtuple
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import requests
import json
from instamojo_wrapper import Instamojo

API_KEY = 'test_530bc68fdd48fa14a39c6eedace'
AUTH_TOKEN = 'test_d5d9765989bcfd08e2514acafb5'
api = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/');


# 650a90b2c2af21576c724aa9582480e9
# 62ddf48ff6189aee2f1ec18cff16e48d

# c5f309813b0bf98878abfb22ae5df4f4
# fb165db20a4cbc85fe4849c16683e40e
import datetime

from random import randint

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

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

def calc_fare(train_no, class_type, source, destination):
    train_obj = Train.objects.get(train_no=train_no)
    s1 = TrainSchedule.objects.get(train=train_obj, station=source)
    s2 = TrainSchedule.objects.get(train=train_obj, station=destination)
    dist = abs(s1.distance - s2.distance)
    total_dist = 0
    if class_type == "1A":
        total_dist = dist*3
    elif class_type == "2A":
        total_dist = dist*1.8
    elif class_type == "3A":
        total_dist = dist*1.2
    elif class_type == "SL":
        total_dist = dist*0.6
    return round(total_dist, 2)


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
    context = {"is_submit": False}
    if request.method == "POST":
        source = request.POST.get("source")
        destination = request.POST.get("destination")

        cursor.execute(f"SELECT T1.train_id, T1.day FROM website_trainschedule as T1, website_trainschedule as T2 WHERE T1.station_id='{source}' AND T2.station_id='{destination}' AND T1.distance < T2.distance AND T1.train_id=T2.train_id")
        search = namedtuplefetchall(cursor)

        search_without_date = []
        for s in search:
            try:
                search_without_date += cursor.fetchone()
            except:
                pass
        
        trains_obj = []
        traintime = []

        for train_no in search:
            print(train_no)
            train_no = train_no.train_id
            cursor.execute(f"SELECT * FROM `website_train` WHERE `train_no`='{train_no}'")
            trains_obj += namedtuplefetchall(cursor)
            l = {}
            cursor.execute(f"SELECT `arrival`, `day` FROM `website_trainschedule` WHERE `train_id`='{train_no}' AND `station_id`='{source}'")
            l['source'] = cursor.fetchone()
            cursor.execute(f"SELECT `arrival`, `day` FROM `website_trainschedule` WHERE `train_id`='{train_no}' AND `station_id`='{destination}'")
            l['destination'] = cursor.fetchone()
            traintime.append(l)

        if not trains_obj:
            messages.error(request, 'No Trains Found.')
        else:
            context['t1'] = zip(trains_obj, traintime)
            context['source'] = source
            context['destination'] = destination
            context['is_submit'] = True
    return render(request, app_name + 'train-search.html', context=context)


@login_required
def book_ticket(request):
    context = {"is_submit": False, "flexible":False}


    if request.method == "POST":
        journey_date = request.POST.get("date")
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        flexible = request.POST.get("flexible")

        if flexible == "yes":
            context['flexible'] = True

        day_number_source = datetime.datetime.strptime(journey_date, "%Y-%m-%d").weekday()  #Day Number for searched date

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

    return render(request, app_name + 'book-ticket.html', context=context)

@login_required
def book_now(request, train_no, journey_date, class_type, source, destination):
    context = {
        'train_no': train_no,
        'journey_date': journey_date,
        'class_type': class_type,
        'source': source,
        'destination': destination,
    }
    cursor.execute(f"SELECT * FROM website_train WHERE train_no='{train_no}'")
    train_obj = namedtuplefetchall(cursor)
    cursor.execute(f"SELECT * FROM website_trainschedule WHERE train_id='{train_no}' AND station_id='{source}'")
    schedule_source_obj = namedtuplefetchall(cursor)
    cursor.execute(f"SELECT * FROM website_trainschedule WHERE train_id='{train_no}' AND station_id='{destination}'")
    schedule_destination_obj = namedtuplefetchall(cursor)
    context['train'] = train_obj[0]
    context['schedule_source'] = schedule_source_obj[0]
    context['schedule_destination'] = schedule_destination_obj[0]

    source_time = datetime.datetime.combine(datetime.date.today(), schedule_source_obj[0].arrival)
    day_diff = schedule_destination_obj[0].day - schedule_source_obj[0].day
    print(schedule_destination_obj[0].day , schedule_source_obj[0].day)
    destination_time = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=day_diff), schedule_destination_obj[0].arrival)
    print(destination_time, source_time, day_diff)
    travel_time = destination_time - source_time
    context['travel_time'] = travel_time
    context['n'] = range(6)
    context['fare'] = calc_fare(train_no, class_type, source, destination)
    fare = context['fare']
    if request.method == "POST":
        pnr = random_with_N_digits(5)
        while Ticket.objects.filter(pnr=pnr):
            pnr = random_with_N_digits(5)
        rows = Ticket.objects.all().count()
        transaction_id = 100000 + rows
        today = datetime.datetime.today()

        passengers = 0
        for i in range(1, 7):
            if request.POST.get("name" + str(i)) == "":
                break
            passengers += 1

        cursor.execute(f"INSERT INTO `website_ticket`(`pnr`, `transaction_id`, `journey_date`, `class_type`, `transaction_date`, `amount`, `booked_by_id`, `ticket_from_id`, `ticket_to_id`, `train_id`, `is_cancelled`) VALUES ('{pnr}','{transaction_id}','{journey_date}','{class_type}','{today}','{fare*passengers}','{request.user.id}','{source}','{destination}','{train_no}', '0')")
        cursor.execute("SELECT LAST_INSERT_ID()")
        c = 0

        for i in range(1, 7):
            if request.POST.get("name" + str(i)) == "":
                break
            c = c + 1
            name = request.POST.get("name" + str(i))
            age = request.POST.get("age" + str(i))
            gender = request.POST.get("gender" + str(i))
            seat_number = random_with_N_digits(2)
            cursor.execute(f"INSERT INTO `website_passenger`(`name`, `age`, `gender`, `seat_no`, `ticket_id`) VALUES ('{name}','{age}','{gender}','{seat_number}','{pnr}')")
        
        profile_obj = Profile.objects.get(user=request.user)
        response = api.payment_request_create(
            amount=fare*passengers,
            purpose='Booking Ticket (SwiftRail)',
            send_email=True,
            send_sms=True,
            buyer_name=request.user.first_name,
            email=request.user.email,
            phone=profile_obj.phone_number,
            redirect_url=request.build_absolute_uri(reverse('transaction-success', kwargs={'transaction_id':transaction_id})),
        )

        return HttpResponseRedirect(response['payment_request']['longurl'])
    
    return render(request, app_name + 'book-now.html', context=context)

# Custom function
def get_transaction_detail(transaction_id):
    cursor.execute(f"SELECT * FROM website_ticket WHERE transaction_id='{transaction_id}'")
    ticket_obj = namedtuplefetchall(cursor)
    train_no = ticket_obj[0].train_id
    source = ticket_obj[0].ticket_from_id
    destination = ticket_obj[0].ticket_to_id
    cursor.execute(f"SELECT * FROM website_train WHERE train_no='{train_no}'")
    train_obj = namedtuplefetchall(cursor)
    cursor.execute(f"SELECT * FROM website_trainschedule WHERE train_id='{train_no}' AND station_id='{source}'")
    schedule_source_obj = namedtuplefetchall(cursor)
    cursor.execute(f"SELECT * FROM website_trainschedule WHERE train_id='{train_no}' AND station_id='{destination}'")
    schedule_destination_obj = namedtuplefetchall(cursor)
    context = {}
    context['ticket'] = ticket_obj[0]
    context['train'] = train_obj[0]
    context['schedule_source'] = schedule_source_obj[0]
    context['schedule_destination'] = schedule_destination_obj[0]
    day_diff = schedule_destination_obj[0].day - schedule_source_obj[0].day
    arrival_date = ticket_obj[0].journey_date + datetime.timedelta(days=day_diff)
    context['arrival_date'] = arrival_date

    source_time = datetime.datetime.combine(ticket_obj[0].journey_date, schedule_source_obj[0].arrival)
    day_diff = schedule_destination_obj[0].day - schedule_source_obj[0].day
    destination_time = datetime.datetime.combine(arrival_date, schedule_destination_obj[0].arrival)
    travel_time = destination_time - source_time
    context['travel_time'] = travel_time

    cursor.execute(f"SELECT * FROM website_passenger WHERE ticket_id='{ticket_obj[0].pnr}'")
    passenger_obj = namedtuplefetchall(cursor)
    context['passengers'] = passenger_obj

    return context


@login_required
def transaction_success(request, transaction_id):
    context = get_transaction_detail(transaction_id)
    return render(request, app_name + 'transaction-success.html', context=context)

@login_required
def transactions(request):
    return render(request, app_name + 'transactions.html')

@login_required
def last_transaction(request):
    cursor.execute(f"SELECT * FROM website_ticket WHERE booked_by_id='{request.user.id}' ORDER BY transaction_id DESC")
    ticket_obj = namedtuplefetchall(cursor)
    context = {}
    if ticket_obj:
        context = get_transaction_detail(ticket_obj[0].transaction_id)
        context['found'] = True
    else:
        messages.error(request, 'No Transactions Found')
        context['found'] = False
    return render(request, app_name + 'last-transaction.html', context=context)

@login_required
def booked_history(request):
    cursor.execute(f"SELECT * FROM website_ticket WHERE (booked_by_id='{request.user.id}' AND is_cancelled='0') ORDER BY transaction_id DESC")
    ticket_obj = namedtuplefetchall(cursor)
    print(ticket_obj)
    all_tickets = []
    for ticket in ticket_obj:
        all_tickets.append(get_transaction_detail(ticket.transaction_id))
    return render(request, app_name + 'booked-history.html', {'all_tickets': all_tickets})


@login_required
def cancelled_history(request):
    cursor.execute(f"SELECT * FROM website_ticket WHERE (booked_by_id='{request.user.id}' AND is_cancelled='1') ORDER BY transaction_id DESC")
    ticket_obj = namedtuplefetchall(cursor)
    print(ticket_obj)
    all_tickets = []
    for ticket in ticket_obj:
        all_tickets.append(get_transaction_detail(ticket.transaction_id))
    return render(request, app_name + 'cancelled-history.html', {'all_tickets': all_tickets})

def emergency(request):
    return render(request, app_name + 'emergency.html')

def termsofservice(request):
    return render(request, app_name + 'terms-of-service.html')

def live_status(request):
    context = {'is_submit': False}
    if request.method == "POST":
        train_no = request.POST.get('train-no')
        date = request.POST.get('date')
        cursor.execute(f"SELECT * FROM `website_train` WHERE `train_no`='{train_no}'")
        train_obj = namedtuplefetchall(cursor)
        if not train_obj:
            messages.error(request, 'The given Train Number does not exist.')
        else:
            context['is_submit'] = True
            train_obj = train_obj[0]
            # cursor.execute(f"SELECT * FROM `website_trainschedule` INNER JOIN `website_station` ON (`website_trainschedule`.`station_id` =`website_station`.`station_code`) WHERE `train_id`='{train_no}' ORDER BY distance ASC")
            # schedule_obj = namedtuplefetchall(cursor)
            context['train'] = train_obj
            # context['schedules'] = schedule_obj

            d = ''
            for c in date:
                if c != '-':
                    d += c
        
            response = requests.get("http://indianrailapi.com/api/v2/livetrainstatus/apikey/bd65ce7e4f343268b4f85cc1cc95ef05/trainnumber/"+ str(train_no) +"/date/"+ str(d) +"/")
            print(response.text)
            j = json.loads(response.text)
            if j.get("Message") != "SUCCESS":
                messages.error(request, j.get("Message"))
                context['is_submit'] = False
            else:
                messages.success(request, 'SUCCESS.')
                context['current_station'] = j['CurrentStation']
                context['train_route'] = j['TrainRoute']

    return render(request, app_name + 'live-status.html', context=context)


@login_required
def ticket_cancel_page(request, pnr_no):
    Ticket.objects.filter(pnr=pnr_no).update(is_cancelled=1)
    context = {}
    messages.success(request, 'Your ticket has been successfully cancelled.')
    return render(request, app_name + 'ticket-cancel-page.html', context=context)
