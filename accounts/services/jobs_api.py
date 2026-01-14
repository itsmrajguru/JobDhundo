import requests
from django.conf import settings

def search_jobs(query, location="India", page=1):
    url = f"https://api.adzuna.com/v1/api/jobs/in/search/{page}"
    params = {
        "app_id": settings.ADZUNA_APP_ID,
        "app_key": settings.ADZUNA_APP_KEY,
        "what": query,        # keyword (can be empty string)
        "where": location,    # location
        "results_per_page": 10,
        "content-type": "application/json",
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()
