from django import template
from ..models import *
import datetime
from django.db import connection
from collections import namedtuple

register = template.Library()

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    result = namedtuple('Result', [col[0] for col in desc])
    return [result(*row) for row in cursor.fetchall()]

BERTH = {
    "1A": ["LB", "UB"],
    "2A": ["LB", "UB", "SL", "SU"],
    "3A": ["LB", "MB", "UB", "LB", "MB", "UB", "SL", "SU"],
    "CC": ["WS", "AS", "AS", "MS", "WS"],
}

@register.filter
def get_berth(obj):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `website_ticket` WHERE `pnr` = '{obj.ticket_id}'")
        ticket_obj = namedtuplefetchall(cursor)[0]
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