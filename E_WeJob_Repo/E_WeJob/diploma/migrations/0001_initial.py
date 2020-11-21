# Generated by Django 3.1.3 on 2020-11-19 23:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Diploma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diplomaTitle', models.CharField(max_length=255, verbose_name='Diploma Title')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diploma', to=settings.AUTH_USER_MODEL, verbose_name='candidate')),
            ],
        ),
    ]
