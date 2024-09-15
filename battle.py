# ./battle.py
from pokemon_battle_sim.fetch_pokemon import get_pokemon_data
from pokemon_battle_sim.calculate_moves import select_moves, calculate_move_damage
import random

def battle(pokemon1, pokemon2, pokemon1_moves, pokemon2_moves):
    """Simulate a battle between two Pokémon with their selected moves."""
    pokemon1_hp = pokemon1['stats']['hp']
    pokemon2_hp = pokemon2['stats']['hp']
    
    print(f"Battle Start: {pokemon1['name'].capitalize()} vs {pokemon2['name'].capitalize()}")

    turn = 0
    while pokemon1_hp > 0 and pokemon2_hp > 0:
        turn += 1
        print(f"\nTurn {turn}!")
        
        # Pokémon 1 randomly selects a move
        move1 = random.choice(pokemon1_moves)
        damage = calculate_move_damage(pokemon1, pokemon2, move1)
        pokemon2_hp -= damage
        print(f"{pokemon1['name'].capitalize()} uses {move1['name'].capitalize()} and deals {damage} damage!")
        print(f"{pokemon2['name'].capitalize()} has {max(pokemon2_hp, 0)} HP left.")
        
        # Check if Pokémon 2 fainted
        if pokemon2_hp <= 0:
            print(f"{pokemon2['name'].capitalize()} fainted! {pokemon1['name'].capitalize()} wins!")
            return pokemon1['name']
        
        # Pokémon 2 randomly selects a move
        move2 = random.choice(pokemon2_moves)
        damage = calculate_move_damage(pokemon2, pokemon1, move2)
        pokemon1_hp -= damage
        print(f"{pokemon2['name'].capitalize()} uses {move2['name'].capitalize()} and deals {damage} damage!")
        print(f"{pokemon1['name'].capitalize()} has {max(pokemon1_hp, 0)} HP left.")
        
        # Check if Pokémon 1 fainted
        if pokemon1_hp <= 0:
            print(f"{pokemon1['name'].capitalize()} fainted! {pokemon2['name'].capitalize()} wins!")
            return pokemon2['name']

if __name__ == "__main__":
    pokemon1_name = input("Enter the name of the first Pokémon: ").strip().lower()
    pokemon2_name = input("Enter the name of the second Pokémon: ").strip().lower()

    pokemon1 = get_pokemon_data(pokemon1_name)
    pokemon2 = get_pokemon_data(pokemon2_name)

    if pokemon1 and pokemon2:
        # Select 4 moves for each Pokémon
        pokemon1_moves = select_moves(pokemon1)
        pokemon2_moves = select_moves(pokemon2)
        print (pokemon1_moves)

        if len(pokemon1_moves) == 4 and len(pokemon2_moves) == 4:
            # Start the battle
            winner = battle(pokemon1, pokemon2, pokemon1_moves, pokemon2_moves)
            print(f"\nThe winner is {winner.capitalize()}!")
        else:
            print("One or both Pokémon do not have enough valid moves.")

