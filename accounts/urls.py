from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/last/', views.last_transaction, name='last-transaction'),
    path('transactions/booked/', views.booked_history, name='booked-history'),
    path('transactions/cancelled/', views.cancelled_history, name='cancelled-history'),
]