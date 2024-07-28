from django.contrib.auth.models import AbstractUser
from django.db import models

from post_office.models import PostOffice


class CustomUser(AbstractUser):
    CHOICE = (
        (None, 'Выберите должность'),
        ('a', 'Инженер Электроник'),
        ('b', 'Инженер програмист'),
        ('c', 'Начальник ОПС')
    )
    job_title = models.CharField('Должность: ', choices=CHOICE, max_length=1)
    department = models.ForeignKey(
        PostOffice,
        on_delete=models.PROTECT,
        verbose_name="в каком отделе работает сотрудник",
        related_name="worker",
        blank=True,  # Позволяет оставить поле пустым в формах
        null=True  # Позволяет хранить NULL в базе данных
    )


