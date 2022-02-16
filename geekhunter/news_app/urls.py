from django.urls import path

import news_app.views as news_app

app_name = 'news_app'

urlpatterns = [
    path('', news_app.news, name='news'),
    path('<int:pk>/', news_app.post, name='post'),
]
