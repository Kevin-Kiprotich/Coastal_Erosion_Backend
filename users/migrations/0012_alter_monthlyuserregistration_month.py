# Generated by Django 5.1 on 2024-11-05 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_monthlyuserregistration_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlyuserregistration',
            name='month',
            field=models.CharField(max_length=20),
        ),
    ]
