# ./pokemon/fetch_pokemon.py
import requests

POKEAPI_URL = "https://pokeapi.co/api/v2/"

def get_pokemon_list(limit=1025):
    """Fetch a list of Pokémon names from the PokeAPI."""
    url = f"{POKEAPI_URL}pokemon?limit={limit}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        pokemon_list = [pokemon['name'] for pokemon in data['results']]
        return pokemon_list
    else:
        print("Failed to fetch Pokémon list from the API.")
        return []
    
def get_pokemon_data(pokemon_name):
    """Fetch the Pokémon's basic data, including types, stats, abilities, and moves."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        available_moves = [move['move']['name'] for move in data['moves']]
        types = [type_info['type']['name'] for type_info in data['types']]
        abilities = [ability_info['ability']['name'] for ability_info in data['abilities']]
        
        return {
            'name': data['name'],
            'stats': {stat['stat']['name']: stat['base_stat'] for stat in data['stats']},
            'available_moves': available_moves,
            'types': types,
            'abilities': abilities
        }
    else:
        print(f"Error: Could not find data for {pokemon_name}")
        return None
