# Generated by Django 5.1 on 2024-11-05 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_appuser_sector'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100, unique=True)),
                ('user_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Country Statistics',
            },
        ),
        migrations.CreateModel(
            name='InstitutionCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=255, unique=True)),
                ('user_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Institution Statistics',
            },
        ),
        migrations.CreateModel(
            name='RoleCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=255, unique=True)),
                ('user_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Role Statistics',
            },
        ),
        migrations.CreateModel(
            name='SectorCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector', models.CharField(max_length=40, unique=True)),
                ('user_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Sector Statistics',
            },
        ),
        migrations.AlterModelOptions(
            name='countrystats',
            options={},
        ),
        migrations.CreateModel(
            name='MonthlyUserRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('registration_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Registration Stats',
                'unique_together': {('month', 'year')},
            },
        ),
    ]
