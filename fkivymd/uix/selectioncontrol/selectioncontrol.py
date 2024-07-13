from __future__ import annotations

__all__ = ('FCheckBox')

from kivy.uix.behaviors import ToggleButtonBehavior
from fkivymd.uix.label import FIcon
from kivy.properties import AliasProperty, ColorProperty, StringProperty

import os
from FKivyMD import uix_path
from kivy.lang.builder import Builder

with open(
    os.path.join(uix_path, "selectioncontrol", "selectioncontrol.kv"),
    encoding="utf-8",
) as kv_file:
    Builder.load_string(kv_file.read())


class FCheckBox(
    ToggleButtonBehavior, 
    FIcon
):
    checkbox_icon_normal = StringProperty("checkbox-blank-outline")
    checkbox_icon_down = StringProperty("checkbox-marked")
    radio_icon_normal = StringProperty("circle-outline")
    radio_icon_down = StringProperty("record-circle-outline")
    color_active = ColorProperty(None)
    color_inactive = ColorProperty(None)
    color_disabled = ColorProperty(None)
    _current_color = ColorProperty([0.0, 0.0, 0.0, 0.0])

    def _get_active(self):
        return self.state == 'down'

    def _set_active(self, value):
        self.state = 'down' if value else 'normal'

    active = AliasProperty(
        _get_active, _set_active, bind=('state', ), cache=True)
    
    def __init__(self, **kwargs):
        self.fbind('state', self._on_state)
        self.fbind('state', self.update_icon)
        super().__init__(**kwargs)
        self.bind(
            checkbox_icon_normal=self.update_icon,
            checkbox_icon_down=self.update_icon,
            radio_icon_normal=self.update_icon,
            radio_icon_down=self.update_icon,
            group=self.update_icon,
        )
        self.update_icon()

    def _on_state(self, instance, value):
        if self.group and self.state == 'down':
            self._release_group(self)

    def on_group(self, *largs):
        super().on_group(*largs)
        if self.active:
            self._release_group(self)
        self.update_icon()

    def update_icon(self, *args) -> None:
        if self.state == "down":
            self.icon = (
                self.radio_icon_down
                if self.group and self.group not in ["root", "child"]
                else self.checkbox_icon_down
                if self.group != "root"
                else self.checkbox_icon_normal
            )
        else:
            self.icon = (
                self.radio_icon_normal
                if self.group and self.group not in ["root", "child"]
                else self.checkbox_icon_normal
            )