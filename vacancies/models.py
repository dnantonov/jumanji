from django.db import models
from django.contrib.auth.models import User

from jumanji.settings import MEDIA_COMPANY_IMAGE_DIR, \
                             MEDIA_SPECIALITY_IMAGE_DIR, \
                             MEDIA_RESUME_FILE_DIR


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Имя')
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, 
                             verbose_name='Логотип',
                             blank=True,
                             default='company_images/default.gif')
    employee_count = models.IntegerField(verbose_name='Количество сотрудников')
    location = models.CharField(max_length=100, verbose_name='Город')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    owner = models.OneToOneField(User, on_delete=models.PROTECT, related_name='owner_of_company')

    class Meta:
        verbose_name = "компания"
        verbose_name_plural = "компании"

    def __str__(self):
        return self.name


class Specialty(models.Model):
    code = models.CharField(primary_key=True, max_length=64)
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    class Meta:
        verbose_name = "специализация"
        verbose_name_plural = "специализации"

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name='Название вакансии')
    specialty = models.ForeignKey(Specialty,
                                  on_delete=models.CASCADE,
                                  related_name="vacancies",
                                  verbose_name='Специализация')
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                related_name="vacancies")
    salary_from = models.IntegerField(blank=True, null=True, verbose_name='Зарплата от')
    salary_to = models.IntegerField(blank=True, null=True, verbose_name='Зарплата до')
    published_at = models.DateTimeField(auto_now_add=True)
    skills = models.TextField(blank=True, null=True, verbose_name='Навыки')
    description = models.TextField(blank=True, null=True, verbose_name='Описание вакансии')

    class Meta:
        verbose_name = "вакансия"
        verbose_name_plural = "вакансии"

    def __str__(self):
        return self.title


class Application(models.Model):
    id = models.AutoField(primary_key=True)
    written_username = models.CharField(max_length=200, verbose_name='Имя')
    written_phone = models.CharField(max_length=200, verbose_name='Телефон')
    written_cover_letter = models.TextField(blank=True, null=True, verbose_name='Сопроводительное письмо')
    vacancy = models.ForeignKey(Vacancy,
                                on_delete=models.CASCADE,
                                related_name="applications")
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="applications",
                             to_field='username')

    class Meta:
        verbose_name = "отклик"
        verbose_name_plural = "отклики"

    def __str__(self):
        return 'Отклик на вакансию от ' + self.written_username


class Resume(models.Model):
    id = models.AutoField(primary_key=True)
    
    STATUS = (
        ('Не ищу работу', 'Не ищу работу'),
        ('Рассматриваю предложения', 'Рассматриваю предложения'),
        ('Ищу работу', 'Ищу работу'),
    )

    GRADE = (
        ('Стажер', 'Стажер'),
        ('Джуниор', 'Джуниор'),
        ('Мидл', 'Мидл'),
        ('Синьор', 'Синьор'),
        ('Лид', 'Лид'),
    )

    user = models.OneToOneField(User, 
                             on_delete=models.PROTECT,
                             related_name="resumes")
    specialty = models.ForeignKey(Specialty,
                                  on_delete=models.CASCADE,
                                  verbose_name='Специализация',
                                  related_name="resumes",
                                  default="backend")
    name = models.CharField(max_length=200, verbose_name='Имя')
    surname = models.CharField(max_length=200, verbose_name='Фамилия')
    status = models.CharField(max_length=200, null=True, choices=STATUS, verbose_name='Статус')
    salary = models.IntegerField(blank=True, null=True, verbose_name='Ожидаемая зарплата')
    education = models.TextField(verbose_name='Образование', blank=True)
    grade = models.CharField(max_length=200, null=True, choices=GRADE, verbose_name='Квалификация')
    experience = models.TextField(verbose_name='Опыт работы', blank=True)
    portfolio = models.FileField(upload_to=MEDIA_RESUME_FILE_DIR,
                                 verbose_name='Портфолио',
                                 blank=True)
    
    class Meta:
        verbose_name = "резюме"
        verbose_name_plural = "резюме"

    def __str__(self):
        return 'Резюме от ' + self.name + ' ' + self.surname
