# ./pokemon_selector.py
import tkinter as tk
from tkinter import ttk
from pokemon.fetch_pokemon import get_pokemon_data, get_pokemon_list
from pokemon.calculate_moves import get_move_data
from pokemon.battle import battle

class PokemonGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokémon Battle Simulator")

        self.num_pokemon = 2

        # Create a list of frames for Pokémon and moves
        self.pokemon_frames = []
        self.pokemon_select_vars = []
        self.move_select_vars = []
        self.pokemon_data = []
        self.pokemon_comboboxes = []
        self.move_comboboxes = {}

        self.create_pokemon_selection()

        self.start_button = ttk.Button(self.root, text="Start Battle", command=self.start_battle)
        self.start_button.grid(row=2 * self.num_pokemon + 1, column=0, padx=10, pady=10, columnspan=2)

        self.load_pokemon_list()

    def create_pokemon_selection(self):
        """Dynamically create the Pokémon and move selection UI for both sides."""
        for i in range(self.num_pokemon):
            # Frame for Pokémon
            pokemon_frame = ttk.LabelFrame(self.root, text=f"Pokémon {i + 1} - Team {i%2 + 1}")
            pokemon_frame.grid(row=(i//2), column=(i%2), padx=10, pady=10)

            # Create variables for Pokémon selection
            pokemon_name = tk.StringVar()

            pokemon_select = ttk.Combobox(pokemon_frame, textvariable=pokemon_name)
            pokemon_select.grid(row=0, column=0, padx=10, pady=10)

            # Create move selection for both Pokémon (4 moves each)
            moves = [ttk.Combobox(pokemon_frame) for _ in range(4)]

            for j, move_combobox in enumerate(moves):
                move_combobox.grid(row=j + 1, column=0, padx=10, pady=5)
                
            # Button to fetch moves after Pokémon selection
            get_moves_button = ttk.Button(pokemon_frame, text="Fetch Moves", command=lambda f=pokemon_frame: self.load_moves(f))
            get_moves_button.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
            
            self.move_comboboxes[pokemon_frame] = moves
            self.pokemon_comboboxes.append((pokemon_select))
            self.pokemon_frames.append((pokemon_frame))
            self.pokemon_select_vars.append((pokemon_name))
            self.move_select_vars.append((moves))

    def load_pokemon_list(self):
        """Fetch the list of Pokémon from the API and populate dropdowns."""
        pokemon_list = get_pokemon_list()

        if pokemon_list:
            for pokemon_frame in self.pokemon_frames:
                # Find the Combobox in each frame and set the 'values' attribute
                pokemon_combobox = pokemon_frame.children['!combobox']
                pokemon_combobox['values'] = pokemon_list
                
        else:
            print("Failed to load Pokémon list")


    def load_moves(self, frame):
        """Load available moves for each selected Pokémon."""           
        # Get the Pokémon combobox from the frame's children
        pokemon_combobox = frame.children['!combobox']
        pokemon_name = pokemon_combobox.get().lower()

        if not pokemon_name:
            print("No Pokémon selected.")
            return

        # Fetch Pokémon data
        pokemon_data = get_pokemon_data(pokemon_name)

        if pokemon_data:
            available_moves = pokemon_data['available_moves']

            # Update the move comboboxes stored for this frame with available moves
            move_comboboxes = self.move_comboboxes[frame]
            for move_combobox in move_comboboxes:
                move_combobox['values'] = available_moves
        else:
            print(f"Failed to load moves for {pokemon_name}")

    def start_battle(self):
        """Start the battle simulation based on selected Pokémon and moves."""
        team1_data = []
        team2_data = []

        for i, frame in enumerate(self.pokemon_frames):
            # Get the Pokémon name from the combobox in the current frame
            pokemon_combobox = frame.children['!combobox']
            pokemon_name = pokemon_combobox.get().lower()

            if not pokemon_name:
                print("Please select valid Pokémon.")
                return

            # Fetch Pokémon data
            pokemon_data = get_pokemon_data(pokemon_name)
            if not pokemon_data:
                print(f"Failed to load data for {pokemon_name}")
                return

            move_comboboxes = self.move_comboboxes[frame]
            pokemon_moves = []
            for move_combobox in move_comboboxes:
                move = move_combobox.get()
                if move:
                    pokemon_moves.append(get_move_data(move))

            # Ensure 4 moves are selected
            if len(pokemon_moves) != 4:
                print(f"Please select 4 moves for {pokemon_name}.")
                return

            # Assign moves to the Pokémon data
            pokemon_data['moves'] = pokemon_moves

            # Split teams: team1 for Pokémon in frames with even index, team2 for odd
            if i % 2 == 0:
                team1_data.append(pokemon_data)
            else:
                team2_data.append(pokemon_data)

        # Ensure each team has Pokémon
        if not team1_data or not team2_data:
            print("Please select Pokémon for both teams.")
            return

        # Run the battle simulation (currently only for 1v1)
        winner = battle(team1_data[0], team2_data[0])
        print(f"\nThe winner is {winner.capitalize()}!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonGUI(root)
    root.mainloop()
