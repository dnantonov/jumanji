# Generated by Django 3.2 on 2021-05-04 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0002_auto_20210504_0708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
