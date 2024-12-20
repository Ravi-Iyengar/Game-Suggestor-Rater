import requests
from bs4 import BeautifulSoup
import pandas as pd

# Replace yourusername ; also this assumes you have at least 1 page worth of data in terms of rating and hours played for the model
base_url = "https://www.backloggd.com/u/yourusername/games/time/type:played?page="

# List to store the scraped data
games_data = []

# Loop through pages 1 to 5 (Change this to fit How many ever pages you need)
for page in range(1, 6):
    print(f"Scraping page {page}...")
    # Construct the URL for the current page
    url = f"{base_url}{page}"
    
    # Fetch the page content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch page {page}. Status code: {response.status_code}")
        continue
    
    # Parse the page content
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all game elements
    game_elements = soup.find_all("div", class_="card mx-auto game-cover user-rating")
    
    for game in game_elements:
        try:
            # Extract game ID
            game_id = game["game_id"]
            
            # Extract rating
            rating = game["data-rating"]
            
            # Extract hours played
            hours_element = game.find_next("p", class_="mb-0 avg-rating")
            hours_played = hours_element.text.strip() if hours_element else "0.0 hrs"
            
            # Convert hours to a float value
            hours_played = float(hours_played.replace(" hrs", "").replace(",", ""))
            
            # Append the data to the list
            games_data.append({
                "id": game_id,
                "rating": int(rating),
                "hours_played": hours_played
            })
        except Exception as e:
            print(f"Error processing a game entry: {e}")
            continue

# Create a DataFrame from the collected data
df = pd.DataFrame(games_data)

# Ensure 'id' column is treated as a string
df['id'] = df['id'].astype(str)

# Save the data to a CSV file
df.to_csv("PlayedGames.csv", index=False)
print("Scraping complete. Data saved to PlayedGames.csv.")
