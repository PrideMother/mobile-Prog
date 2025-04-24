import requests

def get_steam_achievements(api_key, steam_id, app_id):
    url = "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
    params = {
        "key": "FA2A02009368B6111842D0D2A1311FA5",
        "steamid": 76561198839380403,
        "appid": 292030
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None
