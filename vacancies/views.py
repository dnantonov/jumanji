from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Count
from django.views.generic import CreateView

from django.http import HttpResponse, HttpResponseRedirect

from django.core.exceptions import ObjectDoesNotExist


from .models import Specialty, Company, Vacancy
from .forms import ApplicationForm



class MainView(View):
    # CBV для главной
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
        form = ApplicationForm
        vacancy = Vacancy.objects.get(id=id)
        context = {'vacancy': vacancy, 'form': form}
        return render(request, 'vacancies/vacancy.html', context)
    def post(self, request, id):
        success_url = f'/vacancies/{id}/send'
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.vacancy = Vacancy.objects.get(id=id)
            application.save()
            return HttpResponseRedirect(success_url)


class SendApplicationView(View):
    # CBS для отправки заявки
    def get(self, request, id):
        context = {'id': id}
        return render(request, 'vacancies/sent.html', context)


class MyCompanyView(View):
    # CBS для отображения страницы редактирования компании
    def get(self, request):
        try:
            company = Company.objects.get(owner=request.user)
            return render(request, 'vacancies/company-edit.html')
        except ObjectDoesNotExist:
            return render(request, 'vacancies/company-create.html')


class MyCompanyEditView(View):
    # CBS для создания новой компании
    def get(self, request):
            Company.objects.create(
                name="Название вашей компании",
                employee_count=0,
                location="Челябинск",
                description="Описание компании",
                owner=request.user)
            return redirect('mycompany')


class MyCompanyVacanciesView(View):
    # CBS для отображения вакансий компании
    def get(self, request):
        return render(request, 'vacancies/vacancy-list.html')


class MyCompanyVacancyView(View):
    # CBS для отображения вакансии компании
    def get(self, request, id):
        return render(request, 'vacancies/vacancy-edit.html')