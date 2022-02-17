import folium
from django.shortcuts import render, get_object_or_404

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transprevious_evolution'
)


def add_pokemon(folium_map, lat, lon, characteristic=None, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    final = ''
    for key, value in characteristic:
        final_popup = '{key}={value}\n'.format(key=key, value=value)
        final += final_popup
    folium.Marker(
        [lat, lon],
        icon=icon,
        popup=final
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)
        img_url = request.build_absolute_uri(pokemon.photo.url)
        for pokemon_entity in pokemon_entities:
            characteristic = {'level': pokemon_entity.level,
                              'health': pokemon_entity.health,
                              'strength': pokemon_entity.strength,
                              'defence': pokemon_entity.defence,
                              'stamina': pokemon_entity.stamina,
                              }
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                characteristic.items(),
                img_url,
                       )

    pokemons_on_page = []
    for pokemon in pokemons:
        img_url = request.build_absolute_uri(pokemon.photo.url)
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
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entitys = pokemon.pokemon_characteristic.all()
    for pokemon_entity in pokemon_entitys:
        characteristic = {'level': pokemon_entity.level,
                          'health': pokemon_entity.health,
                          'strength': pokemon_entity.strength,
                          'defence': pokemon_entity.defence,
                          'stamina': pokemon_entity.stamina,
                          }
        img_url = request.build_absolute_uri(pokemon.photo.url)
        add_pokemon(folium_map, pokemon_entity.lat,
                    pokemon_entity.lon,
                    characteristic.items(),
                    image_url=img_url,
                    )
    if pokemon.next_evolution.all():
        next_evolution = pokemon.next_evolution.all().first()
        next_evolution = {'pokemon_id': next_evolution.id,
                          'img_url': request.build_absolute_uri(next_evolution.photo.url),
                          'title_ru': next_evolution.title,
                          }
    else:
        next_evolution = None
    if pokemon.previous_evolution:
        previous_evolution = {'pokemon_id': pokemon.previous_evolution.id,
                              'img_url': request.build_absolute_uri(pokemon.previous_evolution.photo.url),
                              'title_ru': pokemon.previous_evolution.title,
                              }
    else:
        previous_evolution = None
    pokemons_on_page = {
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'description': pokemon.description,
            "next_evolution": next_evolution,
            "previous_evolution": previous_evolution
        }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons_on_page
    })
