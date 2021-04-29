from django.shortcuts import render
from django.views import View

from .models import Specialty, Company, Vacancy


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.all()
        companies = Company.objects.all()
        spec_count = {}
        comp_count = {}
        # подсчитываем количество вакансий в каждой категории
        for specialty in specialties:
            spec_count[specialty.code] = Vacancy.objects.filter(specialty=specialty.code).count()
        # подсчитываем количество вакансий у каждой компании
        for company in companies:
            comp_count[company.id] = Vacancy.objects.filter(company=company.id).count()
        print(comp_count.items())     
        
        context = {
            'specialties': specialties, 
            'companies': companies, 
            'spec_count': spec_count,
            'comp_count': comp_count
        }
        return render(request, 'vacancies/index.html', context)


class VacanciesView(View):
    def get(self, request):
        vacancies = Vacancy.objects.all()
        context = {'vacancies': vacancies}
        return render(request, 'vacancies/vacancies.html', context)


class CategoryView(View):
    def get(self, request, category):
        vacancies = Vacancy.objects.filter(specialty=category)
        category = Specialty.objects.get(code=category).name
        context = {'vacancies': vacancies, 'category': category}
        return render(request, 'vacancies/vacancies.html', context)


class CompanyView(View):
    def get(self, request, id):
        return render(request, 'vacancies/company.html')


class VacancyView(View):
    def get(self, request, id):
        return render(request, 'vacancies/vacancy.html')