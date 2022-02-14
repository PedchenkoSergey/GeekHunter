from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ngettext

from .models import Company, HrManager, FavoriteResume, Card, Vacancy, Offer
from .forms.AdminCompanyCardForm import AdminCompanyCardFrom
from .forms.AdminVacancyForm import AdminVacancyFrom


class ForReviewFilter(SimpleListFilter):
    title = 'Admin useful filters'
    parameter_name = 'moderation_status'

    def lookups(self, request, model_admin):
        return [
            ('for_review', 'For review'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'for_review':
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
    list_display = ('title', 'about', 'moderation_status', 'status')
    list_filter = (ForReviewFilter,)
    form = AdminCompanyCardFrom
    fieldsets = (
        ('General Information', {
            'fields': (('company', 'title', 'status'), 'about')
        }),
        ('Additional Descriptions', {
            'classes': ('collapse',),
            'fields': ('priorities', 'awards')
        }),
        ('Approval', {
            'fields': ('moderation_status', 'error_text')
        }),
    )
    actions = [make_approved, make_declined]


@admin.register(Vacancy)
class AdminVacancy(admin.ModelAdmin):
    list_display = ('title', 'moderation_status', 'status')
    list_filter = (ForReviewFilter,)
    form = AdminVacancyFrom
    fieldsets = (
        ('General Information', {
            'fields': (('company', 'title', 'status'), 'description')
        }),
        ('Additional Descriptions', {
            'classes': ('collapse',),
            'fields': (('salary', 'location'),)
        }),
        ('Approval', {
            'fields': ('moderation_status', 'error_text')
        }),
    )
    actions = [make_approved, make_declined]


admin.site.register(Company)
admin.site.register(HrManager)
admin.site.register(FavoriteResume)
admin.site.register(Offer)
