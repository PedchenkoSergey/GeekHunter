from django.urls import path
from .views import PostListView, PostDetailView

app_name = 'news_app'

urlpatterns = [
    path('', PostListView.as_view(), name='news'),
    path('<int:pk>/', PostDetailView.as_view(), name='post'),
]
