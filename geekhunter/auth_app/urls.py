from django.urls import path

from auth_app.views import PortalUserLoginView, PortalUserLogoutView, PortalUserRegisterView

app_name = 'auth_app'

urlpatterns = [
    path('login/', PortalUserLoginView.as_view(), name='login'),
    path('logout/', PortalUserLogoutView.as_view(), name='logout'),
    path('signup/', PortalUserRegisterView.as_view(), name='signup'),

]
