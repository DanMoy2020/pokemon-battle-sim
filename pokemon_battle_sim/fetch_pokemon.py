# ./pokemon_battle_sim/fetch_pokemon.py
import requests

def get_pokemon_data(pokemon_name):
    """Fetch the Pokémon's basic data and a list of available moves."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        available_moves = [move['move']['name'] for move in data['moves']]

        return {
            'name': data['name'],
            'stats': {stat['stat']['name']: stat['base_stat'] for stat in data['stats']},
            'available_moves': available_moves
        }
    else:
        print(f"Error: Could not find data for {pokemon_name}")
        return None
