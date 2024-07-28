import uuid

from django.db import models


class PostOffice(models.Model):
    """ Почтовое отделение или отделы
        имеющие технику на своем балансе
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('название', max_length=200)
    index = models.IntegerField('индекс почтового отделения', null=True, blank=True)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата последнего редактирования', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Почтовое отделение/отдел"
        verbose_name_plural = "Почтовые отделения/отделы"
