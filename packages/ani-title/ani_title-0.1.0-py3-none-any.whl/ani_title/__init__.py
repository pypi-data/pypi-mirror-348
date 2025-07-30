import requests

_session = requests.Session()
_cache = {}

def _clean_input(text: str) -> str:
    return text.lower().strip().replace('-', ' ').replace('_', ' ')

def get_ani_title(anime_name: str) -> str:
    anime_name_clean = _clean_input(anime_name)
    if anime_name_clean in _cache:
        return _cache[anime_name_clean]

    url = f"https://kitsu.io/api/edge/anime?filter[text]={anime_name_clean}"
    try:
        response = _session.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data["data"]:
                titles = data["data"][0]["attributes"]["titles"]
                ani_title = titles.get("en_jp") or titles.get("ja_jp") or "Title not found"
                _cache[anime_name_clean] = ani_title
                return ani_title
            else:
                return "❌ No anime found."
        else:
            return f"❌ API Error: {response.status_code}"
    except requests.exceptions.RequestException:
        return "❌ Network error or timeout."
  
