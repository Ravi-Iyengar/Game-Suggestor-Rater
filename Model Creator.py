import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Step 1: Preprocessing function for MergedGameDetails.csv
def preprocess_data(csv_path):
    df = pd.read_csv(csv_path)

    # Fill missing values in 'rating' column with 75
    df['rating'] = df['rating'].fillna(75)

    # Transform 'hours_played' to 'log_hours_played' for normalization
    df['log_hours_played'] = np.log(df['hours_played'])

    # Convert genres, themes, and keywords from string representations to comma-separated names
    mlb_genres = MultiLabelBinarizer()
    mlb_themes = MultiLabelBinarizer()

    # Process genres and themes
    df['genres'] = df['genres'].apply(lambda x: x.split(', ') if isinstance(x, str) else [])
    df['themes'] = df['themes'].apply(lambda x: x.split(', ') if isinstance(x, str) else [])

    genres_bin = mlb_genres.fit_transform(df['genres'])
    themes_bin = mlb_themes.fit_transform(df['themes'])

    genres_df = pd.DataFrame(genres_bin, columns=mlb_genres.classes_)
    themes_df = pd.DataFrame(themes_bin, columns=mlb_themes.classes_)

    # Handle keywords with TF-IDF
    df['keywords'] = df['keywords'].fillna('')
    tfidf_vectorizer = TfidfVectorizer(tokenizer=lambda x: x.split(', '), stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['keywords'])
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())

    # Combine features
    feature_df = pd.concat([df[['id', 'name', 'log_hours_played', 'rating']], genres_df, themes_df, tfidf_df], axis=1)
    target = df['myrating']
    return feature_df, target, mlb_genres, mlb_themes, tfidf_vectorizer

# Step 2: Preprocessing function for CleanedBacklogdata.csv
def preprocess_backlog(csv_path, mlb_genres, mlb_themes, tfidf_vectorizer):
    df = pd.read_csv(csv_path)

    # Fill missing values in 'rating' column with 75
    df['rating'] = df['rating'].fillna(75)

    # Add 'log_hours_played' column with log(10) value for every game in the backlog
    df['log_hours_played'] = np.log(10)

    # Process genres and themes
    df['genres'] = df['genres'].apply(lambda x: x.split(', ') if isinstance(x, str) else [])
    df['themes'] = df['themes'].apply(lambda x: x.split(', ') if isinstance(x, str) else [])

    genres_bin = mlb_genres.transform(df['genres'])
    themes_bin = mlb_themes.transform(df['themes'])

    genres_df = pd.DataFrame(genres_bin, columns=mlb_genres.classes_)
    themes_df = pd.DataFrame(themes_bin, columns=mlb_themes.classes_)

    # Handle keywords with TF-IDF
    df['keywords'] = df['keywords'].fillna('')
    tfidf_matrix = tfidf_vectorizer.transform(df['keywords'])
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())

    # Combine features
    feature_df = pd.concat([df[['id', 'name', 'log_hours_played', 'rating']], genres_df, themes_df, tfidf_df], axis=1)
    return feature_df

# Step 3: Train the model
merged_data_path = "MergedGameDetails.csv"
backlog_data_path = "CleanedBacklogdata.csv"

# Preprocess the merged data
features, target, mlb_genres, mlb_themes, tfidf_vectorizer = preprocess_data(merged_data_path)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features.drop(columns=['id', 'name']), target, test_size=0.2, random_state=42)

# Train the Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate on test data
y_pred_test = rf_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred_test)
print(f"Mean Squared Error on Test Set: {mse}")

# Step 4: Predict ratings for backlog data
backlog_features = preprocess_backlog(backlog_data_path, mlb_genres, mlb_themes, tfidf_vectorizer)
backlog_predictions = rf_model.predict(backlog_features.drop(columns=['id', 'name']))

# Step 5: Save the results
backlog_features['predicted_rating'] = backlog_predictions

# Create a new DataFrame with only 'id', 'name', and 'predicted_rating'
final_output = backlog_features[['id', 'name', 'predicted_rating']]

# Sort the DataFrame by 'predicted_rating' in descending order before saving
final_output = final_output.sort_values(by='predicted_rating', ascending=False)

# Save the DataFrame to a CSV file
output_path = "PredictedBacklogRatings.csv"
final_output.to_csv(output_path, index=False)

# Print top 10 highest predicted ratings
top_10 = final_output.head(10)
print(top_10)

print(f"Predicted ratings saved to {output_path}")


