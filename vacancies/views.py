from django.shortcuts import render
from django.views import View

from .models import Specialty


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.all()
        
        context = {'specialties': specialties}
        return render(request, 'vacancies/index.html', context)


class VacanciesView(View):
    def get(self, request):
        return render(request, 'vacancies/vacancies.html')


class CategoryView(View):
    def get(self, request, category):
        return render(request, 'vacancies/vacancies.html')


class CompanyView(View):
    def get(self, request, id):
        return render(request, 'vacancies/company.html')


class VacancyView(View):
    def get(self, request, id):
        return render(request, 'vacancies/vacancy.html')