# Generated by Django 5.0.4 on 2024-04-07 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_department'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='mistake_in',
            new_name='job_title',
        ),
    ]