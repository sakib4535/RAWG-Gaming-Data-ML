import requests
import json


api_key = '8e4abb10a6174c3a8361dd367a604618'
base_url = 'https://api.rawg.io/api/'


endpoint = 'games'

all_games = []

page = 1

while page <= 200:  # Loop through all 200 pages
    # Define query parameters including the API key, page number, and page size
    params = {
        'key': api_key,
        'page': page,
        'page_size': 20  # Adjust the page size as needed
    }


    response = requests.get(f'{base_url}{endpoint}', params=params)


    if response.status_code == 200:
        data = response.json()
        games = data.get('results', [])


        if not games:
            break


        all_games.extend(games)


        page += 1
    else:
        print(f'Failed to retrieve data from the API. Status code: {response.status_code}')
        break


num_games_retrieved = len(all_games)
print(f"Total number of games retrieved: {num_games_retrieved}")


with open('rawg_games.json', 'w') as json_file:
    json.dump(all_games, json_file, indent=4)

print("Data saved to 'rawg_games.json'")

