# Generated by Django 3.1.14 on 2022-02-17 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0011_pokemonelementtype_strong_against'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonelementtype',
            name='strong_against',
            field=models.ManyToManyField(to='pokemon_entities.PokemonElementType', verbose_name='Силен против'),
        ),
    ]
