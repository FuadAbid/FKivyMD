"""
Text Field
==========

The :class:`FTextField` let users enter text into a UI.

FTextField is created following the material design
`Material Design Text field <https://m3.material.io/FKivyMD/text-fields>`


Note
----

It is created using the material system and some behaviors
of KivyMD. So you need to have both Kivy and KivyMD (2.0.0
or above) installed on your machine.

`Kivy <https://kivy.org/>`
`KivyMD <https://kivymd.readthedocs.io/en/latest/index.html>`


Difference between MDTextField(KivyMD) and FTextField(FKivyMD)
--------------------------------------------------------------

1. Implementation:

- MDTextField (KivyMD) example::

    MDTextField:
        mode: "filled"

        MDTextFieldLeadingIcon:
            icon: "magnify"

        MDTextFieldHintText:
            text: "Hint text"

        MDTextFieldHelperText:
            text: "Helper text"
            mode: "persistent"

        MDTextFieldTrailingIcon:
            icon: "information"

        MDTextFieldMaxLengthText:
            max_text_length: 10


- FTextField (FKivyMD) example::

    FTextField:
        style: 'filled'
        hint_text: 'Hint Text'
        helper_text: 'Helper Text'
        leading_icon: 'magnify'
        trailing_icon: 'information'
        max_length: 10


2. Additonal Styles (Line, Text)

- Line Style: 
A line under the text to show text field region::

    FTextField:
        style: 'line'

- Text Style:
Only text with FKivyMD::

    FTextField:
        style: 'text'


3. Add Action Buttons:

You can add leading and trailing action button and if
you want to refer :class:`FTextField` from button, 
use `self._parent`

- Example (KV)::

    FTextField:
        style: 'line'
        hint_text: 'Search'
        
        FTextFieldLeadingButton:
            icon: 'arrow-left'
            on_release: print("Back")

        FTextFieldTrailingButton:
            icon: 'magnify'
            on_release: print(self._parent.text)


- Example (Py)::

    self.text_field = FTextField(
        FTextFieldLeadingButton(
            icon='arrow-left',
            on_release=lambda x: print("Back")
            ), 
        style='line', 
        hint_text='Search'
        )
    
    self.textfield_trailing_button = FTextFieldTrailingButton(
        icon='magnify',
        on_release=lambda x: print(self.text_field.text)
        )

    self.text_field.add_widget(self.textfield_trailing_button)


4. Preserves normal hint text visuality:

By default, if a user enters text, the hint text disappears.
To keep hint text visible even when there is text and 
minimize it on top of text::

    FTextField:
        keep_hint_visible: True


5. Works with different alignment unlike :class:`MDTextField`:

- MDTextField (KivyMD) example::

    MDTextField:
        mode: "outlined"
        halign: 'right' # or 'center'

        MDTextFieldHintText:
            text: "Hint text"


- FTextField (FKivyMD) example::

    FTextField:
        style: 'outlined'
        hint_text: 'Hint Text'
        keep_hint_visible: True
        halign: 'right' # or 'center'


6. Is resizable and works with multiline unlike :class:`MDTextField`:

- MDTextField (KivyMD) example::

    MDTextField:
        mode: "outlined"
        halign: 'right' # or 'center'
        multiline: True

        MDTextFieldHintText:
            text: "Hint text"


- FTextField (FKivyMD) example::

    FTextField:
        style: 'outlined'
        hint_text: 'Hint Text'
        keep_hint_visible: True
        halign: 'right' # or 'center'
        multiline: True
"""


from __future__ import annotations

__all__ = (
    "FTextField",
    "FTextFieldButton",
    "FTextFieldLeadingButton", 
    "FTextFieldTrailingButton"
)

import os
from fkivymd import uix_path
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.properties import (
    StringProperty,
    ColorProperty, 
    NumericProperty,
    VariableListProperty, 
    OptionProperty, 
    BooleanProperty, 
    ObjectProperty
)
from kivy.graphics import Color, Line, InstructionGroup
from kivymd.uix.behaviors import DeclarativeBehavior
from kivymd.theming import ThemableBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from fkivymd.uix.button import FIconButton 
from kivy.metrics import dp
from kivymd.font_definitions import theme_font_styles

with open(
    os.path.join(uix_path, "textfield", "textfield.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class FTextFieldButton(FIconButton):
    _parent = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ripple_alpha = .2
        self.ripple_color = self.theme_cls.primaryColor


class FTextFieldLeadingButton(FTextFieldButton):
    pass


class FTextFieldTrailingButton(FTextFieldButton):
    pass


class FTextFieldLeadingButtonContainer(BoxLayout):
    def add_widget(self, widget, *args, **kwargs):
        if not isinstance(widget, FTextFieldLeadingButton):
            return
        return super().add_widget(widget, *args, **kwargs)
    

class FTextFieldTrailingButtonContainer(BoxLayout):
    def add_widget(self, widget, *args, **kwargs):
        if not isinstance(widget, FTextFieldTrailingButton):
            return
        return super().add_widget(widget, *args, **kwargs)


class FTextField(
    DeclarativeBehavior, 
    ThemableBehavior,
    TextInput
):
    """
    Textfield class.

    For more information, see in the
    :class:`~kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior` and
    :class:`~kivymd.theming.ThemableBehavior` and
    :class:`~kivy.uix.textinput.TextInput` and
    classes documentation.
    """

    fill_color = ColorProperty(None)
    """Background color in 'filled' mode when text field is out of focus"""

    fill_color_focus = ColorProperty(None)
    """Background color in 'filled' mode when text field has focus"""

    text_color = ColorProperty(None)
    """Text color when text field is out of focus"""

    text_color_focus = ColorProperty(None)
    """Text color when text field has focus"""
    
    text_color_disabled = ColorProperty(None)
    """Text color when text field is disabled"""
    
    hint_text_color_focus = ColorProperty(None)
    """Hint text color when text field has focus"""
    
    hint_text_color_disabled = ColorProperty(None)
    """Hint text color when text field is disabled"""
    
    leading_icon_color = ColorProperty(None)
    """Leading icon color when text field is out of focus"""

    leading_icon_color_focus = ColorProperty(None)
    """Leading icon color when text field has focus"""

    trailing_icon_color = ColorProperty(None)
    """Trailing icon color when text field has focus"""

    trailing_icon_color_focus = ColorProperty(None)
    """Trailing icon color when text field has focus"""

    button_icon_color = ColorProperty(None)
    """Button icon color when text field is out of focus"""

    button_icon_color_focus = ColorProperty(None)
    """Button icon color when text field has focus"""

    border_color = ColorProperty(None)
    """Border color in 'outlined' mode when text field is out of focus"""

    border_color_focus = ColorProperty(None)
    """Border color in 'outlined' mode when text field has focus"""

    line_color = ColorProperty(None)
    """
    Line color in 'filled' (active indicator) and 'line' (underline)
    mode when text field is out of focus
    """

    line_color_focus = ColorProperty(None)
    """
    Line color in 'filled' (active indicator) and 'line' (underline)
    mode when text field has focus
    """

    helper_text_color = ColorProperty(None)
    """Helper text color when text field is out of focus"""

    helper_text_color_focus = ColorProperty(None)
    """Helper text color when text field has focus"""

    max_length_color = ColorProperty(None)
    """Max length text color when text field is out of focus"""

    max_length_color_focus = ColorProperty(None)
    """Max length text color when text field has focus"""

    leading_icon = StringProperty()
    """Leading icon name"""

    trailing_icon = StringProperty()
    """Trailing icon name"""

    button_divider = BooleanProperty(False)
    """
    Button divider. If True then a divider between text region
    and trailing buttons will appear.
    """

    helper_text = StringProperty()
    """Helper text to show more information about text field"""

    max_length = NumericProperty()
    """
    Max text length number. If a number is set, user can
    not type more than that number of characters.
    """

    font_style = StringProperty("Body")
    """
    Name of the style for the input text.
    `Font style names <https://kivymd.readthedocs.io/en/latest/components/label/#all-styles>`
    """

    role = StringProperty("large")
    """
    Role of font style.
    `Font style roles <https://kivymd.readthedocs.io/en/latest/components/label/#all-styles>`

    """
    style = OptionProperty("outlined", options=['outlined', 'filled', 'line', 'text'])
    """
    Text field style. Available options are: 
    `'outlined'`, `'filled'`, `'line'`, `'text'`.
    """

    helper_text_style = OptionProperty("persistent", options=["persistent", "on_focus"])
    """
    Helper text mode. Available options are: 
    `'persistent'`, `'on_focus'`.
    """

    radius = VariableListProperty()
    """The corner radius for a text field in `filled/outlined` style"""

    button_radius = VariableListProperty()
    """FTextFieldLeadingButton and FTextFieldTrailingButton radius"""

    keep_hint_visible = BooleanProperty(False)
    """
    Keep the hint text visible or not when there is text in text field.
    If True, hint text will minimize and stay above text, otherwise
    hint text will disappear if there's text in text field.
    """


    # Text Region Boundary Box
    _bbox = VariableListProperty()
    # Part of the hint text that will appear
    _extracted_hint_text = StringProperty()
    # Full hint text that will be stored at first
    _original_hint_text = ''

    # Top left and right line points used while animating hint text
    _top_left_line_pos = NumericProperty(dp(32))
    _top_right_line_pos = NumericProperty(dp(32))

    # Active indicator thickness
    _outline_thickness = NumericProperty(dp(1))
    # Base padding without any abstractions
    _component_padding = NumericProperty(dp(15))
    # Amount of height to reduce to fit hint text in textfield region
    _outlined_reduce_height = NumericProperty()
    # Increased pad amount to make text appear down to hint text
    _filled_pad_downside = NumericProperty()
    # Minimized width of hint text, used to calculate top lines positions
    _minimized_hint_text_width = 0
    # Under line color, used to animate line in 'line' style
    _under_line_color = [0, 0, 0, 0]

    # Buttons
    _leading_button_container = FTextFieldLeadingButtonContainer()
    _trailing_button_container = FTextFieldTrailingButtonContainer()
    _leading_buttons_added = False
    _trailing_buttons_added = False
    _leading_buttons = []
    _trailing_buttons = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update buttons position when created using python
        Clock.schedule_once(lambda x: self._update_top_outline_pos(), 1.05)

    def add_widget(self, widget, *args, **kwargs):
        if isinstance(widget, FTextFieldTrailingButton):
            widget._parent = self
            self._trailing_button_container.add_widget(widget, *args, **kwargs)
            self._trailing_buttons.append(widget)
            return
        if isinstance(widget, FTextFieldLeadingButton):
            widget._parent = self
            self._leading_button_container.add_widget(widget, *args, **kwargs)
            self._leading_buttons.append(widget)
            return
        return super().add_widget(widget, *args, **kwargs)

    def _add_buttons(self, category): # category: lead or trail
        if category == 'trail':
            if len(self._trailing_buttons) and self._trailing_button_container:
                Window.add_widget(self._trailing_button_container)
                self._trailing_buttons_added = True
        elif category == 'lead':
            if len(self._leading_buttons) and self._leading_button_container:
                Window.add_widget(self._leading_button_container)
                self._leading_buttons_added = True

    def _remove_buttons(self, category): # category: lead or trail
        if category == 'trail':
            if (len(self._trailing_button_container.children)
                and self._trailing_buttons_added):
                Window.remove_widget(self._trailing_button_container)
                self._trailing_buttons_added = False
        elif category == 'lead':
            if (len(self._leading_button_container.children)
                and self._leading_buttons_added):
                Window.remove_widget(self._leading_button_container)
                self._leading_buttons_added = False

    def _get_hint_text_pos(self) -> tuple:
        x = y = 0
        text_width = self.width - self.padding[0] - self.padding[2]
        if self.style == 'outlined':
            if self.text or self.focus:
                y = (self.y + self.height 
                     - self.hint_text_label.texture_size[1])
                
                if self.halign == 'auto' or self.halign == 'left':
                    x = self.x + dp(15)
                elif self.halign == 'center':
                    x = (self.x + (self.width/2 - 
                         self.hint_text_label.texture_size[0]/2))
                elif self.halign == 'right':
                    x = (self.x + self.width - dp(15) - 
                         self.hint_text_label.texture_size[0])
            
            else:
                y = (self.y + self.height - self.padding[1]
                     - self.hint_text_label.texture_size[1])
                
                if self.halign == 'auto' or self.halign == 'left':
                    x = self.x + self.padding[0]
                elif self.halign == 'center':
                    x = (self.x + self.padding[0] + (text_width/2 - 
                         self.hint_text_label.texture_size[0]/2))
                elif self.halign == 'right':
                    x = (self.x + self.width - self.padding[2] - 
                         self.hint_text_label.texture_size[0])
        
        else:
            if self.text or self.focus:
                y = (self.y + self.height - dp(8) 
                     - self.hint_text_label.texture_size[1])
                
                if self.halign == 'auto' or self.halign == 'left':
                    x = self.x + self.padding[0]
                elif self.halign == 'center':
                    x = (self.x + self.padding[0] + (text_width/2 - 
                         self.hint_text_label.texture_size[0]/2))
                elif self.halign == 'right':
                    x = (self.x + self.width - self.padding[2] 
                         - self.hint_text_label.texture_size[0])
            
            else:
                y = (self.y + self.height - self.padding[1]
                     - self.hint_text_label.texture_size[1]
                     + self._filled_pad_downside)
                
                if self.halign == 'auto' or self.halign == 'left':
                    x = self.x + self.padding[0]
                elif self.halign == 'center':
                    x = (self.x + self.padding[0] + (text_width/2 - 
                         self.hint_text_label.texture_size[0]/2))
                elif self.halign == 'right':
                    x = (self.x + self.width - self.padding[2] - 
                         self.hint_text_label.texture_size[0])
                    
        return int(x), int(y)

    def _add_hint_text_label(self, text:str) -> None:
        self._extracted_hint_text = text
        hint_text_rectangle = self.canvas.after.get_group("hint-text-rectangle")[0]
        self.hint_text_label.texture_update()
        hint_text_rectangle.texture = self.hint_text_label.texture
        hint_text_rectangle.size = self.hint_text_label.texture_size
        hint_text_rectangle.pos = self._get_hint_text_pos()
        self._refresh_hint_text()

    def _remove_hint_text_label(self, *_) -> None:
        self._extracted_hint_text = ''
        self.hint_text_label.texture_update()
        hint_text_rectangle = self.canvas.after.get_group("hint-text-rectangle")[0]
        hint_text_rectangle.texture = None
        hint_text_rectangle.size = [0,0]
        self._refresh_hint_text()

    def _update_hint_canvas(self):
        self.hint_text_label.texture_update()
        hint_text_rectangle = self.canvas.after.get_group("hint-text-rectangle")[0]
        hint_text_rectangle.texture = self.hint_text_label.texture
        Animation(pos=hint_text_rectangle.pos, d=0).start(hint_text_rectangle)
        return hint_text_rectangle
    
    def _get_top_outline_pos(self):
        _top_left_line_pos = _top_right_line_pos = 0
        if (self.keep_hint_visible and self._extracted_hint_text and (self.text or self.focus)):
            hint_pos = self._get_hint_text_pos()[0]
            label_width = self.hint_text_label.texture_size[0]
            _top_left_line_pos = hint_pos - dp(5)
            _top_right_line_pos = hint_pos + label_width + dp(5)
        else:
            label_width_half = self._minimized_hint_text_width / 2
            x = 0
            if self.halign == 'auto' or self.halign == 'left':
                x = self.x + dp(15) + label_width_half + dp(5)
            elif self.halign == 'center':
                x = (self.x + (self.width/2 - 
                        label_width_half)
                        + label_width_half + dp(5))
            elif self.halign == 'right':
                x = (self.x + self.width - dp(15) - 
                        label_width_half + dp(5))
            
            _top_left_line_pos = _top_right_line_pos = x
        
        return _top_left_line_pos, _top_right_line_pos

    def _update_top_outline_pos(self):
        if self.keep_hint_visible and self._extracted_hint_text:
            if self.text or self.focus:
                hint_pos = self._get_hint_text_pos()[0]
                label_width = self.hint_text_label.texture_size[0]
                self._top_left_line_pos = hint_pos - dp(5)
                self._top_right_line_pos = hint_pos + label_width + dp(5)
            else:
                self._top_left_line_pos, self._top_right_line_pos = self._get_top_outline_pos()
    
    def on_hint_text(self, *args):
        if self.hint_text:
            self._original_hint_text = self.hint_text
            if self.keep_hint_visible:
                Clock.schedule_once(lambda x: self._add_hint_text_label(
                    self._hint_text_lines[0]))
                self.hint_text = ''

    def on_keep_hint_visible(self, *_):
        if self.keep_hint_visible and not self._extracted_hint_text:
            text = self.hint_text or self._original_hint_text
            self.hint_text = ''
            Clock.schedule_once(lambda x: self._add_hint_text_label(
                self._split_smart(text)[0][0]))
        else:
            self.hint_text = self._original_hint_text
            Clock.schedule_once(lambda x: self._remove_hint_text_label())

    def on_width(self, *_):
        if self.keep_hint_visible and self._original_hint_text:
            Clock.schedule_once(lambda x: self._add_hint_text_label(
                self._split_smart(self._original_hint_text)[0][0]))
            if self.style == 'outlined':
                self._update_top_outline_pos()

    def on_focus(self, *_):
        if self.keep_hint_visible and self._extracted_hint_text:
            self.hint_text_label.font_size = (
                theme_font_styles['Body']['small']['font-size']
                if self.text or self.focus else
                self.font_size)
            hint_text_rectangle = self._update_hint_canvas()
            self._minimized_hint_text_width = hint_text_rectangle.size[0]
            pos = self._get_hint_text_pos()

            Animation(
                size=self.hint_text_label.texture_size,
                pos=pos, d=.2, t='out_quad'
            ).start(hint_text_rectangle)

            if self.style == 'outlined':
                top_line_pos = self._get_top_outline_pos()
                self.set_space_in_line(
                    top_line_pos[0], top_line_pos[1]
                )

        if self.style == 'line':
            line_points = self.canvas.before.get_group("line-style-line")[0].points
            ini_x = self.center_x
            ini_y = line_points[1]

            ini_points = ([ini_x, ini_y, ini_x, ini_y] 
                          if self.focus else 
                          line_points)
            final_points = (line_points if self.focus else 
                            [ini_x, ini_y, ini_x, ini_y])
            
            self.under_line_group = InstructionGroup()
            self.under_line_group.add(
                Color(rgba=self.line_color_focus)
            )
            self._line = Line(
                        group='line-style-line2', 
                        width=dp(1), 
                        points=ini_points
                    )
            self.under_line_group.add(self._line)
            self.canvas.before.add(self.under_line_group)
            self._under_line_color = self.line_color[:-1] + [.3]
            anim = Animation(points=final_points, d=.15)
            anim.bind(on_complete=self._remove_under_line2)
            anim.start(self._line)

    def _remove_under_line2(self, *_):
        if hasattr(self, '_line'):
            self.canvas.before.remove(self.under_line_group)
        self.canvas.before.get_group("line-style-line-color")[0].rgba = (
            self.line_color_focus 
            if self.focus else 
            self.line_color[:-1] + [.3]
        )

    def set_space_in_line(
        self, left_width: float | int, right_width: float | int
    ) -> None:
        Animation(_top_left_line_pos=left_width, d=0.15, t="out_quad").start(self)
        Animation(_top_right_line_pos=right_width, d=0.15, t="out_quad").start(self)

    def on_kv_post(self, base_widget):
        if self.opacity > 0:
            self.on_opacity()
        return super().on_kv_post(base_widget)

    def on_pos(self, *_):
        if self._trailing_button_container:
            setattr(self._trailing_button_container, 'pos', \
            [self.x + self.width - self._trailing_button_container.width, \
            self.y + self.height - self._trailing_button_container.height 
            - self._outlined_reduce_height])
            
        if self._leading_button_container: 
            setattr(self._leading_button_container, 'pos', \
            [self.x, self.y + self.height - 
            self._leading_button_container.height
            - self._outlined_reduce_height])
            
        if self.keep_hint_visible and self._extracted_hint_text:
            hint_text_rectangle = self.canvas.after.get_group("hint-text-rectangle")[0]
            hint_text_rectangle.pos = self._get_hint_text_pos()

            if self.style == 'outlined':
                self._update_top_outline_pos()

    def on_size(self, *_):
        Clock.schedule_once(self.on_pos)
    
    def on_opacity(self, *_):
        if self.opacity > 0:
            if self._trailing_buttons_added is False:
                Clock.schedule_once(lambda x: self._add_buttons('trail'))
            if self._leading_buttons_added is False:
                Clock.schedule_once(lambda x: self._add_buttons('lead'))
        else:
            Clock.schedule_once(lambda x: self._remove_buttons('lead'))
            Clock.schedule_once(lambda x: self._remove_buttons('trail'))

        super().on_opacity(self, self.opacity)