# ./pokemon_battle_sim/calculate_moves.py
import random, requests

def get_move_data(move_name):
    """Fetch details about a specific move from the PokeAPI."""
    url = f"https://pokeapi.co/api/v2/move/{move_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        move_data = response.json()
        return {
            'name': move_data['name'],
            'power': move_data['power'],
            'accuracy': move_data['accuracy'],
            'type': move_data['type']['name']
        }
    else:
        return None

def select_moves(pokemon):
    """Select 4 random moves for the Pokémon from its available move pool."""
    if len(pokemon['available_moves']) < 4:
        moves = pokemon['available_moves']  # In case it has less than 4 moves
    else:
        moves = random.sample(pokemon['available_moves'], 4)  # Randomly select 4 moves

    move_details = []
    for move in moves:
        move_data = get_move_data(move)
        move_details.append(move_data)
    
    return move_details

def calculate_move_damage(attacker, defender, move):
    """Calculate damage based on the move's power and attack/defense stats."""
    attack_stat = attacker['stats']['attack']
    defense_stat = defender['stats']['defense']
    
    move_power = move['power'] if move['power'] is not None else 0

    # Base damage formula (simplified)
    base_damage = (move_power * attack_stat / defense_stat) / 50 + 2
    
    # Introduce randomness to simulate variable damage (e.g., crits, etc.)
    damage = random.randint(int(base_damage * 0.85), int(base_damage * 1.15))
    
    return damage
