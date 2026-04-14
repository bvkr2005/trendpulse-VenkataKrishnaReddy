import pandas as pd
import numpy as np

# Step 1 — Load data
file_path = "data/trends_clean.csv"

df = pd.read_csv(file_path)

print(f"Loaded data: {df.shape}")

# First 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Average score and comments
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {avg_score:,.0f}")
print(f"Average comments: {avg_comments:,.0f}")


# Step 2 — NumPy Analysis
print("\n--- NumPy Stats ---")

scores = df["score"].values

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

max_score = np.max(scores)
min_score = np.min(scores)

print(f"Mean score   : {mean_score:,.0f}")
print(f"Median score : {median_score:,.0f}")
print(f"Std deviation: {std_score:,.0f}")
print(f"Max score    : {max_score:,}")
print(f"Min score    : {min_score:,}")

# Category with most stories
top_category = df["category"].value_counts().idxmax()
top_count = df["category"].value_counts().max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Story with most comments
max_comments_idx = df["num_comments"].idxmax()
top_story = df.loc[max_comments_idx]

print(f'\nMost commented story: "{top_story["title"]}" — {top_story["num_comments"]:,} comments')


# Step 3 — Add new columns

# engagement = comments per upvote
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = score > average
df["is_popular"] = df["score"] > avg_score


# Step 4 — Save file

output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")