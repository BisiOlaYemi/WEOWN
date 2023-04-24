from django.urls import path
from . import views

urlpatterns = [
    path('contact', views.contact, name='contact'),
    path('download_enquiry/', views.download_enquiry, name='download_enquiry'),
]