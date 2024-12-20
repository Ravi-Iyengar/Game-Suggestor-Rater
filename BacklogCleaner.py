import pandas as pd

# Step 1: Read the CSV file into DataFrame
game_details_df = pd.read_csv("BacklogDetails.csv")

# Step 4: Function to extract names from a list of dictionaries
def extract_names(list_of_dicts):
    try:
        # Convert the string representation of a list of dicts into an actual list of dicts
        list_of_dicts = eval(list_of_dicts) if isinstance(list_of_dicts, str) else list_of_dicts
        if isinstance(list_of_dicts, list):  
            # Extract the 'name' from each dictionary in the list
            return ", ".join(d['name'] for d in list_of_dicts if 'name' in d)
    except (SyntaxError, ValueError, TypeError):
        pass  
    return None

# Step 5: Clean the genres, themes, and keywords columns
columns_to_clean = ['genres', 'themes', 'keywords']
for column in columns_to_clean:
    if column in game_details_df.columns:  # Ensure the column exists in the DataFrame
        game_details_df[column] = game_details_df[column].apply(extract_names)

# Step 6: Clean the 'genres' column for specific cases (example)
if 'genres' in game_details_df.columns:
    game_details_df['genres'] = game_details_df['genres'].str.replace(
        "4X (explore, expand, exploit, and exterminate)", 
        "4X", 
        regex=False
    )

# Step 7: Save the cleaned DataFrame to a new CSV file
output_file = "CleanedBacklogData.csv"
game_details_df.to_csv(output_file, index=False)

print(f"Cleaned data saved to {output_file}")
