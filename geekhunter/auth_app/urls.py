from django.urls import path

from auth_app.views import login, register, logout

app_name = 'auth_app'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', register, name='signup'),

]
