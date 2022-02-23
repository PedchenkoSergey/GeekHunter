from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='user_avatar')
def user_avatar_filter(path):
    if not path:
        path = 'user_photo/default_user_photo.png'
    return f'{settings.MEDIA_URL}{path}'
