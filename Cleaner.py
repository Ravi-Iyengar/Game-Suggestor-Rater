import pandas as pd

# Step 1: Read both CSV files into DataFrames
game_details_df = pd.read_csv("GameDetails.csv")
played_games_df = pd.read_csv("PlayedGames.csv")

# Step 2: Rename the 'rating' column in PlayedGames.csv to 'myrating'
played_games_df.rename(columns={"rating": "myrating"}, inplace=True)

# Step 3: Sort both DataFrames by the 'id' column
game_details_df.sort_values(by="id", inplace=True)
played_games_df.sort_values(by="id", inplace=True)

# Step 4: Function to extract names from list of dictionaries
def extract_names(list_of_dicts):
    try:
        list_of_dicts = eval(list_of_dicts) if isinstance(list_of_dicts, str) else list_of_dicts
        if isinstance(list_of_dicts, list):  
            return ", ".join(d['name'] for d in list_of_dicts if 'name' in d)
    except (SyntaxError, ValueError, TypeError):
        pass  
    return None

# Step 5: Clean the genres, themes, and keywords columns in GameDetails.csv
columns_to_clean = ['genres', 'themes', 'keywords']
for column in columns_to_clean:
    if column in game_details_df.columns:  # Ensure the column exists in the DataFrame
        game_details_df[column] = game_details_df[column].apply(extract_names)

# Step 6: Merge the two DataFrames on the 'id' column
merged_df = pd.merge(game_details_df, played_games_df, on="id", how="inner")

# Step 7: Replace the '4X (explore, expand, exploit, and exterminate)' text in the merged DataFrame
merged_df['genres'] = merged_df['genres'].str.replace(
    "4X (explore, expand, exploit, and exterminate)", 
    "4X", 
    regex=False
)

# Step 8: Save the merged DataFrame to a new CSV file
output_file = "MergedGameDetails.csv"
merged_df.to_csv(output_file, index=False)

print(f"Merged data saved to {output_file}")
