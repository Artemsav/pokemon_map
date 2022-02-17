from django.db import models


class Pokemon(models.Model):
    """Покемон"""
    title = models.CharField(verbose_name='РУ Название покемона', max_length=200)
    title_en = models.CharField(verbose_name='Англ. Название покемона', max_length=200, blank=True)
    title_jp = models.CharField(verbose_name='Японск. Название покемона', max_length=200, blank=True)
    photo = models.ImageField(verbose_name='Изображение', null=True, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    element_type = models.ManyToManyField('PokemonElementType', verbose_name='Стихия', related_name='element_type')
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL,
                                           null=True,
                                           blank=True,
                                           related_name='next_evolution',
                                           verbose_name='Предыдущая эволюция',
                                           )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    """Основные характеристике покемона, в т.ч. его расположение на карте"""
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='pokemon_characteristic', verbose_name='Покемон')
    appeared_at = models.DateTimeField(verbose_name='Появился', null=True, blank=True)
    disappeared_at = models.DateTimeField(verbose_name='Исчезнет', null=True, blank=True)
    level = models.IntegerField(verbose_name='Уровень', null=True, blank=True)
    health = models.IntegerField(verbose_name='Здоровье', null=True, blank=True)
    strength = models.IntegerField(verbose_name='Сила', null=True, blank=True)
    defence = models.IntegerField(verbose_name='Защита', null=True, blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', null=True, blank=True)


class PokemonElementType(models.Model):
    """Стихии покемонов"""
    title = models.CharField(verbose_name='Стихия', max_length=200)

    def __str__(self):
        return self.title
