import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiftrail.settings")
application = get_wsgi_application()

from website.models import *

def create_station(station_code, station_name):
    Station.objects.create(station_code=station_code, station_name=station_name)

def create_train(train_no, train_name, source_code, destination_code, run_days, first_ac, second_ac, third_ac, sleeper, chair_car):
    source = Station.objects.get(station_code=source_code)
    destination = Station.objects.get(station_code=destination_code)
    train_obj = Train.objects.create(train_no=train_no, train_name=train_name, source=source, destination=destination, run_days=run_days)
    TrainSeatChart.objects.create(train=train_obj, first_ac=first_ac, second_ac=second_ac, third_ac=third_ac, sleeper=sleeper, chair_car=chair_car)

def create_schedule(train_no, station_code, arrival, departure, distance, day):
    train = Train.objects.get(train_no=train_no)
    station = Station.objects.get(station_code=station_code)
    TrainSchedule.objects.create(train=train, station=station, arrival=arrival, departure=departure, distance=distance, day=day)

def create_ticket(pnr, train_no, transaction_id, ticket_from, ticket_to, journey_date, class_type, booked_by, transaction_date, amount):
    Ticket.objects.create(pnr=pnr, seat_chart=train_no, transaction_id=transaction_id, ticket_from=ticket_from, ticket_to=ticket_to, journey_date=journey_date, class_type=class_tpe, booked_by=booked_by, transaction_date=transaction_date, amount=amount)

def create_passenger(pnr, name, age, gender, seat_no):
    Passenger.objects.create(ticket=pnr, name=name, age=age, gender=gender, seat_no=seat_no)

# create_station("DHN", "DHANBAD")
# create_station("BSB", "VARANASI")
# create_train(13307, "GANGASUTLEJ EXPRESS", "DHN", "BSB", "SUN MON WED FRI", 0, 0, 20, 20, 0)
# create_schedule(13307, "DHN", "15:30", "15:45", 0, 0)