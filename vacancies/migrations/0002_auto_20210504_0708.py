# Generated by Django 3.2 on 2021-05-04 07:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vacancies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='written_cover_letter',
            field=models.TextField(blank=True, null=True, verbose_name='Сопроводительное письмо'),
        ),
        migrations.AlterField(
            model_name='application',
            name='written_phone',
            field=models.CharField(max_length=200, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='application',
            name='written_username',
            field=models.CharField(max_length=200, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='company',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='company',
            name='employee_count',
            field=models.IntegerField(verbose_name='Количество сотрудников'),
        ),
        migrations.AlterField(
            model_name='company',
            name='location',
            field=models.CharField(max_length=100, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, default='company_images/default.gif', upload_to='company_images', verbose_name='Логотип'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='company',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='owner_of_company', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание вакансии'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='salary_from',
            field=models.IntegerField(blank=True, null=True, verbose_name='Зарплата от'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='salary_to',
            field=models.IntegerField(blank=True, null=True, verbose_name='Зарплата до'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='skills',
            field=models.TextField(blank=True, null=True, verbose_name='Навыки'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='specialty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='vacancies.specialty', verbose_name='Специализация'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название вакансии'),
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя')),
                ('surname', models.CharField(max_length=200, verbose_name='Фамилия')),
                ('salary', models.IntegerField(blank=True, null=True, verbose_name='Ожидаемая зарплата')),
                ('education', models.TextField(verbose_name='Образование')),
                ('experience', models.TextField(verbose_name='Опыт работы')),
                ('portfolio', models.FileField(blank=True, upload_to='company_images', verbose_name='Портфолио')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resumes', to='vacancies.specialty', verbose_name='Специализация')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='resumes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
