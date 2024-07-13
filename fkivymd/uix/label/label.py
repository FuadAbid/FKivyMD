"""
Label
=====

Difference between FLabel and MDLabel:
--------------------------------------

1. Created using 
    FBackgroundColorBehavior instead of BackgroundColorBehavior
    FStateLayerBehavior instead of StateLayerBehavior

2. Fixed Color Implementation:
Giving both custom value text_color and text_color_disabled
results in MDLabel/MDIcon only showing custom text_color, means 
even if the label is disabled, it won't change the color to
text_color_disabled color. But this issue is fixed in FLabel/FIcon.

Example::

    MDLabel:
        text: 'MDLabel'
        theme_text_color: 'Custom'
        text_color: 'red'
        text_color_disabled: 'blue'
        disabled: True

    FLabel:
        text: 'FLabel'
        theme_text_color: 'Custom'
        text_color: 'red'
        text_color_disabled: 'blue'
        disabled: True


2. Label selection feature removed:
Thought it was unnecessary, so removed it.

For More Information on how to use Label 
and change attributes of Label, see::

`KivyMD MDLabel <https://kivymd.readthedocs.io/en/latest/components/label/>`

"""

from __future__ import annotations

__all__ = (
    "FLabel",
    "FIcon",
    "FBadge"
)

import os

from kivy.animation import Animation
from kivy.core.clipboard import Clipboard
from kivy.lang.builder import Builder

from kivy.properties import (
    StringProperty, 
    BooleanProperty, 
    OptionProperty, 
    ColorProperty, 
    ObjectProperty, 
)
from kivy.uix.label import Label

from fkivymd import uix_path
from kivymd.theming import ThemableBehavior
from kivymd.uix import MDAdaptiveWidget
from kivymd.uix.behaviors import (
    DeclarativeBehavior, 
    TouchBehavior,
)
from fkivymd.uix.behaviors import FBackgroundColorBehavior, FStateLayerBehavior

with open(os.path.join(uix_path, "label", "label.kv"), encoding="utf-8") as kvfile:
    Builder.load_string(kvfile.read())


class FLabelBase(
    DeclarativeBehavior,
    ThemableBehavior,
    Label, 
    FBackgroundColorBehavior,
    MDAdaptiveWidget, 
    TouchBehavior,
    FStateLayerBehavior
):
    """
    Label class.

    For more information, see in the
    :class:`~kivymd.uix.behaviors.declarative_behavior.DeclarativeBehavior` and
    :class:`~kivymd.theming.ThemableBehavior` and
    :class:`~FKivyMD.uix.behaviors.backgroundcolor_behavior.BackgroundColorBehavior` and
    :class:`~kivymd.uix.MDAdaptiveWidget` and
    :class:`~kivy.uix.label.Label` and
    :class:`~kivymd.uix.behaviors.touch_behavior.TouchBehavior` and 
    :class: `~FKivyMD.uix.behaviors.state_layer_behavior.FStateLayerBehavior
    classes documentation.

    :Events:
        `on_ref_press`
            Fired when the user clicks on a word referenced with a
            ``[ref]`` tag in a text markup.
        `on_copy`
            Fired when double-tapping on the label.
    """

    allow_copy = BooleanProperty(False)
    """
    Allows you to copy text to the clipboard by double-clicking on the label.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type("on_copy")

    def on_double_tap(self, touch, *args) -> None:
        """Fired by double-clicking on the widget"""

        if self.allow_copy and self.collide_point(*touch.pos):
            Clipboard.copy(self.text)
            self.dispatch("on_copy")

    def on_copy(self, *args) -> None:
        """Fired when double-tapping on the label"""


class FLabel(FLabelBase):
    text_color = ColorProperty(None)
    text_color_disabled = ColorProperty(None)

    font_style = StringProperty("Body")
    """
    Label font style.
    Available vanilla font_style are: `'Display'`, `'Headline'`, `'Title'`,
    `'Label'`, `'Body'``.
    """

    role = OptionProperty("large", options=["large", "medium", "small"])


class FIcon(FLabelBase):
    font_style = StringProperty("Icon")
    role = StringProperty("large")
    icon = StringProperty("blank")
    source = StringProperty(None, allownone=True)
    icon_color = ColorProperty(None)
    icon_color_disabled = ColorProperty(None)

    # FBadge object.
    _badge = ObjectProperty()

    def add_widget(self, widget, index=0, canvas=None):
        if isinstance(widget, FBadge):
            self._badge = widget
        return super().add_widget(widget)
    
    def on_double_tap(self, touch, *args) -> None:
        """Fired by double-clicking on the widget"""

        if self.allow_copy and self.collide_point(*touch.pos):
            Clipboard.copy(self.icon)
            self.dispatch("on_copy")
    

class FBadge(FLabel):
    pass