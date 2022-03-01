from django.conf.global_settings import LOGIN_URL
from django.http import HttpResponseRedirect
from django.urls import reverse


def superuser_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('main:index'))
        else:
            return view_func(request, *args, **kwargs)
    return wrapped
