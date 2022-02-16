from django.shortcuts import render, get_object_or_404
from .models import News


def news(request):
    title = 'новости'
    news_list = News.objects.filter(status='APPROVED')
    context = {
        'title': title,
        'news': news_list
    }
    return render(request, 'news_app/news.html', context)


def post(request, pk):
    title = 'новость'
    context = {
        'title': title,
        'post': get_object_or_404(News, pk=pk),
    }
    return render(request, 'news_app/post.html', context)
