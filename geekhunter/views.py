from django.shortcuts import render


def main(request):
    title = 'main'
    context = {
        'title': title,
    }
    return render(request, 'geekhunter/base.html', context)