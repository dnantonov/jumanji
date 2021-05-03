from django.db import models
from django.contrib.auth.models import User

from jumanji.settings import MEDIA_COMPANY_IMAGE_DIR, \
                             MEDIA_SPECIALITY_IMAGE_DIR


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, blank=True,
                             default='company_images/default.gif')
    employee_count = models.IntegerField()
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

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
    title = models.CharField(max_length=200)
    specialty = models.ForeignKey(Specialty,
                                  on_delete=models.CASCADE,
                                  related_name="vacancies")
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                related_name="vacancies")
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    skills = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "вакансия"
        verbose_name_plural = "вакансии"

    def __str__(self):
        return self.title


class Application(models.Model):
    id = models.AutoField(primary_key=True)
    written_username = models.CharField(max_length=200)
    written_phone = models.CharField(max_length=200)
    written_cover_letter = models.TextField(blank=True, null=True)
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
        return 'Отклик на вакансию ' + self.vacancy.title
