from django.shortcuts import render
from django.views import View

from .models import Specialty, Company, Vacancy


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.all()
        companies = Company.objects.all()
        context = {'specialties': specialties, 'companies': companies}
        return render(request, 'vacancies/index.html', context)


class VacanciesView(View):
    def get(self, request):
        vacancies = Vacancy.objects.all()
        context = {'vacancies': vacancies}
        return render(request, 'vacancies/vacancies.html', context)


class CategoryView(View):
    def get(self, request, category):
        return render(request, 'vacancies/vacancies.html')


class CompanyView(View):
    def get(self, request, id):
        return render(request, 'vacancies/company.html')


class VacancyView(View):
    def get(self, request, id):
        return render(request, 'vacancies/vacancy.html')