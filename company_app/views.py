from django.core import serializers
from django.shortcuts import render, get_object_or_404

from .models import Card


# Create your views here.

def get_company_card(request, pk=None):
    card = get_object_or_404(Card, pk=pk)
    card_data = serializers.serialize("python", Card.objects.filter(id=pk))
    context = {
        'title': 'company card',
        'card': card,
        'card_data': card_data,
    }
    if card.status == 'ACTIVE' and card.moderation_status == 'APPROVED':
        return render(request, 'company_app/company_card.html', context)
    else:
        return render(request, 'company_app/company_card_not_available.html', context)
