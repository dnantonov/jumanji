from django.shortcuts import render
from django.views import View
from django.db.models import Count

from .models import Specialty, Company, Vacancy


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.all()
        companies = Company.objects.all()
        
        context = {
            'specialties': specialties,
            'companies': companies,
        }
        return render(request, 'vacancies/index.html', context)


class VacanciesView(View):
    # CBV для страницы со всеми вакансиями
    def get(self, request):
        vacancies = Vacancy.objects.all()
        context = {'vacancies': vacancies}
        return render(request, 'vacancies/vacancies.html', context)


class CategoryView(View):
    # CBS для страницы с вакансиями по категории
    def get(self, request, category):
        vacancies = Vacancy.objects.filter(specialty=category)
        category = Specialty.objects.get(code=category)
        context = {'vacancies': vacancies, 'category': category}
        return render(request, 'vacancies/vacancies.html', context)


class CompanyView(View):
    # CBS для страницы компании
    def get(self, request, id):
        company = Company.objects.get(id=id)
        vacancies = Vacancy.objects.filter(company=id)
        
        context = {
            'company': company,
            'vacancies': vacancies,
        }
        return render(request, 'vacancies/company.html', context)


class VacancyView(View):
    # CBS для страницы вакансии
    def get(self, request, id):
        vacancy = Vacancy.objects.get(id=id)
        context = {'vacancy': vacancy}
        return render(request, 'vacancies/vacancy.html', context)
