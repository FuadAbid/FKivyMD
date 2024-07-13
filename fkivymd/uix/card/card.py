from __future__ import annotations

__all__ = (
    "FFrame"
    "FCard", 
    "FCardSwipe",
    "FCardSwipeFront"
)

import os

from kivy.animation import Animation
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.properties import (
    NumericProperty,
    OptionProperty,
    StringProperty,
    ColorProperty,
    BooleanProperty
)
from kivy import platform
from fkivymd import uix_path
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import (
    DeclarativeBehavior, 
    RectangularRippleBehavior
)
from fkivymd.uix.behaviors import (
    FCommonElevationBehavior, 
    FBackgroundColorBehavior, 
    FStateLayerBehavior
)

with open(
    os.path.join(uix_path, "card", "card.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read(), filename="FCard.kv")


class FFrame(
    DeclarativeBehavior, 
    ThemableBehavior, 
    FBackgroundColorBehavior, 
    FCommonElevationBehavior, 
    RelativeLayout
):
    style = OptionProperty("filled", options=("filled", "elevated", "outlined"))
    md_bg_color_disabled = ColorProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.on_disabled(self, self.disabled))

    def shadow_update(self, *args):
        if self.style == "elevated":
            if self.disabled:
                self.shadow_color = (self.theme_cls.shadowColor[:-1] + [.5]
                                    if self.theme_shadow_color == "Primary"
                                    else self.shadow_color[:-1] + [.5])
            else:
                self.shadow_color = (self.theme_cls.shadowColor if
                                    self.theme_shadow_color == "Primary" 
                                    else self.shadow_color)
        else:
            self.shadow_color = self.theme_cls.transparentColor
            
    def on_disabled(self, instance, value):
        self.shadow_update()
        if value:
            self.on_md_bg_color(instance, self.md_bg_color 
                                if not self.md_bg_color_disabled
                                else self.md_bg_color_disabled)
        else:
            self.on_md_bg_color(instance, self.md_bg_color)


class FCard(
    RectangularRippleBehavior, 
    FStateLayerBehavior, 
    ButtonBehavior,
    FFrame
):
    ripple_effect = BooleanProperty(False)

    def on_press(self, *args) -> None:
        """Fired when the button is pressed."""

        self._on_press(args)

    def on_release(self, *args) -> None:
        """
        Fired when the button is released
        (i.e. the touch/click that pressed the button goes away).
        """

        self._on_release(args)

    def set_properties_widget(self) -> None:
        """Fired `on_release/on_press/on_enter/on_leave` events."""

        super().set_properties_widget()

        if not self.disabled:
            if self._state == self.state_hover and self.focus_behavior:
                self._elevation_level = self.elevation_level
                self._shadow_softness = self.shadow_softness
                self._bg_color = self.md_bg_color

                if self.style in ["filled", "outlined"]:
                    if self.theme_elevation_level == "Primary":
                        self.elevation_level = 0
                    if self.theme_shadow_softness == "Primary":
                        self.shadow_softness = 0
                else:
                    if self.theme_elevation_level == "Primary":
                        self.elevation_level = 2
                    if self.theme_shadow_softness == "Primary":
                        self.shadow_softness = dp(4)
                    if self.theme_shadow_offset == "Primary":
                        self.shadow_offset = [0, -2]
            elif self._state == self.state_press:
                if self.theme_elevation_level == "Primary":
                    self.elevation_level = 1
                if self.theme_shadow_softness == "Primary":
                    self.shadow_softness = 0
            elif not self._state:
                if self.theme_elevation_level == "Primary":
                    self.elevation_level = 1
                if self.theme_shadow_softness == "Primary":
                    self.shadow_softness = 0
                if self.theme_shadow_offset == "Primary":
                    self.shadow_offset = [0, -2]
                self.md_bg_color = self._bg_color


class FCardSwipe(MDRelativeLayout):
    both_sides_slide = False
    anchor = OptionProperty("left", options=("left", "right"))
    opening_transition = StringProperty("out_cubic")
    closing_transition = StringProperty("out_sine")
    opening_time = NumericProperty(0.2)
    closing_time = NumericProperty(0.2)
    _is_closed = True
    _front_widget = None
    
    def __init__(self, *args, **kwargs):
        self.register_event_type("on_left_swipe_complete")
        self.register_event_type("on_right_swipe_complete")
        super().__init__(*args, **kwargs)
        #self.size_hint = None, None

    def add_widget(self, widget, index=0, canvas=None):
        if isinstance(widget, FCardSwipeFront):
            if self._front_widget:
                return
            self._front_widget = widget
        
        return super().add_widget(widget)

    def on_left_swipe_complete(self, *args):
        """Fired when a swipe of card is completed."""

    def on_right_swipe_complete(self, *args):
        """Fired when a swipe of card is completed."""

    def on_touch_move(self, touch):
        if self.collide_point(touch.x, touch.y):
            if self._front_widget:
                self._front_widget.x += touch.dx
                if not self.both_sides_slide:
                    if self.anchor == "left" and self._front_widget.x < 0:
                        self._front_widget.x = 0
                    elif self.anchor == "right" and self._front_widget.right > self.width:
                        self._front_widget.right = self.width

        return super().on_touch_move(touch)
                
    def on_touch_up(self, touch):
        if self._front_widget:
            del_x_percent = self._front_widget.x / self.width
            if del_x_percent:
                def get_anim(side, action): # side: ['left', 'right'], action: ['close', 'open']
                    if action == 'open':
                        duration = self.opening_time
                        transition = self.opening_transition
                        dest = self.width if side == "left" else -self.width
                    else:
                        duration = self.closing_time
                        transition = self.closing_transition
                        dest = 0
                    anim = Animation(x=dest, d=duration, t=transition)
                    if action == "open":
                        anim.bind(on_complete=self._on_swipe_complete)
                    return anim
                
                if not self.both_sides_slide:
                    side = self.anchor
                else:
                    side = 'left' if del_x_percent > 0 else 'right'

                action = 'open' if abs(del_x_percent) > .33 else 'close'
                anim = get_anim(side, action)
                anim.start(self._front_widget)

        return super().on_touch_up(touch)

    def _on_swipe_complete(self, *args):
        if self._front_widget.x == self.width:
            self.dispatch("on_left_swipe_complete")
        else:
            self.dispatch("on_right_swipe_complete")



class FCardSwipeFront(FCard):
    ripple_effect = False