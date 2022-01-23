from django.contrib import admin

from employee_app.models import Employee, Resume, FavoriteVacancies, Experience, Education, Courses, Response

admin.site.register(Employee)
admin.site.register(Resume)
admin.site.register(FavoriteVacancies)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Courses)
admin.site.register(Response)