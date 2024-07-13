from kivy.lang.builder import Builder
from kivy.properties import NumericProperty, ColorProperty


Builder.load_string('''
<ExtendedBackgroundBehavior>:
    _canvas_height: self.height
    canvas.before:
        Color:
            rgba: 
                ((self.md_bg_color if hasattr(self, "md_bg_color") \
                and self.md_bg_color else [0,0,0,0]) \
                if not self.extended_bg_color else self.extended_bg_color) \
                if abs(self._canvas_width) else[0,0,0,0]
        SmoothRoundedRectangle:
            size:
                [self.width + abs(self._canvas_width) + self._padding, \
                self._canvas_height + self._padding*2] \
                if abs(self._canvas_width) > 0 else [0, 0]
            pos:
                (self.x - self._padding if self._canvas_width > 0 \
                else self.x + self._canvas_width, \
                self.y + (self.height-self._canvas_height)/2 - self._padding)
            radius:
                [self.radius[0] + self._padding] if hasattr(self, "radius") \
                else [(self.height/2) + self._padding]
''')

class ExtendedBackgroundBehavior:
    _canvas_width = NumericProperty(0)
    _canvas_height = NumericProperty(0)
    _padding = NumericProperty(0)
    extended_bg_color = ColorProperty(None)