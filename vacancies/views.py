from django.shortcuts import render
from django.views import View

from .models import Specialty, Company, Vacancy


class MainView(View):
    
    def comp_counter(self):
        # подсчитываем количество вакансий у каждой компании
        # и возвращаем все компании и количество вакансий у этих компаний
        companies = Company.objects.all()
        comp_count = {}
        
        for company in companies:
            comp_count[company.id] = Vacancy.objects.filter(company=company.id).count()   
        
        return comp_count, companies
    
    def spec_counter(self):
        # подсчитываем количество вакансий в каждой категории
        # и возвращаем все специализации и количество вакансий у этих специализация
        specialties = Specialty.objects.all()
        spec_count = {}

        for specialty in specialties:
            spec_count[specialty.code] = Vacancy.objects.filter(specialty=specialty.code).count()
        
        return spec_count, specialties


    def get(self, request):
        comp_count, companies = MainView.comp_counter(self)
        spec_count, specialties = MainView.spec_counter(self)

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
        category = Specialty.objects.get(code=category)
        context = {'vacancies': vacancies, 'category': category}
        return render(request, 'vacancies/vacancies.html', context)


class CompanyView(View):
    def get(self, request, id):
        company = Company.objects.get(id=id)
        # получаем нужные нам вакансии у компании по id
        vacancies = Vacancy.objects.filter(company=id)
        # получаем количество вакансий у компании по id
        comp_count = MainView.comp_counter(self)[0][id]
                
        context = {'company': company, 'vacancies': vacancies, 'comp_count': comp_count}
        return render(request, 'vacancies/company.html', context)


class VacancyView(View):
    def get(self, request, id):
        return render(request, 'vacancies/vacancy.html')