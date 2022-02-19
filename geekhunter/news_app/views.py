from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, DetailView)
from .models import News


class PostListView(ListView):
    """
    Список всех APPROVED новостей
    """
    model = News
    # Под данным именем наш список статей будет доступен в шаблоне
    context_object_name = 'news'

    # Название шаблона
    template_name = 'news_app/news_list.html'

    def get_queryset(self):
        return News.objects.filter(status='APPROVED').order_by('-created_at')

class PostDetailView(DetailView):
    """
    Одна новость
    """

    model = News

    # Под данным именем наш список статей будет доступен в шаблоне
    context_object_name = 'post'

    # Название шаблона
    template_name = 'news_app/news_detail.html'
