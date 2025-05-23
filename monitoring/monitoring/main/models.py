from django.db import models


class Ditina(models.Model):
    REGION_CHOICES = [
        ('UKR', 'Україна'),
        ('FR', 'Фрнція'),
        ('TU', 'Туреччина'),
        ('JA', 'Японія'),
        ('USA', 'США'),
    ]

    imya = models.CharField(max_length=100, verbose_name="Ім'я")
    prizvische = models.CharField(max_length=100, verbose_name='Прізвище')
    region = models.CharField(max_length=4, choices=REGION_CHOICES, verbose_name='Регіон')
    vik = models.PositiveIntegerField(verbose_name='Вік')
    zrist = models.PositiveIntegerField(verbose_name='Зріст (у см)')
    pryimaie_gormony = models.BooleanField(default=False, verbose_name='Приймає гормони')
    data_stvorennia = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    data_onovlennia = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')

    class Meta:
        verbose_name = 'Дитина'
        verbose_name_plural = 'Діти'
        ordering = ['prizvische', 'imya']

    def __str__(self):
        return f"{self.prizvische} {self.imya}"