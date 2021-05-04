# Generated by Django 3.2 on 2021-05-04 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0008_auto_20210504_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='grade',
            field=models.CharField(choices=[('Стажер', 'Стажер'), ('Джуниор', 'Джуниор'), ('Мидл', 'Мидл'), ('Синьор', 'Синьор'), ('Лид', 'Лид')], max_length=200, null=True, verbose_name='Квалификация'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='status',
            field=models.CharField(choices=[('Не ищу работу', 'Не ищу работу'), ('Рассматриваю предложения', 'Рассматриваю предложения'), ('Ищу работу', 'Ищу работу')], max_length=200, null=True, verbose_name='Статус'),
        ),
    ]