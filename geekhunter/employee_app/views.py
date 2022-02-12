from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic import ListView

from company_app.models import FavoriteResume

from employee_app.models import Resume


class ResumesView(PermissionRequiredMixin, ListView):
    login_url = 'auth_app:login'
    permission_required = 'employee_app.view_resume'
    template_name = 'employee_app/resumes.html'
    extra_context = {
        'title': 'резюме',
        'favorite_resumes': 'favorite_resumes',
    }

    context_object_name = 'resumes'
    ordering = ['-updated_at']

    def get_queryset(self):
        if 'pk' in self.kwargs:
            return Resume.objects.filter(
                employee_id=self.kwargs.get('pk'),
                status='ACTIVE'
            ).order_by(*self.ordering)
        else:
            return Resume.objects.filter(status='ACTIVE').order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite_resumes'] = FavoriteResume.objects.filter(hr_manager=self.request.user.id)

        return context

