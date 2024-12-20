import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the base URL for Backloggd and replace yourusername here
base_url = 'https://www.backloggd.com/u/yourusername/backlog?page='

# Function to scrape a single page
def scrape_page(page_num):
    url = base_url + str(page_num)
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_num}")
        return []
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all game cards
    game_cards = soup.find_all('div', class_='card mx-auto game-cover')
    
    # Extract game ID and name from each game card
    games = []
    for card in game_cards:
        game_id = card.get('game_id')
        game_name = card.find('img')['alt']
        
        games.append({'id': game_id, 'name': game_name})
    
    return games

# Scrape the first two pages (Change the range to how many ever you need)
all_games = []
for page in range(1, 3):
    all_games.extend(scrape_page(page))

# Create a DataFrame from the scraped data
games_df = pd.DataFrame(all_games)

# Save the data to a CSV file
games_df.to_csv('backlog.csv', index=False)

print(f"Scraped {len(games_df)} games from the backlog.")
