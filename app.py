import os
import json
import logging
import requests
import time
import random
import re
from urllib.parse import urljoin, urlparse, quote
from flask import Flask, render_template, request, jsonify, redirect, url_for
import trafilatura
from bs4 import BeautifulSoup

from urllib.parse import urlparse
import sqlite3
from flask import request
# Configure logging
logging.basicConfig(level=logging.DEBUG)
from flask import Flask, request, redirect, render_template, url_for
import sqlite3, urllib.parse

# Cload_dotenv()

app = Flask(__name__)

# API key from environment
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Secret key (Render: SESSION_SECRET, Local: fallback to dev-secret-key)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Serper API URL
SERPER_URL = "https://google.serper.dev/search"
# Search engine configuration
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

class SearchEngine:
    def __init__(self):
        self.session = requests.Session()
        self.serper_api_key = SERPER_API_KEY
        self.perplexity_api_key = os.environ.get("PERPLEXITY_API_KEY")
        self.serper_url = f"{SERPER_URL}/search"

    def get_direct_answer(self, query: str):
        """Try to fetch a direct answer from Serper API"""
        if not self.serper_api_key:
            return None
        try:
            headers = {
                "X-API-KEY": self.serper_api_key,
                "Content-Type": "application/json"
            }
            payload = {"q": query, "num": 3}
            resp = self.session.post(self.serper_url, headers=headers, json=payload, timeout=8)
            resp.raise_for_status()
            data = resp.json()

            if "answerBox" in data:
                abox = data["answerBox"]
                if "answer" in abox:
                    return abox["answer"]
                if "snippet" in abox:
                    return abox["snippet"]
                if "title" in abox:
                    return abox["title"]

            return None
        except Exception as e:
            logging.warning(f"Direct answer fetch failed: {e}")
            return None

    def serper_request(self, query, search_type="search", num=20):
        """Generic request to Serper API for search, images, news, videos, shopping"""
        if not self.serper_api_key:
            return {}
        payload = {"q": query, "num": num}
        headers = {
            "X-API-KEY": self.serper_api_key,
            "Content-Type": "application/json"
        }
        url = f"{SERPER_URL}/{search_type}"
        response = self.session.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()


search_engine = SearchEngine()


# ---------------- ROUTES ---------------- #

@app.route('/')
def index():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/terms')
def terms():
    return render_template("terms.html")
@app.route('/privacy')
def privacy():
    return render_template("privacy.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/search')
def search():
    query = request.args.get("q", "")
    if not query:
        return redirect(url_for("index"))

    page = request.args.get("page", 1, type=int)
    return perform_search(query, "search", page)


@app.route('/search/images')
def search_images():
    query = request.args.get("q", "")
    return perform_search(query, "images")


@app.route('/search/news')
def search_news():
    query = request.args.get("q", "")
    return perform_search(query, "news")


@app.route('/search/videos')
def search_videos():
    query = request.args.get("q", "")
    return perform_search(query, "videos")


@app.route('/search/shopping')
def search_shopping():
    query = request.args.get("q", "")
    return perform_search(query, "shopping")

def perform_search(query, search_type, page=1):
    if not query:
        return redirect(url_for("index"))

    verified_only = request.args.get("verified") in ("1", "true", "on")
    results = []

    try:
        data = search_engine.serper_request(query, search_type)

        if search_type == "search" and "organic" in data:
            results = [
                {
                    "title": item.get("title"),
                    "url": item.get("link"),   # 👈 unified as url
                    "snippet": item.get("snippet"),
                    "domain": urlparse(item.get("link")).netloc if item.get("link") else ""
                }
                for item in data["organic"]
            ]

        elif search_type == "images" and "images" in data:
            results = [
                {
                    "title": item.get("title"),
                    "url": item.get("imageUrl"),   # 👈 url not link
                    "thumbnail": item.get("thumbnailUrl"),
                    "domain": urlparse(item.get("imageUrl")).netloc if item.get("imageUrl") else ""
                }
                for item in data["images"]
            ]

        elif search_type == "videos" and "videos" in data:
            results = [
                {
                    "title": item.get("title"),
                    "url": item.get("link"),
                    "thumbnail": item.get("imageUrl") or item.get("thumbnailUrl"),
                    "domain": urlparse(item.get("link")).netloc if item.get("link") else ""
                }
                for item in data["videos"]
            ]

        elif search_type == "news" and "news" in data:
            results = [
                {
                    "title": item.get("title"),
                    "url": item.get("link"),
                    "snippet": item.get("snippet"),
                    "domain": item.get("source") or urlparse(item.get("link")).netloc
                }
                for item in data["news"]
            ]

        elif search_type == "shopping" and "shopping" in data:
            results = [
                {
                    "title": item.get("title"),
                    "url": item.get("link"),
                    "price": item.get("price"),
                    "thumbnail": item.get("thumbnail"),
                    "domain": urlparse(item.get("link")).netloc if item.get("link") else ""
                }
                for item in data["shopping"]
            ]
        if results:
                    conn = sqlite3.connect("verified_sites.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT url FROM verified_sites")
                    verified_domains = {urlparse(row[0]).hostname.replace("www.", "") for row in cursor.fetchall()}
                    conn.close()

                    for r in results:
                        try:
                            domain = urlparse(r["url"]).hostname.replace("www.", "")
                            r["domain"] = r.get("domain") or domain
                            r["verified"] = domain in verified_domains
                            # wrap all clicks through /out
                            r["click_url"] = url_for("out", url=r["url"], q=query)
                        except:
                            r["verified"] = False
                            r["click_url"] = r["url"]

                    if verified_only:
                        results = [r for r in results if r["verified"]]

    except Exception as e:
        logging.error(f"{search_type} search error: {e}")
        results = []

    # ----- Pagination -----
    results_per_page = 10
    start_idx = (page - 1) * results_per_page
    paginated = results[start_idx:start_idx + results_per_page]
    total_pages = max(1, (len(results) + results_per_page - 1) // results_per_page)
    conn = sqlite3.connect("verified_sites.db")
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM verified_sites")
    verified_sites = [row[0] for row in cursor.fetchall()]
    conn.close()

    return render_template(
        "search.html",
        query=query,
        results=paginated,
        tab=search_type,
        page=page,
        total_pages=total_pages,
        total_results=len(results),
        search_time=round(random.uniform(0.15, 0.89), 2),
        verified_only=verified_only,
        verified_sites=verified_sites
    )
def get_verified_domains():
    conn = sqlite3.connect("verified_sites.db")
    cur = conn.cursor()
    cur.execute("SELECT url FROM verified_sites")
    rows = cur.fetchall()
    conn.close()
    domains = []
    for r in rows:
        try:
            domains.append(urllib.parse.urlparse(r[0]).hostname.replace("www.", ""))
        except:
            pass
    return domains
@app.route("/out")
def out():
    target_url = request.args.get("url")
    query = request.args.get("q", "")

    if not target_url:
        return redirect(url_for("index"))

    domain = urllib.parse.urlparse(target_url).hostname.replace("www.", "")
    verified_domains = get_verified_domains()

    if domain in verified_domains:
        # Directly verified → just open
        return redirect(target_url)
    else:
        filtered_domains = []
        if query:
            # split query into words, check if any word is in domain
            query_words = query.lower().split()
            for d in verified_domains:
                if any(word in d.lower() for word in query_words):
                    filtered_domains.append(d)

        # fallback → if nothing matched, show ALL verified
        if not filtered_domains:
            filtered_domains = verified_domains  

        return render_template(
            "confirm.html",
            url=target_url,
            domain=domain,
            filtered_domains=filtered_domains,
            query=query
        )
    
@app.route('/api/suggestions')
def get_suggestions():
    """Enhanced API endpoint for search suggestions"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])

    # Popular searches
    popular_searches = [
        "python programming", "javascript tutorial", "react development",
        "machine learning", "artificial intelligence", "web development",
        "data science", "cloud computing", "cybersecurity", "blockchain",
        "mobile development", "software engineering", "open source projects",
        "coding bootcamp", "programming languages", "tech news today",
        "weather forecast", "stock market", "cryptocurrency prices",
        "sports scores", "movie reviews", "restaurant near me"
    ]

    try:
        with open('static/data/suggestions.json', 'r') as f:
            file_suggestions = json.load(f)
        popular_searches.extend(file_suggestions)
    except FileNotFoundError:
        pass

    # Smart matching
    exact_matches = [s for s in popular_searches if s.lower().startswith(query)]
    partial_matches = [s for s in popular_searches if query in s.lower() and not s.lower().startswith(query)]
    suggestions = exact_matches + partial_matches

    # Deduplicate
    seen, unique_suggestions = set(), []
    for s in suggestions:
        if s.lower() not in seen:
            seen.add(s.lower())
            unique_suggestions.append(s)

    return jsonify(unique_suggestions[:8])


@app.route('/lucky')
def feeling_lucky():
    """I'm Feeling Lucky - redirects to first search result"""
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('index'))

    try:
        results = search_engine.search_web(query, 1)
        if results:
            return redirect(results[0]['url'])
    except Exception as e:
        logging.error(f"Feeling lucky error: {e}")

    return redirect(url_for('search', q=query))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
