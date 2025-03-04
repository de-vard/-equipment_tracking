# Generated by Django 5.0.4 on 2024-05-29 19:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0007_alter_equipment_bar_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='bar_number',
            field=models.CharField(max_length=12, unique=True, validators=[django.core.validators.MinLengthValidator(12)], verbose_name='Штрих номер'),
        ),
    ]
