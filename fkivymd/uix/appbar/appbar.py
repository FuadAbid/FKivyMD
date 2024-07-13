# container (BoxLayout)
# title (always left)
# icon

from __future__ import annotations

__all__ = (
    'FTopAppBar',
    'FTopAppBarTitle',
    'FTopAppBarIcon'
)

import os
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.properties import (
    ColorProperty, 
    ObjectProperty)

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.behaviors import (
    DeclarativeBehavior, 
    CommonElevationBehavior, 
    BackgroundColorBehavior)

from kivymd.theming import ThemableBehavior
from kivymd.uix.controllers import WindowController
from fkivymd.uix.label import FLabel
from fkivymd.uix.button import FIconButton

from FKivyMD import uix_path

with open(
    os.path.join(uix_path, "appbar", "appbar.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class FTopAppBarIcon(FIconButton):
    # FKivyMD.uix.appbar.appbar.FTopAppBar object.
    _appbar = ObjectProperty()

    md_bg_color_disabled = ColorProperty([0,0,0,0])
    """
    The background color in (r, g, b, a) or string format of the button when
    the button is disabled.

    :attr:`md_bg_color_disabled` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """


class FTopAppBarTitle(FLabel):
    # FKivyMD.uix.appbar.appbar.FTopAppBar object.
    _appbar = ObjectProperty()


class FTopAppBar(
    DeclarativeBehavior,
    ThemableBehavior,
    BackgroundColorBehavior,
    BoxLayout,
):
    _appbar_title = ObjectProperty()

    def add_widget(self, widget, *args, **kwargs):
        if not isinstance(widget, (FTopAppBarIcon, FTopAppBarTitle)):
            return
        
        if isinstance(widget, FTopAppBarTitle):
            if not self._appbar_title:
                self._appbar_title = widget
            else:
                raise OverflowError("Window cannot have more than 1 title")
            
        widget._appbar = self

        return super().add_widget(widget, *args, **kwargs)