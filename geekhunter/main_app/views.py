from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from company_app.models import Company
from news_app.models import News


# Create your views here.
def index(request):
    news_list = News.objects.get_queryset().filter(status='APPROVED').order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(news_list, 2)
    try:
        page_number = paginator.page(page)
    except PageNotAnInteger:
        page_number = paginator.page(1)
    except EmptyPage:
        page_number = paginator.page(paginator.num_pages)
    context = {
        "title": "GeekHunter",
        "companies": Company.objects.all(),
        "news": page_number
    }
    return render(request, "main_app/index.html", context)
