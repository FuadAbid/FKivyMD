__all__ = ("FDivider",)

import os

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ColorProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.behaviors import DeclarativeBehavior
from kivymd.theming import ThemableBehavior
from fkivymd import uix_path

with open(
    os.path.join(uix_path, "divider", "divider.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class FDivider(DeclarativeBehavior, ThemableBehavior, BoxLayout):
    color = ColorProperty(None)
    divider_length = NumericProperty()
    divider_thickness = NumericProperty(dp(1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.on_orientation)

    def on_orientation(self, *args) -> None:
        if self.orientation == "vertical":
            self.size_hint_x = None
            self.width = self.divider_thickness
        elif self.orientation == "horizontal":
            self.size_hint_y = None
            self.height = self.divider_thickness