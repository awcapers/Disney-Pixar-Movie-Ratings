import pandas as pd
import matplotlib.pyplot as plt
import os

# Print current directory for debugging
print("Current working directory:", os.getcwd())

# --- Load IMDb Data ---
basics = pd.read_csv(
    "C:/Users/anjol/CHIP690/milestone2/title.basics.tsv.gz",
    sep="\t",
    low_memory=False,
    compression="gzip",
)

ratings = pd.read_csv(
    "C:/Users/anjol/CHIP690/milestone2/title.ratings.tsv.gz",
    sep="\t",
    low_memory=False,
    compression="gzip",
)

# --- Filter to only movies ---
movies = basics[basics["titleType"] == "movie"]

# --- Pixar Movies: (title, year) pairs ---
pixar_title_years = [
    ("Toy Story", 1995),
    ("A Bug's Life", 1998),
    ("Toy Story 2", 1999),
    ("Monsters, Inc.", 2001),
    ("Finding Nemo", 2003),
    ("The Incredibles", 2004),
    ("Cars", 2006),
    ("Ratatouille", 2007),
    ("WALL-E", 2008),
    ("Up", 2009),
    ("Toy Story 3", 2010),
    ("Cars 2", 2011),
    ("Brave", 2012),
    ("Monsters University", 2013),
    ("Inside Out", 2015),
    ("The Good Dinosaur", 2015),
    ("Finding Dory", 2016),
    ("Cars 3", 2017),
    ("Coco", 2017),
    ("Incredibles 2", 2018),
    ("Toy Story 4", 2019),
    ("Onward", 2020),
    ("Soul", 2020),
    ("Luca", 2021),
    ("Turning Red", 2022),
]

# --- Filter by exact title and year ---
# Remove rows where startYear is not a number
movies = movies[movies["startYear"].apply(lambda x: str(x).isdigit())]
movies["startYear"] = movies["startYear"].astype(int)

# Create tuple column for matching
movie_tuples = movies[["primaryTitle", "startYear"]].apply(tuple, axis=1)

# Filter to exact Pixar movies
pixar_df = movies[movie_tuples.isin(pixar_title_years)]

# --- Merge with Ratings ---
merged_df = pd.merge(pixar_df, ratings, on="tconst")

# --- Final Clean DataFrame ---
final_df = merged_df[["primaryTitle", "startYear", "averageRating", "numVotes"]]
final_df = final_df.sort_values(by="averageRating", ascending=False)

# --- Print to confirm matches ---
print("\n✅ Final Pixar Movie Matches (title + year):\n")
print(final_df[["primaryTitle", "startYear"]].drop_duplicates().to_string(index=False))

# --- Save to CSV ---
final_df.to_csv(
    "C:/Users/anjol/CHIP690/milestone2/pixar_movie_ratings.csv", index=False
)

# --- Plot 1: Top 10 Highest Rated Pixar Movies ---
top_10 = final_df.head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_10["primaryTitle"], top_10["averageRating"], color="skyblue")
plt.xlabel("IMDb Rating")
plt.title("Top 10 Highest Rated Pixar Movies")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# --- Plot 2: Pixar Ratings Over Time ---
plt.figure(figsize=(10, 6))
plt.scatter(final_df["startYear"], final_df["averageRating"], color="purple")
plt.xlabel("Release Year")
plt.ylabel("IMDb Rating")
plt.title("Pixar Movie Ratings Over Time")
plt.grid(True)
plt.tight_layout()
plt.show()
