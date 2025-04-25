# icon_game.py

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage
import requests

STEAM_API_KEY = "FA2A02009368B6111842D0D2A1311FA5"
STEAM_ID = "76561198839380403"

def get_steam_games(api_key, steam_id):
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": api_key,
        "steamid": steam_id,
        "include_appinfo": True,
        "include_played_free_games": True
    }
    response = requests.get(url, params=params)
    return response.json()['response'].get('games', [])

class MainScreen(MDScreen):
    def load_steam_games(self):
        try:
            games = get_steam_games(STEAM_API_KEY, STEAM_ID)
            games_list = self.ids.games_list
            games_list.clear_widgets()

            for game in games:
                card = MDCard(
                    orientation="horizontal",
                    size_hint_y=None,
                    height="100dp",
                    padding="8dp"
                )
                image_url = f"https://media.steampowered.com/steamcommunity/public/images/apps/{game['appid']}/{game['img_icon_url']}.jpg"
                icon = AsyncImage(source=image_url, size_hint=(None, None), size=("64dp", "64dp"))

                label = MDLabel(
                    text=f"{game['name']}\nID: {game['appid']}",
                    halign="left",
                    valign="middle"
                )
                label.bind(size=label.setter('text_size'))

                card.add_widget(icon)
                card.add_widget(label)
                games_list.add_widget(card)
        except Exception as e:
            print(f"Ошибка при загрузке игр: {e}")
