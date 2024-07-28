import random
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid

from post_office.models import PostOffice


class Equipment(models.Model):
    """Оборудование"""
    CHOICE = (
        (None, 'Статус техники'),
        ('a', 'В наличии'),
        ('b', 'отправленна'),
        ('c', 'потерянна')
    )
    status = models.CharField('Статус техники', choices=CHOICE, max_length=1, )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('название', max_length=200)
    price = models.DecimalField('ценна', max_digits=10, decimal_places=2, null=True, blank=True)
    manufacturer = models.CharField('производитель', max_length=200)
    inventory_number = models.BigIntegerField('инвертарный номер', unique=True)
    serial_number = models.BigIntegerField('серийный номер', unique=True)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата последнего редактирования', auto_now=True)
    photo = models.ImageField(upload_to='static/images/normal_photos/%Y/%m/%d', verbose_name='Фото')
    bar_number = models.CharField(
        "Штрих номер",
        max_length=12,
        validators=[MinLengthValidator(12)],
        unique=True,
        editable=False
    )
    department = models.ForeignKey(
        PostOffice,
        on_delete=models.PROTECT,
        verbose_name="какому опс/отделу пренадлежит",
        related_name='equipments',
    )

    def __str__(self):
        return self.title

    @staticmethod
    def generate_unique_bar_number():
        """Генерируем числа для штрих кода и проверяем его не уникальность"""
        while True:
            bar_number = ''.join(random.choices('0123456789', k=12))  # Генерируем 12-значное число
            if not Equipment.objects.filter(bar_number=bar_number).exists():
                return bar_number

    def save(self, *args, **kwargs):
        """перед сохранением обьекта, автоматически заполняем поле"""
        if self._state.adding:  # Проверяем, новый ли это объект
            self.bar_number = self.generate_unique_bar_number()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('equipment_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудования"


class MovementHistory(models.Model):
    """История перемещения техники"""
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        verbose_name="техника",
        related_name='movement_history'
    )
    from_where = models.ForeignKey(
        PostOffice,
        on_delete=models.PROTECT,
        verbose_name="с откуда техника",
        related_name='from_where_equipment',
    )
    where = models.ForeignKey(
        PostOffice,
        on_delete=models.PROTECT,
        related_name='equipment_is_now',
        verbose_name="куда техника",
    )
    who_moved = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name="кто перемещал технику")
    created = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f"Техника перемещена с: {self.from_where} в {self.where} работником {self.who_moved}"

    class Meta:
        ordering = ['-created']
