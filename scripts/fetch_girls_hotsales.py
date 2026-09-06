import requests
from bs4 import BeautifulSoup
import json
import datetime

BASE_URL = "https://www.readnovel.com"
RANK_URL = "https://www.readnovel.com/rank/hotsales?chanId=300"  # 女生畅销榜

def fetch_toplist():
    resp = requests.get(RANK_URL, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    books = []

    for item in soup.select(".book-img-text li"):
        title = item.select_one(".book-mid-info h4 a").text.strip()
        link = BASE_URL + item.select_one(".book-mid-info h4 a")["href"]
        author = item.select_one(".author a").text.strip()
        intro = item.select_one(".intro").text.strip()
        category = item.select_one(".author span:nth-of-type(2)").text.strip()
        status = item.select_one(".author span:nth-of-type(3)").text.strip()

        books.append({
            "title": title,
            "author": author,
            "intro": intro,
            "category": category,
            "status": status,
            "link": link
        })

    return books

def save_data(data):
    output = {
        "updated_at": datetime.datetime.now().isoformat(),
        "source": RANK_URL,
        "books": data
    }
    with open("data/girls_hotsales.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    data = fetch_toplist()
    save_data(data)
