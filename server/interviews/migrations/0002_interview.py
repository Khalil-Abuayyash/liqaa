# Generated by Django 5.1.1 on 2024-09-27 14:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('status', models.CharField(default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('interviewee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interviewee', to=settings.AUTH_USER_MODEL)),
                ('interviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interviewer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
