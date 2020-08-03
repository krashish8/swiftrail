from django import template
from ..models import *
import datetime

register = template.Library()

BERTH = {
    "1A": ["LB", "UB"],
    "2A": ["LB", "UB", "SL", "SU"],
    "3A": ["LB", "MB", "UB", "LB", "MB", "UB", "SL", "SU"],
    "CC": ["WS", "AS", "AS", "MS", "WS"],
}

@register.filter
def get_berth(obj):
    ticket_obj = Ticket.objects.filter(pnr=obj.ticket)[0]
    if ticket_obj.class_type == "3A" or ticket_obj.class_type == "SL":
        seat = (obj.seat_no - 1) % 8
        return BERTH["3A"][seat]
    elif ticket_obj.class_type == "2A":
        seat = (obj.seat_no - 1) % 4
        return BERTH["2A"][seat]
    elif ticket_obj.class_type == "1A":
        seat = (obj.seat_no - 1) % 2
        return BERTH["1A"][seat]
    elif ticket_obj.class_type == "CC":
        seat = (obj.seat_no - 1) % 5
        return BERTH["CC"][seat]

@register.filter
def count(obj):
    return len(obj)

@register.filter
def get_delay(obj):
    departure = datetime.datetime.combine(datetime.date.today(), obj.departure)
    arrival = datetime.datetime.combine(datetime.date.today(), obj.arrival)
    if obj.arrival > obj.departure:
        departure = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), obj.departure)
    delay = departure - arrival
    return f'{delay.seconds//3600}:{(delay.seconds//60)%60}'

@register.filter
def get_travel_time(obj):
    source_time = datetime.datetime.combine(datetime.date.today(), obj['source'][0])
    day_diff = obj['destination'][1] - obj['source'][1]
    destination_time = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=day_diff), obj['destination'][0])
    delay = destination_time - source_time
    return f'{delay.seconds//3600}:{(delay.seconds//60)%60}'

@register.filter
def split(obj):
    return obj.split(' ')

@register.filter
def get_full_station_name(obj):
    station_name = Station.objects.filter(station_code=obj)[0]

    return station_name

@register.filter
def get_full_train_name(obj):
    train_name = Train.objects.filter(train_no=obj)[0]

    return train_name

@register.filter
def get_full_gender(obj):
    if obj == 'M':
        return "Male"
    elif obj == 'F':
        return "Female"
    else:
        return "Others/Not Specified"

@register.filter
def get_live_delay(obj):
    if obj[-1] != "M":
        return obj
    obj = int(obj[:-1])
    if (obj < 60):
        return str(obj) + " minutes"
    else:
        return str(obj//60) + ":" + str(obj%60) + " hours"