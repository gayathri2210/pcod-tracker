import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# 1. Load the Excel file
file_path = r'C:\Users\gayat\project25\mood-recipe-tracker\food_data_final.xlsx'
df = pd.read_excel(file_path)

# 2. Inspect the columns
print("Columns:", df.columns.tolist())
print(df.head())

# 3. Combine relevant columns for text features
# Adjust these column names if needed based on your actual file
text_columns = []
if 'Recipe Ingredients' in df.columns:
    text_columns.append('Recipe Ingredients')
if 'Recipe' in df.columns:
    text_columns.append('Recipe')
if 'Dish' in df.columns:
    text_columns.append('Dish')
if not text_columns:
    raise ValueError("No suitable columns found for text features.")

df['text'] = df[text_columns].fillna('').agg(' '.join, axis=1)

# 4. Vectorize the text data
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['text'])

# 5. Choose number of clusters (e.g., number of unique moods)
if 'Mood' in df.columns:
    num_clusters = df['Mood'].nunique()
else:
    num_clusters = 5  # fallback

# 6. Train KMeans clustering model
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X)

# 7. Assign cluster labels to the dataframe
df['cluster'] = kmeans.labels_

# 8. Plot the number of recipes per cluster
cluster_counts = df['cluster'].value_counts().sort_index()
plt.bar(cluster_counts.index, cluster_counts.values, color="#16c1d4")
plt.xlabel('Cluster')
plt.ylabel('Number of Recipes')
plt.title('Number of Recipes per Cluster')
plt.show()

# 9. Save the dataframe with clusters to CSV (optional)
df.to_csv('food_data_with_clusters.csv', index=False)

# 10. Show a sample of the results
print(df[['Mood', 'Dish', 'cluster']].head())
