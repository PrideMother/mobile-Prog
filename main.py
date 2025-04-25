from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.uix.image import AsyncImage
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
import requests

KV = '''
ScreenManager:
    MainScreen:
    AchievementsScreen:

<MainScreen>:
    name: "main"
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Steam Games"
            elevation: 4

        ScrollView:
            MDBoxLayout:
                id: games_list
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: "8dp"
                spacing: "8dp"

<AchievementsScreen>:
    name: "achievements"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            id: top_bar
            title: "Achievements"
            elevation: 4
            left_action_items: [["arrow-left", lambda x: app.back_to_main()]]

        ScrollView:
            MDBoxLayout:
                id: achievements_layout
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: "8dp"
                spacing: "8dp"
'''

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
    data = response.json()
    return data['response'].get('games', [])


def get_game_achievements(api_key, steam_id, appid):
    url = "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
    params = {
        "key": api_key,
        "steamid": steam_id,
        "appid": appid
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("playerstats", {}).get("achievements", [])


class MainScreen(MDScreen):
    def on_pre_enter(self):
        self.load_steam_games()

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
                    padding="8dp",
                    ripple_behavior=True,
                    on_release=lambda x, appid=game['appid'], name=game['name']: self.show_achievements(appid, name)
                )

                image_url = f"https://media.steampowered.com/steamcommunity/public/images/apps/{game['appid']}/{game['img_icon_url']}.jpg"
                icon = AsyncImage(source=image_url, size_hint=(None, None), size=("64dp", "64dp"))

                label = MDLabel(
                    text=f"{game['name']}",
                    halign="left",
                    valign="middle"
                )
                label.bind(size=label.setter('text_size'))

                card.add_widget(icon)
                card.add_widget(label)
                games_list.add_widget(card)

        except Exception as e:
            print(f"Ошибка при загрузке игр: {e}")

    def show_achievements(self, appid, name):
        app = MDApp.get_running_app()
        screen = app.root.get_screen("achievements")
        screen.load_achievements(appid, name)
        app.root.current = "achievements"


class AchievementsScreen(MDScreen):
    def load_achievements(self, appid, name):
        self.ids.top_bar.title = f"Ачивки: {name}"
        layout = self.ids.achievements_layout
        layout.clear_widgets()

        try:
            achievements = get_game_achievements(STEAM_API_KEY, STEAM_ID, appid)

            if not achievements:
                layout.add_widget(MDLabel(text="Нет достижений для этой игры.", halign="center"))
                return

            total = len(achievements)
            unlocked = sum(1 for ach in achievements if ach.get("achieved") == 1)
            layout.add_widget(MDLabel(
                text=f"Прогресс: {unlocked}/{total} достижений",
                halign="center",
                theme_text_color="Custom",
                text_color=(0.2, 0.8, 0.2, 1),
                font_style="H6"
            ))

            for ach in achievements:
                name = ach.get("name", "Без названия")
                achieved = ach.get("achieved", 0)
                percent = "✅" if achieved else "❌"

                label = MDLabel(
                    text=f"{percent} {name}",
                    halign="left",
                    theme_text_color="Secondary"
                )
                layout.add_widget(label)

        except Exception as e:
            print(f"Ошибка при загрузке достижений: {e}")
            layout.add_widget(MDLabel(text="Не удалось загрузить достижения.", halign="center"))


class SteamApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def back_to_main(self):
        self.root.current = "main"


if __name__ == "__main__":
    SteamApp().run()
