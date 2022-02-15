from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, null = True, blank = True)
    title_jp = models.CharField(max_length=200, null = True, blank = True)
    photo = models.ImageField(null = True, blank = True)
    description =  models.TextField(null = True, blank = True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null = True, blank = True, related_name='evolution')
    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
    level = models.IntegerField()
    health = models.IntegerField()
    strength = models.IntegerField()
    defence = models.IntegerField()
    stamina = models.IntegerField()