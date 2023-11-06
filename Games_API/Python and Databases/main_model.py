import sqlite3
import json
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Load the JSON data from the file
try:
    with open('rawg_games.json', 'r') as json_file:
        game_data = json.load(json_file)
except FileNotFoundError:
    print(Fore.RED + "JSON file not found. Make sure it exists in the current directory.")
    exit(1)
except json.JSONDecodeError:
    print(Fore.RED + "Error decoding JSON data. Check the format of the JSON file.")
    exit(1)

# Initialize a list to store the extracted data
extracted_data = []

# Extract the specified fields for all games
for index, game in enumerate(game_data, start=1):
    game_id = game.get('id')
    game_slug = game.get('slug')
    game_name = game.get('name')
    game_released = game.get('released')
    game_tba = game.get('tba')
    game_background_image = game.get('background_image')
    game_rating = game.get('rating', None)
    game_rating_top = game.get('rating_top', None)
    game_reviews_text_count = game.get('reviews_text_count', None)
    game_metacritic = game.get('metacritic', None)
    game_playtime = game.get('playtime', None)
    game_suggestions_count = game.get('suggestions_count', None)
    game_updated = game.get('updated', None)
    game_user_game = game.get('user_game', None)
    game_reviews_count = game.get('reviews_count', None)

    # Create a dictionary with the extracted data for this game
    game_info = {
        "Index": index,
        "ID": game_id,
        "Slug": game_slug,
        "Name": game_name,
        "Released": game_released,
        "TBA": game_tba,
        "Background Image": game_background_image,
        "Rating": game_rating,
        "Rating Top": game_rating_top,
        "Reviews Text Count": game_reviews_text_count,
        "Metacritic": game_metacritic,
        "Playtime": game_playtime,
        "Suggestions Count": game_suggestions_count,
        "Updated": game_updated,
        "User Game": game_user_game,
        "Reviews Count": game_reviews_count,
    }

    # Append the game data to the list
    extracted_data.append(game_info)

# Define the box characters
horizontal_line = "─"  # U+2500
vertical_line = "│"  # U+2502
top_left_corner = "┌"  # U+250C
top_right_corner = "┐"  # U+2510
bottom_left_corner = "└"  # U+2514
bottom_right_corner = "┘"  # U+2518

# Print the extracted data with a box-like border
for game_info in extracted_data:
    index_str = str(game_info['Index'])

    if game_info['Index'] == 1:
        # Highlight index 1 with red text
        index_str = Fore.RED + index_str

    # Calculate the width of the box based on the length of the text
    box_width = len(index_str) + 2

    # Create the top border of the box
    top_border = f"{top_left_corner}{horizontal_line * box_width}{top_right_corner}"

    # Create the middle line with text and box
    middle_line = f"{vertical_line} {index_str} {vertical_line}"

    # Create the bottom border of the box
    bottom_border = f"{bottom_left_corner}{horizontal_line * box_width}{bottom_right_corner}"

    # Print the box
    print(top_border)
    print(middle_line)
    print(bottom_border)

    # Print the game information
    print(f"Game ID: {game_info['ID']}")
    print(f"Slug: {game_info['Slug']}")
    print(f"Name: {game_info['Name']}")
    print(f"Released: {game_info['Released']}")
    print(f"TBA: {game_info['TBA']}")
    print(f"Background Image: {game_info['Background Image']}")
    print(f"Rating: {game_info['Rating']}")
    print(f"Rating Top: {game_info['Rating Top']}")
    print(f"Reviews Text Count: {game_info['Reviews Text Count']}")
    print(f"Metacritic: {game_info['Metacritic']}")
    print(f"Playtime: {game_info['Playtime']}")
    print(f"Suggestions Count: {game_info['Suggestions Count']}")
    print(f"Updated: {game_info['Updated']}")
    print(f"User Game: {game_info['User Game']}")
    print(f"Reviews Count: {game_info['Reviews Count']}")

    # Add some space between boxes
    print("\n")

# SQLite database setup
conn = sqlite3.connect('game_data.db')
cursor = conn.cursor()

# Create a games table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY,
        slug TEXT,
        name TEXT,
        released TEXT,
        tba BOOLEAN,
        background_image TEXT,
        rating REAL,
        rating_top INTEGER,
        reviews_text_count INTEGER,
        metacritic INTEGER,
        playtime INTEGER,
        suggestions_count INTEGER,
        updated TEXT,
        user_game TEXT,
        reviews_count INTEGER
    )
''')

# Insert data into the games table
for game_info in extracted_data:
    cursor.execute('''
        INSERT INTO games (
            slug, name, released, tba, background_image, rating, rating_top,
            reviews_text_count, metacritic, playtime, suggestions_count,
            updated, user_game, reviews_count
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        game_info['Slug'],
        game_info['Name'],
        game_info['Released'],
        game_info['TBA'],
        game_info['Background Image'],
        game_info['Rating'],
        game_info['Rating Top'],
        game_info['Reviews Text Count'],
        game_info['Metacritic'],
        game_info['Playtime'],
        game_info['Suggestions Count'],
        game_info['Updated'],
        game_info['User Game'],
        game_info['Reviews Count'],
    ))

# Commit the changes and close the database connection
conn.commit()
conn.close()

print(Fore.GREEN + "Data successfully inserted into the database.")
