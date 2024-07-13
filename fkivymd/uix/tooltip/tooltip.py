import os

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    BoundedNumericProperty,
    NumericProperty,
    BooleanProperty,
    OptionProperty, 
    ObjectProperty
)
from kivy.uix.boxlayout import BoxLayout
from fkivymd.uix.card import FFrame

from kivymd.uix.behaviors.state_layer_behavior import StateLayerBehavior
from fkivymd.uix.button import FButton
from fkivymd.uix.label import FLabel
from fkivymd import uix_path
from kivymd.material_resources import DEVICE_TYPE
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import (
    TouchBehavior,
    ScaleBehavior,
    DeclarativeBehavior,
    BackgroundColorBehavior,
    CommonElevationBehavior,
)

with open(
    os.path.join(uix_path, "tooltip", "tooltip.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())

# size_min_y = 24dp
# size_max_x = Window.size
# container, unrestricted child widgets

class FTooltip(TouchBehavior, FFrame):
    style = OptionProperty("plain", options=['plain', 'rich'])
    theme_size = OptionProperty("Primary", options=['Primary', 'Custom'])
    tooltip_parent = ObjectProperty()
    is_showing = BooleanProperty(False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.parent:
            self.tooltip_parent = self.parent
            self.tooltip_parent.fbind("size", self.adjust_pos)
            self.tooltip_parent.fbind("pos", self.adjust_pos)
            self._parent = None
        self.register_event_type("on_open")
        self.register_event_type("on_dismiss")

    def delete_clock(self, widget, touch, *args):
        if self.collide_point(touch.x, touch.y) and touch.grab_current:
            try:
                Clock.unschedule(touch.ud["event"])
            except KeyError:
                pass
            self.on_leave()

    def show(self, *args):
        self.is_showing = True
        self.adjust_pos()

    def dismiss(self, *args):
        pass

    def adjust_pos(self, *args):
        if self.is_showing:
            p = self.tooltip_parent
            parent_bbox = p.x, p.y, p.width, p.height