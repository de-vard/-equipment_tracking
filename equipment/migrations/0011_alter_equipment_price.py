# Generated by Django 5.0.4 on 2024-06-08 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0010_alter_equipment_bar_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='ценна'),
        ),
    ]
