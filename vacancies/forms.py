from django.forms import ModelForm

from .models import Application, Company, Vacancy, Resume


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        exclude = ['owner']


class VacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        exclude = ['company', 'published_at']
        labels = {'title': 'Название вакансии',
                  'specialty': 'Специализация',
                  'skills': 'Требуемые навыки',
                  'description': 'Описание вакансии',
                  'salary_from': 'Зарплата от',
                  'salary_to': 'Зарплата до',
                  }


class ResumeForm(ModelForm):
    class Meta:
        model = Resume
        exclude = ['user']
