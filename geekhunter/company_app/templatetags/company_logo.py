from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='company_logo')
def company_logo_filter(path):
    if not path:
        path = 'company_logo/default_company_image.webp'
    return f'{settings.MEDIA_URL}{path}'
