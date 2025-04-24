from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import MDListItem, MDListItemText, MDListItemLeading
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
import requests

KV = '''
Screen:
    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Steam Library"
            elevation: 4

        ScrollView:
            id: scroll
'''

STEAM_API_KEY = 'your_api_key'
STEAM_USER_ID = 'your_steam_id'

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def on_start(self):
        self.load_steam_games()

    def load_steam_games(self):
        url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
        params = {
            'key': STEAM_API_KEY,
            'steamid': STEAM_USER_ID,
            'include_appinfo': True,
            'include_played_free_games': True
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            list_container = MDBoxLayout(orientation="vertical", spacing=4, padding=4)
            for game in data['response'].get('games', []):
                icon_url = f"http://media.steampowered.com/steamcommunity/public/images/apps/{game['appid']}/{game['img_icon_url']}.jpg"
                item = MDListItem()
                item.add_widget(
                    MDListItemLeading(
                        AsyncImage(source=icon_url, size_hint=(None, None), size=(48, 48))
                    )
                )
                item.add_widget(MDListItemText(text=game['name']))
                list_container.add_widget(item)

            self.root.ids.scroll.add_widget(list_container)

        except Exception as e:
            print(f"Error loading games: {e}")

MainApp().run()
