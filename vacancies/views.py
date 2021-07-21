from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import ListView
from django.db.models import Q

from django.http import HttpResponseNotFound, HttpResponseServerError
from django.core.exceptions import ObjectDoesNotExist

from .models import Specialty, Company, Vacancy, Application, Resume
from .forms import ApplicationForm, CompanyForm, VacancyForm, ResumeForm


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
            return redirect(success_url)


class SendApplicationView(View):
    # CBS для отправки заявки
    def get(self, request, id):
        context = {'id': id}
        return render(request, 'vacancies/sent.html', context)


class MyCompanyView(View):
    # CBS для отображения страницы редактирования компании
    def get(self, request):
        form = CompanyForm
        try:
            company = Company.objects.get(owner=request.user)
            context = {'company': company, 'form': form}
            return render(request, 'vacancies/company-edit.html', context)
        except ObjectDoesNotExist:
            return render(request, 'vacancies/company-create.html')

    def post(self, request):
        instance = Company.objects.get(owner=request.user)
        form = CompanyForm(request.POST or None, instance=instance)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            messages.success(request, 'Информация о компании обновлена')
            return redirect(self.request.path_info)
        return render(request, 'vacancies/company-edit.html')


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
    # CBS для отображения всех вакансий компании
    def get(self, request):
        company = Company.objects.get(owner=request.user)
        vacancies = Vacancy.objects.filter(company=company)
        all_vac = Vacancy.objects.all().count()
        context = {'vacancies': vacancies, 'all_vac': all_vac}
        return render(request, 'vacancies/vacancy-list.html', context)


class MyCompanyVacancyView(View):
    # CBS для отображения конкретной вакансии компании
    def get(self, request, id):
        form = VacancyForm
        company = Company.objects.get(owner=request.user)
        specialty = Specialty.objects.get(code="backend")
        specialties = Specialty.objects.all()
        try:
            vacancy = Vacancy.objects.get(id=id)
            applications = Application.objects.filter(vacancy=vacancy)
        except ObjectDoesNotExist:
            vacancy = Vacancy.objects.create(
                id=id,
                title="Название вакансии",
                salary_from=10000,
                salary_to=20000,
                specialty=specialty,
                company=company,
            )
        context = {
            'vacancy': vacancy,
            'form': form,
            'specialties': specialties,
            'applications': applications
        }
        return render(request, 'vacancies/vacancy-edit.html', context)

    def post(self, request, id):
        instance = Vacancy.objects.get(id=id)
        form = VacancyForm(request.POST or None, instance=instance)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.company = Company.objects.get(owner=request.user)
            vacancy.save()
            messages.success(request, 'Вакансия обновлена')
            return redirect(self.request.path_info)
        return render(request, 'vacancies/vacancy-edit.html')


class SearchView(ListView):
    # CBS для выдачи поисковых запросов
    def get(self, request):
        query = self.request.GET.get('q')
        object_list = Vacancy.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        context = {'object_list': object_list, 'query': query}
        return render(request, 'vacancies/search.html', context)


class MyResumeView(View):
    # CBS для отображения страницы редактирования резюме
    def get(self, request):
        form = ResumeForm
        specialties = Specialty.objects.all()
        print(form)
        try:
            resume = Resume.objects.get(user=request.user)
            context = {
                'resume': resume,
                'form': form,
                'specialties': specialties
            }
            return render(request, 'vacancies/resume-edit.html', context)
        except ObjectDoesNotExist:
            return render(request, 'vacancies/resume-create.html')

    def post(self, request):
        instance = Resume.objects.get(user=request.user)
        form = ResumeForm(request.POST or None, instance=instance)
        print(form)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            messages.success(request, 'Ваше резюме обновлено!')
            return redirect(self.request.path_info)
        return render(request, 'vacancies/resume-edit.html')


class MyResumeCreateView(View):
    # CBS для создания нового резюме
    def get(self, request):
        Resume.objects.create(
                user=request.user,
                name="Имя",
                surname="Фамилия"
        )
        return redirect('myresume')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена!')


def custom_handler500(request):
    return HttpResponseServerError('Сервер не доступен!')
