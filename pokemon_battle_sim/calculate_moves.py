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

def get_type_effectiveness(attacking_type, defending_type):
    """Fetch the type effectiveness (damage multiplier) from the PokeAPI."""
    url = f"https://pokeapi.co/api/v2/type/{attacking_type}"
    response = requests.get(url)
    
    if response.status_code == 200:
        type_data = response.json()
        
        # Relations for damage multiplier
        no_damage_to = [type_info['name'] for type_info in type_data['damage_relations']['no_damage_to']]
        half_damage_to = [type_info['name'] for type_info in type_data['damage_relations']['half_damage_to']]
        double_damage_to = [type_info['name'] for type_info in type_data['damage_relations']['double_damage_to']]

        if defending_type in no_damage_to:
            return 0.0
        elif defending_type in half_damage_to:
            return 0.5
        elif defending_type in double_damage_to:
            return 2.0
        else:
            return 1.0
    else:
        return 1.0
    
def calculate_move_damage(attacker, defender, move):
    """Calculate damage based on the move's power and attack/defense stats."""
    attack_stat = attacker['stats']['attack']
    defense_stat = defender['stats']['defense']
    
    move_power = move['power'] if move['power'] is not None else 0
    
    # Type effectiveness: Get multiplier based on defender's type(s)
    effectiveness = 1.0
    for defender_type in defender['types']:
        effectiveness *= get_type_effectiveness(move['type'], defender_type)
        
    if move_power == 0:
        return 0, False, effectiveness

    # STAB (Same Type Attack Bonus): 1.5x if move type matches one of attacker's types
    stab = 1.5 if move['type'] in attacker['types'] else 1.0
    
    # Critical hit chance (6.25% chance)
    critical_hit = 2.0 if random.random() < 0.0625 else 1.0
    
    # Base damage formula (simplified)
    base_damage = (((2 * attack_stat * move_power / defense_stat) / 50) + 2) * stab * effectiveness * critical_hit
    
    # Introduce randomness to simulate variable damage (85% - 100%)
    damage = random.randint(int(base_damage * 0.85), int(base_damage * 1.0))
    
    return damage, critical_hit > 1.0, effectiveness
