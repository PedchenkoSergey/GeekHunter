from django.urls import path

from .views import index, UserProfileView

app_name = 'main_app'

urlpatterns = [
    path("", index, name="index"),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
]
