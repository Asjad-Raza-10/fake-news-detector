# File: api/api_utils.py
import requests
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
GNEWS_KEY = os.getenv("GNEWS_KEY")
FACTCHECK_KEY = os.getenv("FACTCHECK_KEY")
MEDIASTACK_KEY = os.getenv("MEDIASTACK_KEY")
NEWSDATA_KEY = os.getenv("NEWSDATA_KEY")
CURRENTS_KEY = os.getenv("CURRENTS_KEY")

def extract_keywords(text, max_words=8):
    """Extract key terms from the news text for better API search"""
    # For headlines and short text, use more liberal extraction
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'this', 'that', 'these', 'those'}
    
    # Clean the text but preserve important punctuation context
    words = []
    for word in text.split():
        # Remove punctuation but keep apostrophes for contractions
        clean_word = word.strip('.,!?":;()[]{}').replace('"', '').replace('"', '')
        if len(clean_word) > 2 and clean_word.lower() not in stop_words:
            words.append(clean_word)
    
    # For very short text (likely headlines), be more generous
    if len(text.split()) <= 15:
        return ' '.join(words[:max_words])
    else:
        # For longer text, be more selective
        return ' '.join(words[:6])

def search_newsapi_articles(query):
    """Search NewsAPI for articles matching the query"""
    if not NEWSAPI_KEY:
        print("NewsAPI key not found")
        return []
    
    # Try multiple search strategies
    search_queries = [
        query.strip(),  # Original query first
        extract_keywords(query, 8),  # Then keywords
        extract_keywords(query, 4)   # Fallback with fewer keywords
    ]
    
    for search_query in search_queries:
        if not search_query:
            continue
            
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": search_query,
            "apiKey": NEWSAPI_KEY,
            "language": "en",
            "sortBy": "relevancy",
            "pageSize": 15,
            "searchIn": "title,description,content"
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            print(f"NewsAPI Status Code: {response.status_code}")
            print(f"NewsAPI Search Query: '{search_query}'")
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])
                print(f"NewsAPI found {len(articles)} articles with query: '{search_query}'")
                if articles:  # Return first successful result
                    return articles
            else:
                print(f"NewsAPI Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"NewsAPI Exception with query '{search_query}': {e}")
            continue
    
    return []

def search_gnews_articles(query):
    """Search GNews for articles matching the query"""
    if not GNEWS_KEY:
        print("GNews key not found")
        return []
    
    # Try multiple search strategies
    search_queries = [
        query.strip(),  # Original query first
        extract_keywords(query, 6),  # Then keywords
        extract_keywords(query, 3)   # Fallback with fewer keywords
    ]
    
    for search_query in search_queries:
        if not search_query:
            continue
            
        # Clean query for GNews (remove quotes and special characters that cause 400 errors)
        clean_query = search_query.replace("'", "").replace('"', '').replace('(', '').replace(')', '')
        encoded_query = urllib.parse.quote(clean_query)
        
        url = f"https://gnews.io/api/v4/search"
        params = {
            "q": encoded_query,
            "lang": "en",
            "max": 15,
            "token": GNEWS_KEY
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            print(f"GNews Status Code: {response.status_code}")
            print(f"GNews Search Query: '{clean_query}'")
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])
                print(f"GNews found {len(articles)} articles with query: '{clean_query}'")
                if articles:  # Return first successful result
                    return articles
            else:
                print(f"GNews Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"GNews Exception with query '{clean_query}': {e}")
            continue
    
    return []

def search_factcheck(query):
    """Search Google Fact Check API for claims matching the query"""
    if not FACTCHECK_KEY:
        print("FactCheck key not found")
        return []
    
    # Try multiple search strategies
    search_queries = [
        query.strip(),  # Original query first
        extract_keywords(query, 6),  # Then keywords
        extract_keywords(query, 3)   # Fallback with fewer keywords
    ]
    
    for search_query in search_queries:
        if not search_query:
            continue
            
        # Clean query for FactCheck API
        clean_query = search_query.replace("'", "").replace('"', '')
        encoded_query = urllib.parse.quote(clean_query)
        
        url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search"
        params = {
            "query": encoded_query,
            "key": FACTCHECK_KEY,
            "languageCode": "en"
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            print(f"FactCheck Status Code: {response.status_code}")
            print(f"FactCheck Search Query: '{clean_query}'")
            
            if response.status_code == 200:
                data = response.json()
                claims = data.get("claims", [])
                print(f"FactCheck found {len(claims)} claims with query: '{clean_query}'")
                if claims:  # Return first successful result
                    return claims
            else:
                print(f"FactCheck API Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"FactCheck API Exception with query '{clean_query}': {e}")
            continue
    
    return []

def search_mediastack(query):
    """Search MediaStack API for news articles (Free tier: 500 requests/month)"""
    if not MEDIASTACK_KEY:
        print("MediaStack key not found")
        return []
    
    # Try multiple search strategies
    search_queries = [
        query.strip(),  # Original query first
        extract_keywords(query, 6),  # Then keywords
        extract_keywords(query, 3)   # Fallback with fewer keywords
    ]
    
    for search_query in search_queries:
        if not search_query:
            continue
            
        url = "http://api.mediastack.com/v1/news"
        params = {
            "access_key": MEDIASTACK_KEY,
            "keywords": search_query,
            "languages": "en",
            "limit": 15
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            print(f"MediaStack Status Code: {response.status_code}")
            print(f"MediaStack Search Query: '{search_query}'")
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get("data", [])
                print(f"MediaStack found {len(articles)} articles with query: '{search_query}'")
                if articles:  # Return first successful result
                    return articles
            else:
                print(f"MediaStack Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"MediaStack Exception with query '{search_query}': {e}")
            continue
    
    return []

def search_newsdata_io(query):
    """Search NewsData.io API (Free tier: 200 requests/day)"""
    if not NEWSDATA_KEY:
        print("NewsData key not found")
        return []
    
    # Try multiple search strategies
    search_queries = [
        query.strip(),  # Original query first
        extract_keywords(query, 6),  # Then keywords
        extract_keywords(query, 3)   # Fallback with fewer keywords
    ]
    
    for search_query in search_queries:
        if not search_query:
            continue
            
        url = "https://newsdata.io/api/1/news"
        params = {
            "apikey": NEWSDATA_KEY,
            "q": search_query,
            "language": "en",
            "size": 10
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            print(f"NewsData Status Code: {response.status_code}")
            print(f"NewsData Search Query: '{search_query}'")
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get("results", [])
                print(f"NewsData found {len(articles)} articles with query: '{search_query}'")
                if articles:  # Return first successful result
                    return articles
            else:
                print(f"NewsData Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"NewsData Exception with query '{search_query}': {e}")
            continue
    
    return []

def search_currents_api(query):
    """Search Currents API (Free tier: 600 requests/month)"""
    if not CURRENTS_KEY:
        print("Currents key not found")
        return []
    
    # Try multiple search strategies
    search_queries = [
        query.strip(),  # Original query first
        extract_keywords(query, 6),  # Then keywords
        extract_keywords(query, 3)   # Fallback with fewer keywords
    ]
    
    for search_query in search_queries:
        if not search_query:
            continue
            
        url = "https://api.currentsapi.services/v1/search"
        params = {
            "apiKey": CURRENTS_KEY,
            "keywords": search_query,
            "language": "en"
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            print(f"Currents Status Code: {response.status_code}")
            print(f"Currents Search Query: '{search_query}'")
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get("news", [])
                print(f"Currents found {len(articles)} articles with query: '{search_query}'")
                if articles:  # Return first successful result
                    return articles
            else:
                print(f"Currents Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Currents Exception with query '{search_query}': {e}")
            continue
    
    return []