# Generated by Django 4.2.1 on 2024-04-20 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_appuser_institution_alter_appuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='sector',
            field=models.CharField(max_length=40, null=True),
        ),
    ]