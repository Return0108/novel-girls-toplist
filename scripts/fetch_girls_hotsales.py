import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# 改用移动端页面，服务端渲染，可直接解析
URL = "https://m.readnovel.com/rank/hotsales?chanId=300"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Referer": "https://m.readnovel.com/"
}

def main():
    resp = requests.get(URL, headers=HEADERS, timeout=20)
    resp.encoding = "utf‑8"
    soup = BeautifulSoup(resp.text, "html.parser")

    books = []
    # m站榜单条目
    items = soup.select(".rank‑book‑item")
    for item in items:
        title_elem = item.select_one(".book‑title")
        author_elem = item.select_one(".book‑author")
        link_elem = item.select_one("a")
        if not title_elem:
            continue
        book = {
            "title": title_elem.get_text(strip=True),
            "author": author_elem.get_text(strip=True) if author_elem else "",
            "url": "https://m.readnovel.com" + link_elem["href"] if link_elem else ""
        }
        books.append(book)

    output = {
        "updated_at": datetime.utcnow().isoformat(),
        "source": URL,
        "books": books
    }

    with open("data/girls_hotsales.json", "w", encoding="utf‑8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"抓取完成，共获取 {len(books)} 本书籍")

if __name__ == "__main__":
    main()
