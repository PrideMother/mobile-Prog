from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image  # стандартный виджет Kivy
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
from kivymd.uix.appbar import MDTopAppBar
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard

from steam_api import get_steam_achievements
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("STEAM_API_KEY") or "FA2A02009368B6111842D0D2A1311FA5"
STEAM_ID = "76561198839380403"
APP_ID = "292030"  # The Witcher 3

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Мои достижения"
            elevation: 10

        ScrollView:
            MDList:
                id: achievements_list
'''


class AchievementCard(MDCard):
    def __init__(self, name, description, icon_url, achieved, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.height = "100dp"
        self.padding = "8dp"
        self.spacing = "8dp"
        self.elevation = 4
        self.radius = [12]
        self.md_bg_color = (0.15, 0.15, 0.15, 1) if not achieved else (0.1, 0.4, 0.1, 1)

        layout = MDBoxLayout(orientation="horizontal", spacing="10dp")

        icon = AsyncImage(
            source=icon_url,
            size_hint=(None, None),
            size=("64dp", "64dp"),
            allow_stretch=True,
            keep_ratio=True
        )

        text_box = MDBoxLayout(orientation="vertical", spacing="5dp")

        text_box.add_widget(MDLabel(
            text=name,
            font_size="18sp",
            bold=True,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            halign="left"
        ))

        text_box.add_widget(MDLabel(
            text=description,
            font_size="14sp",
            theme_text_color="Custom",
            text_color=(0.9, 0.9, 0.9, 1),
            halign="left"
        ))

        layout.add_widget(icon)
        layout.add_widget(text_box)
        self.add_widget(layout)


class AchievementsApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        Clock.schedule_once(self.load_achievements, 1)
        return Builder.load_string(KV)

    def load_achievements(self, *args):
        data = get_steam_achievements(API_KEY, STEAM_ID, APP_ID)
        achievement_list = self.root.ids.achievements_list
        achievement_list.clear_widgets()

        if "playerstats" in data and "achievements" in data["playerstats"]:
            for ach in data["playerstats"]["achievements"]:
                name = ach.get("name", ach.get("apiname", "Unknown"))
                desc = ach.get("description", "")
                achieved = ach.get("achieved", 0)
                icon_url = ach.get("icon") if achieved else ach.get("icongray")

                if not icon_url:
                    icon_url = "https://via.placeholder.com/64"  # fallback

                print(f"Загрузка иконки: {icon_url}")
                card = AchievementCard(name, desc, icon_url, achieved)
                achievement_list.add_widget(card)
        else:
            print("Нет достижений или ошибка при загрузке данных.")


AchievementsApp().run()
