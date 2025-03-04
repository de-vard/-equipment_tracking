# Generated by Django 5.0.4 on 2024-04-07 17:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0001_initial'),
        ('post_office', '0003_alter_postoffice_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipment',
            options={'verbose_name': 'Оборудование', 'verbose_name_plural': 'Оборудования'},
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='movement_history',
        ),
        migrations.AlterField(
            model_name='equipment',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='locations', to='post_office.postoffice', verbose_name='какому опс/отделу пренадлежит'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='ценна'),
        ),
        migrations.CreateModel(
            name='MovementHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movement_history', to='equipment.equipment', verbose_name='техника')),
                ('from_where', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='from_where_equipment', to='post_office.postoffice', verbose_name='с откуда')),
                ('where', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='equipment_is_now', to='post_office.postoffice', verbose_name='куда')),
                ('who_moved', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='кто перемещал технику')),
            ],
        ),
    ]
