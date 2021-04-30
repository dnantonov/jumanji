from django.db import models
from django.contrib.auth.models import User



class Company(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    logo = models.URLField(max_length=200)
    employee_count = models.IntegerField()
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "компания"
        verbose_name_plural = "компании"

    def __str__(self):
        return self.name


class Specialty(models.Model):
    code = models.CharField(primary_key=True, max_length=64)
    name = models.CharField(max_length=100)
    picture = models.URLField(max_length=200)

    class Meta:
        verbose_name = "специализация"
        verbose_name_plural = "специализации"

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    id = models.IntegerField(primary_key=True)
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
