from django.conf import settings
import requests

def search_jobs(query):
    app_id = settings.ADZUNA_APP_ID
    app_key = settings.ADZUNA_APP_KEY

    if not app_id or not app_key:
        return {"results": []}  # fail gracefully if keys missing

    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": 100,
        "what": query,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return {"results": []}
