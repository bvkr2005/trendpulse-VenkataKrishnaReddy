import pandas as pd
import os

# Step 1 — Load JSON file
file_path = "data/trends_20260413.json"  # change date if needed

df = pd.read_json(file_path)

print(f"Loaded {len(df)} stories from {file_path}")

# Step 2 — Clean Data

# 2.1 Remove duplicates based on post_id
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# 2.2 Drop missing values (critical fields)
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# 2.3 Fix data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)

# 2.4 Remove low quality stories (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# 2.5 Strip whitespace from title
df["title"] = df["title"].str.strip()

# Step 3 — Save cleaned CSV

output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")

# Step 4 — Summary by category
print("\nStories per category:")

category_counts = df["category"].value_counts()

for cat, count in category_counts.items():
    print(f"  {cat:<15} {count}")