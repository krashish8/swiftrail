from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pnr-status/', views.pnr_status, name='pnr-status'),
    path('book-ticket/', views.book_ticket, name='book-ticket'),
    path('train-enquiry/', views.train_enquiry, name='train-enquiry'),
    path('train-search/', views.train_search, name='train-search'),
    path('train-schedule/', views.train_schedule, name='train-schedule'),
]