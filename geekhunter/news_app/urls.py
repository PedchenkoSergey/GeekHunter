from django.urls import path

from news_app.views import PostListView, PostDetailView, PostCreationView, \
    PostEditView, PostDeleteView


app_name = 'news_app'

urlpatterns = [
    path('', PostListView.as_view(), name='news'),
    path('<int:pk>/', PostDetailView.as_view(), name='post'),
    path('create/', PostCreationView.as_view(), name='post_create'),
    path('edit/<int:pk>', PostEditView.as_view(), name='post_edit'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
]
