import json

from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, FormView, DetailView, DeleteView

from employee_app.forms.EmployeeResumeForm import EmployeeResumeForm
from employee_app.models import Employee, Resume, Experience, Education, Courses


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


class EmployeeProfileResumeView(ListView):
    template_name = 'employee_app/profile_resumes.html'
    context_object_name = 'resumes'

    def get_queryset(self):
        return Resume.objects.filter(employee_id=self.request.user.id)


@method_decorator(csrf_exempt, name='dispatch')
class ResumeCreationView(FormView):
    template_name = 'employee_app/resume_create.html'
    form_class = EmployeeResumeForm
    extra_context = {
        'title': 'Создание резюме',
    }
    success_url = reverse_lazy('employee:profile_resumes')

    def get(self, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        employee = Employee.objects.get(user_id=self.request.user.id)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if 'id' in body:
            resume = None
            print('never')
            # resume = Resume.objects.get(id=body['id'])
            # resume.title = body['title']
            # resume.status = body['status']
        else:
            resume = Resume(
                title=body['title'],
                status=body['status'],
                employee=employee
            )
        resume.save()
        for key in body['fields']:
            for value in body["fields"][key]:
                # if 'id' in value:
                # model = apps.get_model('employee_app', key.capitalize())(id=value['id'], **value)
                # else:
                model = apps.get_model('employee_app', key.capitalize())(
                    **value,
                    resume=resume
                )
                model.save()
        return JsonResponse([], safe=False)


class ResumeDetailView(DetailView):
    template_name = 'employee_app/resume_detail.html'
    queryset = Resume.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume_id = self.get_object().id
        context['title'] = self.get_object().title
        context['experiencies'] = Experience.objects.filter(resume_id=resume_id)
        context['educations'] = Education.objects.filter(resume_id=resume_id)
        context['courses'] = Courses.objects.filter(resume_id=resume_id)
        return context


class ResumeDeleteView(DeleteView):
    model = Resume
    template_name = 'employee_app/resume_delete.html'
    context_object_name = 'resume'
    success_url = reverse_lazy('employee:profile_resumes')
