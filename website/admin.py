from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Station)
admin.site.register(Train)
admin.site.register(TrainSeatChart)
admin.site.register(TrainSchedule)
admin.site.register(Ticket)
admin.site.register(Passenger)
