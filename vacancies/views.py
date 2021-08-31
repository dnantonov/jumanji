from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import ListView
from django.db.models import Q

from django.http import HttpResponseNotFound, HttpResponseServerError
from django.core.exceptions import ObjectDoesNotExist

from .models import Specialty, Company, Vacancy, Application, Resume
from .forms import ApplicationForm, CompanyForm, VacancyForm, ResumeForm


class IndexView(View):
    """Index page class based view"""
    template_name = 'vacancies/index.html'

    def get(self, request):
        specialties = Specialty.objects.all()
        companies = Company.objects.all()
        context = {
            'specialties': specialties,
            'companies': companies,
        }
        return render(request, self.template_name, context)


class VacanciesView(View):
    """All vacancies class based view"""
    template_name = 'vacancies/vacancies.html'

    def get(self, request):
        vacancies = Vacancy.objects.all()
        paginator = Paginator(vacancies, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'vacancies': vacancies, 'page_obj': page_obj}
        return render(request, self.template_name, context)


class CategoryView(View):
    """Vacancies by category class based view"""
    template_name = 'vacancies/vacancies.html'

    def get(self, request, category):
        vacancies = Vacancy.objects.filter(specialty=category)
        category = Specialty.objects.get(code=category)
        paginator = Paginator(vacancies, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'vacancies': vacancies, 'category': category, 'page_obj': page_obj}
        return render(request, self.template_name, context)


class CompanyView(View):
    """Company page class based view"""
    template_name = 'vacancies/company.html'

    def get(self, request, company_id):
        company = Company.objects.get(id=company_id)
        vacancies = Vacancy.objects.filter(company=company_id)
        context = {
            'company': company,
            'vacancies': vacancies,
        }
        return render(request, self.template_name, context)


class VacancyView(View):
    """Vacancy page class based view"""
    template_name = 'vacancies/vacancy.html'
    form_class = ApplicationForm

    def get(self, request, vacancy_id):
        form = self.form_class
        vacancy = Vacancy.objects.get(id=vacancy_id)
        context = {'vacancy': vacancy, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, vacancy_id):
        success_url = f'/vacancies/{vacancy_id}/send'
        form = self.form_class(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.vacancy = Vacancy.objects.get(id=vacancy_id)
            application.save()
            return redirect(success_url)


class SendApplicationView(View):
    """Send application page class based view"""
    template_name = 'vacancies/sent.html'

    def get(self, request, vacancy_id):
        context = {'id': vacancy_id}
        return render(request, self.template_name, context)


class MyCompanyView(View):
    """My Company profile class based view"""
    company_edit_template_name = 'vacancies/company-edit.html'
    company_create_template_name = 'vacancies/company-create.html'
    form_class = CompanyForm

    def get(self, request):
        form = self.form_class
        try:
            company = Company.objects.get(owner=request.user)
            context = {'company': company, 'form': form}
            return render(request, self.company_edit_template_name, context)
        except ObjectDoesNotExist:
            return render(request, self.company_create_template_name)

    def post(self, request):
        instance = Company.objects.get(owner=request.user)
        form = self.form_class(request.POST or None, instance=instance)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            messages.success(request, 'Информация о компании обновлена')
            return redirect(self.request.path_info)
        return render(request, self.company_edit_template_name)


class MyCompanyEditView(View):
    """My Company create new profile class based view"""

    def get(self, request):
        Company.objects.create(
            name="Название вашей компании",
            employee_count=0,
            location="Челябинск",
            description="Описание компании",
            owner=request.user)
        return redirect('mycompany')


class MyCompanyVacanciesView(View):
    """My Company vacancies class based view"""
    template_name = 'vacancies/vacancy-list.html'

    def get(self, request):
        company = Company.objects.get(owner=request.user)
        vacancies = Vacancy.objects.filter(company=company)
        all_vac = Vacancy.objects.all().count()
        context = {'vacancies': vacancies, 'all_vac': all_vac}
        return render(request, self.template_name, context)


class MyCompanyVacancyView(View):
    """The company edit vacancy class based view"""
    template_name = 'vacancies/vacancy-edit.html'
    form_class = VacancyForm

    def get(self, request, vacancy_id):
        form = self.form_class
        company = Company.objects.get(owner=request.user)
        specialties = Specialty.objects.all()
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except ObjectDoesNotExist:
            vacancy = Vacancy.objects.create(
                id=vacancy_id,
                title="Название вакансии",
                salary_from=10000,
                salary_to=20000,
                specialty=Specialty.objects.get(code="backend"),
                company=company,
            )
        applications = Application.objects.filter(vacancy=vacancy)
        context = {
            'vacancy': vacancy,
            'form': form,
            'specialties': specialties,
            'applications': applications
        }
        return render(request, self.template_name, context)

    def post(self, request, vacancy_id):
        instance = Vacancy.objects.get(id=vacancy_id)
        form = self.form_class(request.POST or None, instance=instance)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.company = Company.objects.get(owner=request.user)
            vacancy.save()
            messages.success(request, 'Вакансия обновлена')
            return redirect(self.request.path_info)
        return render(request, self.template_name)


class SearchView(ListView, View):
    """Search vacancy class based view"""
    template_name = 'vacancies/search.html'

    def get(self, request):
        query = self.request.GET.get('q')
        object_list = Vacancy.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        context = {'object_list': object_list, 'query': query}
        return render(request, self.template_name, context)


class MyResumeView(View):
    """My Resume class based view"""
    resume_edit_template_name = 'vacancies/resume-edit.html'
    resume_create_template_name = 'vacancies/resume-create.html'
    form_class = ResumeForm

    def get(self, request):
        form = self.form_class
        specialties = Specialty.objects.all()
        try:
            resume = Resume.objects.get(user=request.user)
            context = {
                'resume': resume,
                'form': form,
                'specialties': specialties
            }
            return render(request, self.resume_edit_template_name, context)
        except ObjectDoesNotExist:
            return render(request, self.resume_create_template_name)

    def post(self, request):
        instance = Resume.objects.get(user=request.user)
        form = self.form_class(request.POST or None, instance=instance)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            messages.success(request, 'Ваше резюме обновлено!')
            return redirect(self.request.path_info)
        return render(request, self.resume_edit_template_name)


class MyResumeCreateView(View):
    """My New Resume class based view"""

    def get(self, request):
        Resume.objects.create(
                user=request.user,
                specialty=Specialty.objects.get(code='backend'),
                name="Имя",
                surname="Фамилия"
        )
        return redirect('myresume')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена!')


def custom_handler500(request):
    return HttpResponseServerError('Сервер не доступен!')
