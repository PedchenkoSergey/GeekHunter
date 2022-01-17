from django.urls import path
from auth_app.views import *

app_name = 'auth_app'

urlpatterns = [
    path('login/', login, name='login')
]