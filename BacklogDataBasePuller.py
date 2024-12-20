import requests
import pandas as pd
import time
import json
from igdb.wrapper import IGDBWrapper
from igdb.igdbapi_pb2 import GameResult

# Need to make your twitch account API integration; refer to IGDB's website for information
client_id = "enteryourclientid"
client_secret = "enteryoursecret"

# Authentication URL
auth_url = "https://id.twitch.tv/oauth2/token"

# Parameters for the POST request
params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "client_credentials"
}

# Make the POST request to get the access token
response = requests.post(auth_url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    access_token = data.get("access_token")
    expires_in = data.get("expires_in")
    token_type = data.get("token_type")
    
    # Print the results
    print(f"Access Token: {access_token}")
    print(f"Expires In: {expires_in} seconds")
    print(f"Token Type: {token_type}")
else:
    # Print the error if authentication fails
    print(f"Failed to get access token. Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    exit()

# Read the CSV file into a DataFrame
df = pd.read_csv("backlog.csv")

# Convert the 'id' column to a list of strings
id_list = df['id'].astype(str).tolist()

# Break the list into chunks to respect the API's request limit
batch_size = 10  # Number of IDs per request
id_batches = [id_list[i:i + batch_size] for i in range(0, len(id_list), batch_size)]

# With a wrapper instance already created
wrapper = IGDBWrapper(client_id, access_token)

# Function to process each batch
def fetch_game_details(batch):
    id_string = ",".join(batch)
    query = f'fields id, name, genres.name, themes.name, keywords.name, rating; where id = ({id_string});'
    try:
        # JSON API request
        byte_array = wrapper.api_request('games', query)
        response_json = json.loads(byte_array.decode('utf-8'))
        return response_json
    except Exception as e:
        print(f"Error fetching details for batch {batch}: {e}")
        return []

# Initialize a list to store all results
all_game_details = []

# Process each batch with rate limiting
for batch in id_batches:
    print(f"Processing batch: {batch}")
    game_details = fetch_game_details(batch)
    all_game_details.extend(game_details)
    time.sleep(0.25)  # Sleep for 250ms to respect the 4-requests-per-second limit

# Convert the results into a DataFrame
if all_game_details:
    game_details_df = pd.DataFrame(all_game_details)
    game_details_df.to_csv("BacklogDetails.csv", index=False)
    print("Game details fetched and saved successfully!")
else:
    print("No game details fetched.")
