import json
from colorama import Fore, init
import pandas as pd

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

# Extract the 'platforms' information for all games
for game in game_data:
    game_name = game.get('name')
    game_platforms = game.get('platforms')
    if game_name and game_platforms:
        for platform in game_platforms:
            id = platform['platform']['id']
            platform_name = platform['platform']['name']
            game_counts = platform['platform']['games_count']
            year_start = platform['platform']['year_start']
            year_end = platform['platform']['year_end']
            release_date = platform['released_at']
            requirements = platform['requirements_en']
            extracted_data.append({
                'id': id,
                'Game Name': game_name,
                'Platform Name': platform_name,
                'Year Start': year_start,
                'Year End': year_end,
                'Games Count': game_counts,
                'Release': release_date,
                "System Requirements": requirements
            })

# Create a DataFrame from the extracted data
result_df = pd.DataFrame(extracted_data)
csv_file = 'platform_data.csv'

result_df.to_csv(csv_file, index=False)
# Print the resulting DataFrame
print(result_df)
