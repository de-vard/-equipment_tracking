# Generated by Django 5.0.4 on 2024-04-07 09:32

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostOffice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200, verbose_name='название')),
                ('index', models.IntegerField(blank=True, verbose_name='индекс почтового отделения')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата последнего редактирования')),
            ],
        ),
    ]