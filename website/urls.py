from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pnr-status/', views.pnr_status, name='pnr-status'),
    path('live-status/', views.live_status, name='live-status'),
    path('train-enquiry/', views.train_enquiry, name='train-enquiry'),
    path('train-search/', views.train_search, name='train-search'),
    path('train-schedule/', views.train_schedule, name='train-schedule'),
    path('book-ticket/', views.book_ticket, name='book-ticket'),
    path('book-now/<train_no>/<journey_date>/<class_type>/<source>-<destination>/', views.book_now, name='book-now'),
    path('transaction-success/<transaction_id>/', views.transaction_success, name='transaction-success'),
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/last/', views.last_transaction, name='last-transaction'),
    path('transactions/booked/', views.booked_history, name='booked-history'),
    path('transactions/cancelled/', views.cancelled_history, name='cancelled-history'),
    path('emergency/', views.emergency, name='emergency'),
    path('terms-of-service/', views.termsofservice, name='terms-of-service'),
]