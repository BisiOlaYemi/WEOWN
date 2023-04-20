from django.urls import path
from . import views

app_name = 'investor'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('success/', views.success, name='success'),
    path('investboard/', views.investboard, name='investboard'),
]

