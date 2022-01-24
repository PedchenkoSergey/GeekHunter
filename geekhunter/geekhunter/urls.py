"""geekhunter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD:geekhunter/geekhunter/urls.py
    path('', main, name='index'),
    path('auth/', include('auth_app.urls', namespace='auth')),
=======
    path('', include('main_app.urls', namespace='main')),
    path('auth/', include('auth_app.urls', namespace='auth')),
    path('company/', include('company_app.urls', namespace='company')),
>>>>>>> ba71d7bc11d6d9371981f58f09604deb31fe96d5:geekhunter/urls.py
]
