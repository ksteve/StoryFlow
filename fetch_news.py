import os
import json
from newsapi import NewsApiClient
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# --- Setup Firebase ---
creds = json.loads(os.environ["FIREBASE_CREDENTIALS"])
cred = credentials.Certificate(creds)
firebase_admin.initialize_app(cred)
db = firestore.client()

# --- Setup NewsAPI ---
newsapi = NewsApiClient(api_key=os.environ["NEWSAPI_KEY"])
TOPIC = "technology"

def fetch_articles():
    all_articles = newsapi.get_everything(
        q=TOPIC,
        language="en",
        sort_by="publishedAt",
        page_size=20,
    )

    stored = 0
    for article in all_articles.get("articles", []):
        url = article["url"]

        # Check for duplicates
        docs = db.collection("articles").where("url", "==", url).limit(1).stream()
        if any(True for _ in docs):
            continue

        doc = {
            "title": article["title"],
            "summary": article["description"],
            "url": url,
            "image": article["urlToImage"],
            "source": article["source"]["name"],
            "publishedAt": article["publishedAt"],
            "fetchedAt": datetime.utcnow().isoformat() + "Z",
            "topic": TOPIC,
            "clustered": False,
            "clusterId": None,
        }

        db.collection("articles").add(doc)
        stored += 1

    print(f"✅ Stored {stored} new articles.")

if __name__ == "__main__":
    fetch_articles()
