from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


class BaseScreen(MDScreen):
    image_size = StringProperty()


KV = '''
<BaseMDNavigationItem>

    MDNavigationItemIcon:
        icon: root.icon

    MDNavigationItemLabel:
        text: root.text


<BaseScreen>

    FitImage:
        
        size_hint: .9, .9
        pos_hint: {"center_x": .5, "center_y": .5}
        radius: dp(24)


MDBoxLayout:
    orientation: "vertical"
    md_bg_color: self.theme_cls.backgroundColor

    MDScreenManager:
        id: screen_manager

        BaseScreen:
            name: "Игры"
            image_size: "1024"

        BaseScreen:
            name: "Мои платины"
            image_size: "800"

        BaseScreen:
            name: "Сообщения"
            image_size: "600"
            
        BaseScreen:
            name: "Мой профиль"
            image_size: "600"


    MDNavigationBar:
        on_switch_tabs: app.on_switch_tabs(*args)

        BaseMDNavigationItem
            icon: "controller"
            text: "Игры"
            active: True

        BaseMDNavigationItem
            icon: "gamepad-circle"
            text: "Мои платины"

        BaseMDNavigationItem:
            icon: "message"
            text: "Сообщения"
        
        BaseMDNavigationItem:
            icon: "account"
            text: "Мой профиль"
'''


class Prog(MDApp):
    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
    ):
        self.root.ids.screen_manager.current = item_text

    def build(self):
        return Builder.load_string(KV)


Prog().run()