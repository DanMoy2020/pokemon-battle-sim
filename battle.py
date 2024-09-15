# ./battle.py
from pokemon_battle_sim.fetch_pokemon import get_pokemon_data
from pokemon_battle_sim.calculate_moves import select_moves, calculate_move_damage
import random

def run_turn(attacker, defender):
    """Run one turn for the attacker to hit the defender."""
    # Attacker selects a random move
    move = random.choice(attacker['moves'])
    damage, crit, effectiveness = calculate_move_damage(attacker, defender, move)

    # Apply damage to the defender's HP
    defender['current_hp'] -= damage
    print(f"{attacker['name'].capitalize()} uses {move['name'].capitalize()}!")
    if crit:
        print("A critical hit!")
    if effectiveness != 1:
            print(f"It's {('super effective!' if effectiveness > 1 else 'not very effective...')}")
    print(f"{attacker['name'].capitalize()} deals {damage} damage!")
    print(f"{defender['name'].capitalize()} has {max(defender['current_hp'], 0)} HP left.")

    # Check if the defender has fainted
    if defender['current_hp'] <= 0:
        print(f"{defender['name'].capitalize()} fainted! {attacker['name'].capitalize()} wins!")
        return True  # Defender fainted, battle ends
    return False  # Continue battle

def battle(pokemon1, pokemon2):
    """Simulate a battle between two Pokémon using an array and alternating turns."""
    # Store both Pokémon in an array, alternating turns by iterating through the array
    active_pokemon = [
        {'name': pokemon1['name'], 'stats': pokemon1['stats'], 'types': pokemon1['types'], 'moves': pokemon1['moves'], 'current_hp': pokemon1['stats']['hp']},
        {'name': pokemon2['name'], 'stats': pokemon2['stats'], 'types': pokemon2['types'], 'moves': pokemon2['moves'], 'current_hp': pokemon2['stats']['hp']}
    ]
    
    print(f"Battle Start: {pokemon1['name'].capitalize()} vs {pokemon2['name'].capitalize()}")

    turn = 0
    while all(pokemon['current_hp'] > 0 for pokemon in active_pokemon):
        attacker = active_pokemon[turn % 2]
        defender = active_pokemon[(turn + 1) % 2]
        
        if turn % 2 == 0:
            print(f"\nTurn {(turn + 1) // 2 + 1}!")
            
        if run_turn(attacker, defender):
            return attacker['name']  # Battle ends when someone faints
        
        turn += 1
        
if __name__ == "__main__":
    pokemon1_name = input("Enter the name of the first Pokémon: ").strip().lower()
    pokemon2_name = input("Enter the name of the second Pokémon: ").strip().lower()

    pokemon1 = get_pokemon_data(pokemon1_name)
    pokemon2 = get_pokemon_data(pokemon2_name)

    if pokemon1 and pokemon2:
        # Select 4 moves for each Pokémon
        pokemon1['moves'] = select_moves(pokemon1)
        pokemon2['moves'] = select_moves(pokemon2)
        print (pokemon1['moves'])

        if len(pokemon1['moves']) == 4 and len(pokemon2['moves']) == 4:
            # Start the battle
            winner = battle(pokemon1, pokemon2)
            print(f"\nThe winner is {winner.capitalize()}!")
        else:
            print("One or both Pokémon do not have enough valid moves.")

