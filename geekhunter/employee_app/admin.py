from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ngettext

from employee_app.forms.AdminEmployeeResumeForm import AdminEmployeeResumeForm
from employee_app.models import Resume, Employee, FavoriteVacancies, Experience, Education, Courses, Response


class EmployeeAppForReviewFilter(SimpleListFilter):
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


@admin.register(Resume)
class AdminResume(admin.ModelAdmin):
    list_display = ('title', 'moderation_status', 'status')
    list_filter = (EmployeeAppForReviewFilter,)
    form = AdminEmployeeResumeForm
    fieldsets = (
        ('General Information', {
            'fields': ('employee', 'title', 'status')
        }),
        ('Approval', {
            'fields': ('moderation_status',)
        }),
    )
    actions = [make_approved, make_declined]


@admin.register(Response)
class AdminResponse(admin.ModelAdmin):
    list_display = ('title', 'vacancy', 'status',)


admin.site.register(Employee)
admin.site.register(FavoriteVacancies)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Courses)
