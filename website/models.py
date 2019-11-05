from django.db import models
from accounts.models import *

CLASS_CHOICES=(
    ('1A', '1A'),
    ('2A', '2A'),
    ('3A', '3A'),
    ('SL', 'SL'),
    ('CC', 'CC'),
)

BERTH = {
    "1A": ["LB", "UB"],
    "2A": ["LB", "UB", "SL", "SU"],
    "3A": ["LB", "MB", "UB", "LB", "MB", "UB", "SL", "SU"],
    "CC": ["WS", "AS", "AS", "MS", "WS"],
}


class Station(models.Model):
    station_code = models.CharField(max_length=10, primary_key=True)
    station_name = models.CharField(max_length=30)
    # state = models.CharField(max_length=20, null=True)
    # zone = models.CharField(max_length=20, null=True)
    # address = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.station_name} ({self.station_code})'


class Train(models.Model):
    train_no = models.CharField(max_length=5, primary_key=True)
    train_name = models.CharField(max_length=100)
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='train_source')
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='train_destination')
    run_days = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.train_no} - {self.train_name}'


class TrainSeatChart(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    first_ac = models.IntegerField(verbose_name="1st AC")
    second_ac = models.IntegerField(verbose_name="2nd AC")
    third_ac = models.IntegerField(verbose_name="3rd AC")
    sleeper = models.IntegerField()
    chair_car = models.IntegerField()

    def get_1A(self, date):
        return self.first_ac - self.chart_tickets.filter(class_type="1A", date=date).count()
    
    def get_2A(self, date):
        return self.first_ac - self.chart_tickets.filter(class_type="2A", date=date).count()
    
    def get_3A(self, date):
        return self.first_ac - self.chart_tickets.filter(class_type="3A", date=date).count()
    
    def get_SL(self, date):
        return self.first_ac - self.chart_tickets.filter(class_type="SL", date=date).count()
    
    def get_CC(self, date):
        return self.first_ac - self.chart_tickets.filter(class_type="CC", date=date).count()
    
    def __str__(self):
        return f'{self.train} CHART'


class TrainSchedule(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    arrival = models.TimeField()
    departure = models.TimeField()
    distance = models.IntegerField()
    day = models.IntegerField()

    def __str__(self):
        return f'{self.train} at {self.station}'


class Ticket(models.Model):
    pnr = models.CharField(max_length=10, primary_key=True)
    chart = models.ForeignKey(TrainSeatChart, on_delete=models.CASCADE, related_name='chart_tickets')
    transaction_id = models.CharField(max_length=20)
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='ticket_source')
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='ticket_destination')
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    journey_date = models.DateField()
    class_type = models.CharField(choices=CLASS_CHOICES, max_length=2)
    booked_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'{self.pnr} by {self.booked_by}'


class Passenger(models.Model):
    GENDER_CHOICES=(
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others/Not Specified'),
    )
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    seat_no = models.IntegerField()

    def get_berth(self):
        if self.ticket.class_type == "3A" or self.ticket.class_type == "SL":
            seat = (self.seat_no - 1) % 8
            return BERTH["3A"][seat]
        elif self.ticket.class_type == "2A":
            seat = (self.seat_no - 1) % 4
            return BERTH["2A"][seat]
        elif self.ticket.class_type == "1A":
            seat = (self.seat_no - 1) % 2
            return BERTH["1A"][seat]
        elif self.ticket.class_type == "CC":
            seat = (self.seat_no - 1) % 5
            return BERTH["CC"][seat]

    def __str__(self):
        return f'{self.ticket}, {self.ticket.class_type}/{self.seat_no}/{self.get_berth()}/GN'

