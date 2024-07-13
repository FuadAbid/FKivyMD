from __future__ import annotations

__all__ = ("FCommonElevationBehavior",)

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    BoundedNumericProperty,
    ColorProperty,
    ListProperty,
    NumericProperty,
    VariableListProperty,
    DictProperty,
)

Builder.load_string(
    """
<FCommonElevationBehavior>
    canvas.before:
        Color:
            #rgba: self._shadow_color[:3] + [self._shadow_color[3]*(1/(1+100*(.8**((self.opacity-.7)*100))))]
            rgba: self.shadow_color
        BoxShadow:
            pos: self.pos if not isinstance(self, RelativeLayout) else (0, 0)
            size: self.size
            offset: self.shadow_offset
            spread_radius: -(self.shadow_softness), -(self.shadow_softness)
            blur_radius: self.elevation_levels[self.elevation_level]
            border_radius:
                (self.radius if hasattr(self, "radius") and self.radius else [0, 0, 0, 0]) \
                if self.shadow_radius == [0.0, 0.0, 0.0, 0.0] else \
                self.shadow_radius
"""
)


class FCommonElevationBehavior:
    elevation_level = BoundedNumericProperty(0, min=0, max=5)
    """Elevation level (values from 0 to 5)"""

    elevation_levels = DictProperty(
        {
            0: 0,
            1: dp(8),
            2: dp(12),
            3: dp(16),
            4: dp(20),
            5: dp(24),
        }
    )
    """
    Elevation is measured as the distance between components along the z-axis
    in density-independent pixels (dps)
    """

    elevation = BoundedNumericProperty(0, min=0, errorvalue=0)
    """Elevation of the widget"""

    shadow_radius = VariableListProperty([0], length=4)
    """
    Radius of the corners of the shadow.

    .. versionadded:: 1.1.0

    You don't have to use this parameter.
    The radius of the elevation effect is calculated automatically one way
    or another based on the radius of the parent widget, for example:

    .. code-block:: python

        from kivy.lang import Builder

        from kivymd.app import MDApp

        KV = '''
        MDScreen:

            MDCard:
                radius: dp(12), dp(46), dp(12), dp(46)
                size_hint: .5, .3
                pos_hint: {"center_x": .5, "center_y": .5}
                elevation: 2
                shadow_softness: 4
                shadow_offset: (2, -2)
        '''


        class Test(MDApp):
            def build(self):
                return Builder.load_string(KV)


        Test().run()

    .. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/shadow-radius.png
        :align: center

    :attr:`shadow_radius` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `[0, 0, 0, 0]`.
    """

    shadow_softness = NumericProperty(0.0)
    """Softness of the shadow"""

    shadow_offset = ListProperty((0, 0))
    """Offset of the shadow"""

    shadow_color = ColorProperty([0, 0, 0, 0.6])
    """Color of the shadow"""
