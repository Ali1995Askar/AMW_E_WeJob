# Generated by Django 3.1.3 on 2020-11-22 11:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('diploma', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Job Title')),
                ('requiredExperienceYears', models.IntegerField(verbose_name=' required experience years')),
                ('salary', models.IntegerField(verbose_name='salary')),
                ('date', models.DateField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL, verbose_name='company')),
                ('requiredEducationLevel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requiredEducationLevel', to='diploma.diploma', verbose_name='diploma')),
            ],
        ),
    ]
