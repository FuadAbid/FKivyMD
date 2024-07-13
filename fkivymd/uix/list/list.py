from __future__ import annotations

__all__ = (
    "FList", 
    "FListItem", 
    "FListItemLeadingAvatar", 
    "FListItemLeadingText", 
    "FListItemLeadingIcon", 
    "FListItemLeadingThumbnail"
    "FListItemHeadlineText", 
    "FListItemSupportingText", 
    "FListItemTertiaryText", 
    "FListItemTrailingText", 
    "FListItemTrailingCheckBox", 
    "FListItemTrailingIcon"
)

import os

from kivy.lang.builder import Builder
from fkivymd import uix_path
from kivy.properties import (
    NumericProperty, 
    ColorProperty,
    BooleanProperty, 
    ObjectProperty
)
from kivy import platform
from kivymd.uix.behaviors import (
    DeclarativeBehavior, 
    CircularRippleBehavior
)
from fkivymd.uix.behaviors import FBackgroundColorBehavior
from kivymd.uix import MDAdaptiveWidget
from kivy.clock import Clock
from kivymd.uix.behaviors.focus_behavior import FocusBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivymd.theming import ThemableBehavior
from kivy.uix.boxlayout import BoxLayout
from fkivymd.uix.label import FLabel
from fkivymd.uix.selectioncontrol import FCheckBox
from fkivymd.uix.button import FIconButton
from kivy.uix.image import Image
from kivymd.uix.fitimage import FitImage
from kivy.uix.gridlayout import GridLayout


with open(
    os.path.join(uix_path, "list", "list.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class StateLayerBehavior(FocusBehavior):
    state_layer_color = ColorProperty([0, 0, 0, 0])
    state_hover = NumericProperty(0.04)
    state_press = NumericProperty(0.12)
    state_drag = NumericProperty(0.16)

    _state = 0.0
    _bg_color = (0, 0, 0, 0)
    _is_already_disabled = False
    _shadow_softness = [0, 0]
    _elevation_level = 0

    def set_properties_widget(self) -> None:
        """Fired `on_release/on_press/on_enter/on_leave` events."""

        if not self.disabled:
            self._restore_properties()
            self._set_state_layer_color()

    def on_disabled(self, instance, value) -> None:
        """Fired when the `disabled` value changes."""
        if value and not self._is_already_disabled:
            self._is_already_disabled = True
            if isinstance(self, FListItem):
                self.state_layer_color = (
                    self.theme_cls.onSurfaceColor[:-1] + [0.38]
                    if not self.md_bg_color_disabled
                    else self.md_bg_color_disabled)

        elif not value and self._is_already_disabled:
            self.state_layer_color = self.theme_cls.transparentColor
            self._is_already_disabled = False

    def on_enter(self) -> None:
        """Fired when mouse enter the bbox of the widget."""

        self._state = self.state_hover
        self.set_properties_widget()

    def on_leave(self) -> None:
        """Fired when the mouse goes outside the widget border."""

        self._state = 0.0
        self.set_properties_widget()

    def _on_release(self, *args):
        """
        Fired when the button is released
        (i.e. the touch/click that pressed the button goes away).
        """

        if platform in ["android", "ios"]:
            self._state = 0.0
            self.set_properties_widget()
        else:
            self.on_enter()

    def _on_press(self, *args):
        """Fired when the button is pressed."""

        self._state = self.state_press
        self.set_properties_widget()

    def _restore_properties(self):
        if self._state == self.state_hover and self.focus_behavior:
            if hasattr(self, "elevation_level"):
                self._elevation_level = self.elevation_level
            if hasattr(self, "shadow_softness"):
                self._shadow_softness = self.shadow_softness
            if hasattr(self, "md_bg_color"):
                self._bg_color = self.md_bg_color
        elif not self._state:
            if hasattr(self, "elevation_level"):
                self.elevation_level = self._elevation_level
            if hasattr(self, "shadow_softness"):
                self.shadow_softness = self._shadow_softness
            if hasattr(self, "bg_color"):
                self.bg_color = self._md_bg_color
    
    def _get_target_color(self):
        target_color = None

        if not self.disabled:
            self._restore_properties()
            if isinstance(self, FListItem):
                target_color = self.theme_cls.onSurfaceColor

        return target_color

    def _set_state_layer_color(self):
        target_color = self._get_target_color()
        if target_color:
            if self._state == self.state_hover and self.focus_behavior:
                if (
                    not self.focus_color
                    or self.theme_cls.dynamic_color
                    and self.theme_focus_color == "Primary"
                ):
                    self.state_layer_color = target_color[:-1] + [
                        self._state
                    ]
                else:
                    self.state_layer_color = self.focus_color
            elif self._state == self.state_press:
                self.state_layer_color = target_color[:-1] + [self._state]
            elif not self._state:
                self.state_layer_color = target_color[:-1] + [self._state]


def is_widgets_ordered(source, target):
    ordered_target = sorted(target, key=lambda x: source.index(type(x).__name__))
    if target == ordered_target:
        return True
    return False

def has_unique_widgets(widgets):
    return len(widgets) == len(set([type(x).__name__ for x in widgets]))


class FListException(BaseException):
    pass

class FList(
    DeclarativeBehavior, 
    ThemableBehavior, 
    FBackgroundColorBehavior,
    GridLayout,
    MDAdaptiveWidget
):
    _list_vertical_padding = NumericProperty("8dp")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adaptive_height = True

class FListItem(
    DeclarativeBehavior,
    FBackgroundColorBehavior,
    ButtonBehavior, 
    ThemableBehavior,
    StateLayerBehavior, 
    BoxLayout):

    divider = BooleanProperty(False)
    divider_color = ColorProperty([0,0,0,0])
    md_bg_color_disabled = ColorProperty([0,0,0,0])

    def add_widget(self, widget, *args, **kwargs):
        if isinstance(widget, 
                      (FListItemHeadlineText, 
                       FListItemSupportingText, 
                       FListItemTertiaryText)):
            self.ids.text_container.add_widget(widget)
        elif isinstance(widget, 
                        (FListItemLeadingAvatar, 
                         FListItemLeadingText, 
                         FListItemLeadingIcon, 
                         FListItemLeadingThumbnail)):
            if isinstance(widget, (FListItemLeadingAvatar, 
                                   FListItemLeadingThumbnail)):
                widget._list_item = self
            self.ids.leading_container.add_widget(widget)
            Clock.schedule_once(
                    lambda x: self._set_with_container(
                        self.ids.leading_container, widget
                    )
                )
        elif isinstance(widget, 
                        (FListItemTrailingText, 
                         FListItemTrailingCheckBox, 
                         FListItemTrailingIcon)):
            self.ids.trailing_container.add_widget(widget)
            Clock.schedule_once(
                    lambda x: self._set_with_container(
                        self.ids.trailing_container, widget
                    )
                )
        elif widget.__class__.__name__.endswith('Container'):
            super().add_widget(widget, *args, **kwargs)
            
    def _set_with_container(self, container, widget):
        container.width = widget.width


class FListLeadingContainer(BoxLayout):
    def add_widget(self, widget, *args, **kwargs):
        if len(self.children) == 1:
            raise FListException("FListItem can't contain more than 1 lead widget")
        elif not isinstance(widget, (FListItemLeadingAvatar, 
                                     FListItemLeadingText, 
                                     FListItemLeadingIcon, 
                                     FListItemLeadingThumbnail)):
            return
        return super().add_widget(widget, *args, **kwargs)


class FListTextContainer(BoxLayout):
    possible_widgets = ['FListItemHeadlineText', 'FListItemSupportingText', 'FListItemTertiaryText']
    def add_widget(self, widget, *args, **kwargs):
        if len(self.children) == 3:
            raise FListException("FListItem can't contain more than 3 text widgets")
        elif not isinstance(widget, (FListItemHeadlineText, 
                                     FListItemSupportingText, 
                                     FListItemTertiaryText)):
            return
        elif not has_unique_widgets(self.children+[widget]):
            return
        elif not is_widgets_ordered(self.possible_widgets, self.children + [widget]):
            ordered_widgets = sorted(self.children+[widget], 
                                     key=lambda x: 
                                     self.possible_widgets.index(
                                         type(x).__name__))
            self.clear_widgets()
            for _widget in ordered_widgets:
                super().add_widget(_widget, *args, **kwargs)
            return
        return super().add_widget(widget, *args, **kwargs)


class FListTrailingContainer(BoxLayout):
    def add_widget(self, widget, *args, **kwargs):
        if len(self.children) == 1:
            raise FListException("FListItem can't contain more than 1 trail widget")
        elif not isinstance(widget, (FListItemTrailingText, 
                                     FListItemTrailingIcon, 
                                     FListItemTrailingCheckBox)):
            return
        return super().add_widget(widget, *args, **kwargs)


class ListBaseText(FLabel):
    pass

class FListItemLeadingText(CircularRippleBehavior, ButtonBehavior, FLabel):
    def on_text(self, instance_self, text=None):
        if len(self.text) > 2:
            raise FListException("FListItemHeadlineText can't contain more than 2 characters")
        return super().on_text(instance_self, text)

class FListItemTrailingText(FLabel):
    pass

class FListItemHeadlineText(ListBaseText):
    pass

class FListItemSupportingText(ListBaseText):
    pass 

class FListItemTertiaryText(ListBaseText):
    pass

class FListItemLeadingIcon(FIconButton):
    pass

class FListItemTrailingIcon(FIconButton):
    pass

class FListItemTrailingCheckBox(FCheckBox):
    pass

class FListItemLeadingThumbnail(Image):
    # FKivyMD.uix.list.FListItem object
    _list_item = ObjectProperty()

    def on_kv_post(self, base_widget):
        if self._list_item:
            height = self._list_item.height - (self._list_item.padding[1]*2)
            width = self.texture.width * (height / self.texture.height)
            self.size_hint = None, None
            self.size = width, height
        return super().on_kv_post(base_widget)
    
class FListItemLeadingAvatar(
    ThemableBehavior, 
    CircularRippleBehavior, 
    ButtonBehavior, 
    FitImage
):
    # FKivyMD.uix.list.FList object
    _list_item = ObjectProperty()