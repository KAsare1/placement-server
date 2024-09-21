# Generated by Django 5.1.1 on 2024-09-20 14:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_type', models.CharField(choices=[('SINGLE_MAJOR', 'Single Major'), ('COMBINED_MAJOR', 'Combined Major'), ('MAJOR_MINOR', 'Major Minor')], max_length=20)),
                ('major', models.CharField(max_length=250)),
                ('second_major', models.CharField(blank=True, max_length=250, null=True)),
                ('minor', models.CharField(blank=True, max_length=250, null=True)),
                ('program', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.CharField(max_length=250)),
                ('students_id', models.CharField(max_length=250, unique=True)),
                ('results', models.CharField(max_length=100)),
                ('CGPA', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ConsiderationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Results', models.CharField(max_length=250)),
                ('CGPA', models.CharField(max_length=250)),
                ('choice', models.CharField(max_length=250)),
                ('explanation', models.CharField(max_length=1000)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Students')),
            ],
        ),
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Students')),
                ('placement', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='placement.program', verbose_name="Student's placements")),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Students')),
                ('first_choice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='first_choice_students', to='placement.program')),
                ('second_choice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second_choice_students', to='placement.program')),
                ('third_choice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='third_choice_students', to='placement.program')),
            ],
        ),
    ]
