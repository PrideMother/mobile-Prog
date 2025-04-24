import requests

STEAM_API_KEY = "FA2A02009368B6111842D0D2A1311FA5"
STEAM_ID = "76561198839380403"

def get_user_games():
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": STEAM_ID,
        "format": "json",
        "include_appinfo": 1,  # чтобы получить иконки и названия
    }

    response = requests.get(url, params=params)
    games = response.json()["response"]["games"]
    return games

games = get_user_games()
for game in games:
    print(game["name"], game["appid"], game.get("img_icon_url", ""))
