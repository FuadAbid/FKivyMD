"""
Behaviors/Background Color
==========================

.. note:: The following classes are intended for in-house use of the library.
"""

from __future__ import annotations

__all__ = ("FBackgroundColorBehavior",)

from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import (
    ColorProperty,
    NumericProperty,
    StringProperty,
    VariableListProperty, 
)
from kivy.clock import Clock

Builder.load_string("""
#:import RelativeLayout kivy.uix.relativelayout.RelativeLayout


<FBackgroundColorBehavior>
    canvas.before:
        Color:
            group: "backgroundcolor-behavior-bg-color"
            rgba: self._md_bg_color
        SmoothRoundedRectangle:
            group: "Background_instruction"
            size: self.size
            pos: self.pos if not isinstance(self, RelativeLayout) else (0, 0)
            # FIXME: Sometimes the radius has the value [], which get a
            # `GraphicException:
            #     Invalid radius value, must be list of tuples/numerics` error`
            radius: self.radius if self.radius else [0, 0, 0, 0]
            source: self.background
        Color:
            rgba: self.line_color
        SmoothLine:
            width: root.line_width
            rounded_rectangle:
                [ \
                0,
                0, \
                self.width, \
                self.height, \
                *self.radius, \
                ] \
                if isinstance(self, RelativeLayout) else \
                [ \
                self.x,
                self.y, \
                self.width, \
                self.height, \
                *self.radius, \
                ]
""")


class FBackgroundColorBehavior:
    background = StringProperty()
    radius = VariableListProperty([0], length=4)
    md_bg_color = ColorProperty([0, 0, 0, 0])
    line_color = ColorProperty([0, 0, 0, 0])
    line_width = NumericProperty(1)

    _md_bg_color = ColorProperty([0, 0, 0, 0])
    _shadow_color_ = None
    _first_time = False

    def __init__(self, **kwarg):
        super().__init__(**kwarg)

    def on_md_bg_color(self, instance, color: list | str):
        """Fired when the values of :attr:`md_bg_color` change."""
        has_shadow = False
        if hasattr(self, "shadow_color"):
            has_shadow = True
            if not self._first_time:
                has_shadow = False
                self._first_time = True

            if has_shadow:
                if self._shadow_color_:
                    self.shadow_color = self._shadow_color_.copy()

            
                self._shadow_color_ = self.shadow_color.copy()
                if self.__class__.__name__ != "FSpeedDialButton":
                    self.shadow_color = 0,0,0,0

        def shadow_anim(*args):
            self.shadow_color = [0,0,0,0]
            Animation(shadow_color=self._shadow_color_, 
                    d=self.theme_cls.theme_style_switch_animation_duration, 
                    t="linear").start(self)
        
        if (
            hasattr(self, "theme_cls")
            and self.theme_cls.theme_style_switch_animation
            and self.__class__.__name__ != "MDDropdownMenu"
        ):  
            if has_shadow:
                bg_anim = Animation(
                    _md_bg_color=color,
                    shadow_color=[0,0,0,0],
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t="linear",
                )
                bg_anim.bind(on_complete=shadow_anim)
            else:
                bg_anim = Animation(
                    _md_bg_color=color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t="linear",
                )
            bg_anim.start(self)

        else:
            self._md_bg_color = color
            if has_shadow:
                Clock.schedule_once(shadow_anim)

        # if (
        #     hasattr(self, "theme_cls")
        #     and self.theme_cls.theme_style_switch_animation
        #     and self.__class__.__name__ != "MDDropdownMenu"
        # ):
        #     Animation(
        #         _md_bg_color=color,
        #         d=self.theme_cls.theme_style_switch_animation_duration,
        #         t="linear",
        #     ).start(self)
        # else:
        #     self._md_bg_color = color