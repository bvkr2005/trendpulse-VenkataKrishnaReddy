import requests
import time
import json
import os
from datetime import datetime

# Base URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header
headers = {"User-Agent": "TrendPulse/1.0"}

# Category keywords
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Assign category
def get_category(title):
    title = title.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title:
                return category
    return None


# Retry function
def fetch_story(story_id):
    url = ITEM_URL.format(story_id)

    for attempt in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                return res.json()
        except Exception:
            print(f"Retry {attempt+1} for story {story_id}")
            time.sleep(1)

    print(f"Failed to fetch story {story_id}")
    return None


# Fetch top story IDs
try:
    response = requests.get(TOP_STORIES_URL, headers=headers, timeout=10)
    story_ids = response.json()[:500]
except Exception as e:
    print("Failed to fetch top stories:", e)
    story_ids = []


collected_stories = []
category_count = {cat: 0 for cat in CATEGORIES}
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 🚀 MAIN LOOP (UPDATED)
for i, story_id in enumerate(story_ids):

    print(f"{i+1}/500 | Collected: {len(collected_stories)}")

    story = fetch_story(story_id)

    if not story or "title" not in story:
        continue

    category = get_category(story["title"])

    # fallback category
    if not category:
        category = "technology"

    # flexible category limit
    if category_count[category] >= 25 and len(collected_stories) >= 100:
        continue

    data = {
        "post_id": story.get("id"),
        "title": story.get("title"),
        "category": category,
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by"),
        "collected_at": current_time
    }

    collected_stories.append(data)
    category_count[category] += 1

    # stop condition
    if len(collected_stories) >= 120:
        print("Reached target, stopping early...")
        break

    # faster but safe delay
    time.sleep(0.05)


# ✅ Ensure data folder exists
if not os.path.exists("data"):
    os.makedirs("data")

# Save file
file_name = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

with open(file_name, "w", encoding="utf-8") as f:
    json.dump(collected_stories, f, indent=4)

print("\nDONE ✅")
print(f"Collected {len(collected_stories)} stories.")
print(f"Saved to {file_name}")