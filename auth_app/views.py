from django.shortcuts import render


def login(request):
    title = 'login'
    context = {
        'title': title,
    }
    return render(request, 'auth_app/login.html', context)
