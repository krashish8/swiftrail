from django import template
from ..models import *
import datetime

register = template.Library()

@register.filter
def get_berth(obj):
    return Passenger.get_berth(obj)


@register.filter
def get_delay(obj):
    departure = datetime.datetime.combine(datetime.date.today(), obj.departure)
    arrival = datetime.datetime.combine(datetime.date.today(), obj.arrival)
    print(obj.arrival)
    print(obj.departure)
    print(obj.arrival < obj.departure)
    if obj.arrival > obj.departure:
        departure = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), obj.departure)
    delay = departure - arrival
    return f'{delay.seconds//3600}:{(delay.seconds//60)%60}'