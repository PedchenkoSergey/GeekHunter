from django import forms
from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.forms.widgets import Textarea
from django.utils.translation import ngettext

from .models import Company, HrManager, FavoriteResume, Card, Vacancy, Offer


class BigTextarea(Textarea):
    def __init__(self):
        default_attrs = {'cols': '120', 'rows': '10'}
        super().__init__(default_attrs)


class AdminChangeFrom(forms.ModelForm):
    class Meta:
        model = Card
        widgets = {
            'about': BigTextarea
        }
        fields = '__all__'


class ForReviewFilter(SimpleListFilter):
    title = 'Admin useful filters'
    parameter_name = 'moderation_status'

    def lookups(self, request, model_admin):
        return [
            ('all', 'For review'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'all':
            return queryset.exclude(status='DRAFT').filter(moderation_status='UNDER_REVIEW')


@admin.action(description='Approve selected')
def make_approved(modeladmin, request, queryset):
    updated = queryset.update(moderation_status='APPROVED')
    modeladmin.message_user(request, ngettext(
        '%d item was successfully approved.',
        '%d items were successfully approved.',
        updated,
    ) % updated, messages.SUCCESS)


@admin.action(description='Decline selected')
def make_declined(modeladmin, request, queryset):
    updated = queryset.update(moderation_status='NOT_APPROVED')
    modeladmin.message_user(request, ngettext(
        '%d item was successfully declined.',
        '%d items were successfully declined.',
        updated,
    ) % updated, messages.SUCCESS)


@admin.register(Card)
class AdminCard(admin.ModelAdmin):
    list_display = ('company', 'title', 'about', 'moderation_status', 'status')
    list_filter = (ForReviewFilter,)
    form = AdminChangeFrom
    actions = [make_approved, make_declined]


@admin.register(Vacancy)
class AdminVacancy(admin.ModelAdmin):
    list_display = ('title', 'moderation_status', 'status')
    list_filter = (ForReviewFilter,)
    form = AdminChangeFrom
    actions = [make_approved, make_declined]


admin.site.register(Company)
admin.site.register(HrManager)
admin.site.register(FavoriteResume)
admin.site.register(Offer)
