from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from auth_app.models import PortalUser
from company_app.models import Company
from main_app.forms.UserProfileForm import UserProfileForm
from news_app.models import News


def index(request):
    news_list = News.objects.get_queryset().order_by('-created_at')
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


class UserProfileView(FormView):
    template_name = 'main_app/user_profile.html'
    success_url = reverse_lazy('main:index')

    def get_form(self, form_class=None):
        form = UserProfileForm(instance=PortalUser.objects.get(id=self.request.user.id))
        return form

    def post(self, request, *args, **kwargs):
        user = PortalUser.objects.get(id=request.user.id)
        credentials = {}
        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                credentials[key] = request.POST.get(key)

        for key in credentials:
            if key != 'password':
                setattr(user, key, credentials[key])

        if credentials['password'] != '':
            user.set_password(credentials['password'])
        user.save()

        return HttpResponseRedirect(self.success_url)
