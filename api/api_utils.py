import os, requests
from dotenv import load_dotenv

load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
GNEWS_KEY = os.getenv("GNEWS_KEY")
FACTCHECK_KEY = os.getenv("FACTCHECK_KEY")

def verify_with_newsapi(query):
    url = "https://newsapi.org/v2/everything"
    res = requests.get(url, params={"q": query, "apiKey": NEWSAPI_KEY, "pageSize": 3})
    return res.json().get("articles", [])

def verify_with_gnews(query):
    url = "https://gnews.io/api/v4/search"
    res = requests.get(url, params={"q": query, "token": GNEWS_KEY, "lang": "en", "max": 3})
    return res.json().get("articles", [])

def verify_factcheck(query):
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    res = requests.get(url, params={"query": query, "key": FACTCHECK_KEY})
    return res.json().get("claims", [])
