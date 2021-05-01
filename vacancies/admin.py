from django.contrib import admin
from .models import Company, Specialty, Vacancy, Application


admin.site.register(Company)
admin.site.register(Specialty)
admin.site.register(Vacancy)
admin.site.register(Application)
