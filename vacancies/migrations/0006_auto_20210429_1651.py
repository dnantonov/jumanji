# Generated by Django 3.1.7 on 2021-04-29 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0005_auto_20210429_1044'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'компания', 'verbose_name_plural': 'компании'},
        ),
        migrations.AlterModelOptions(
            name='specialty',
            options={'verbose_name': 'специализация', 'verbose_name_plural': 'специализации'},
        ),
        migrations.AlterModelOptions(
            name='vacancy',
            options={'verbose_name': 'вакансия', 'verbose_name_plural': 'вакансии'},
        ),
    ]
