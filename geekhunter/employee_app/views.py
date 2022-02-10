from django.shortcuts import render
from django.views import View

from employee_app.models import Employee


class EmployeeProfileView(View):
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile = Employee.objects.get(user_id=request.user.id)
        return super(EmployeeProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            'title': f'профиль {self.profile.user.username}',
            'employee': self.profile,
        }
        return render(request, 'employee_app/employee_profile.html', context)
