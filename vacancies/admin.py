from django.contrib import admin
from .models import Company, Specialty, Vacancy, Application, Resume


admin.site.register(Company)
admin.site.register(Specialty)
admin.site.register(Vacancy)
admin.site.register(Application)
admin.site.register(Resume)
