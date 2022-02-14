import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        pokemon_entitys = PokemonEntity.objects.filter(pokemon=pokemon)
        media_photo = '/media/{pokemon_photo}'.format(pokemon_photo = str(pokemon.photo))
        img_url = request.build_absolute_uri(media_photo)
        for pokemon_entity in pokemon_entitys:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                img_url
            )

    pokemons_on_page = []
    for pokemon in pokemons:
        media_photo = '/media/{pokemon_photo}'.format(pokemon_photo = str(pokemon.photo))
        img_url = request.build_absolute_uri(media_photo)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    '''with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
        pokemons = json.load(database)['pokemons']'''
    pokemon = Pokemon.objects.get(id = pokemon_id)
    '''for pokemon in pokemons:
        if pokemon:
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')'''

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entity = PokemonEntity.objects.filter(pokemon=pokemon).first()
    media_photo = '/media/{pokemon_photo}'.format(pokemon_photo = str(pokemon.photo))
    img_url = request.build_absolute_uri(media_photo)
    print(img_url)
    add_pokemon(folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                image_url=img_url,
                )
    pokemons_on_page= {
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'description':pokemon.description
        }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons_on_page
    })
