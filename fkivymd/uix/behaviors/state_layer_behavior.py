from kivy import platform
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ColorProperty, NumericProperty, BooleanProperty
from kivymd.uix.behaviors.focus_behavior import FocusBehavior

Builder.load_string(
    """
<FStateLayerBehavior>
    canvas.after:
        Color
            rgba: self.state_layer_color
        RoundedRectangle:
            group: "State_layer_instruction"
            size: self.size if self.state_effect else [0, 0]
            pos: self.pos
            radius: self.radius if hasattr(self, "radius") else [0, ]
""",
    filename="FStateLayerBehavior.kv",
)

class FStateLayerBehavior(FocusBehavior):
    _state_widget = None
    state_layer_color = ColorProperty([0, 0, 0, 0])
    state_hover = NumericProperty(0.07)
    state_press = NumericProperty(0.11)
    state_drag = NumericProperty(0.16)
    state_effect = BooleanProperty(True)
    _state = 0.0
    _bg_color = (0, 0, 0, 0)
    _is_already_disabled = False
    _shadow_softness = [0, 0]
    _elevation_level = 0
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._state_widget = self.get_root_widget()
        self.add_attr(self._state_widget)
        if hasattr(self, "style"):
            self.bind(style=lambda *x: self.add_attr(self._state_widget))

    def get_root_widget(self):
        _widgets = [
            ('FBaseButton', 'button.button'), 
            ('FIconButton', 'button'), 
            ('FSpeedDialButton', 'button'),
            ('FCard', 'card'),
            ('FFrame', 'card'),
            ('FLabel', 'label'), 
            ('FIcon', 'label'),
            ('FListItem', 'list'), 
            ('FCheckBox', 'selectioncontrol'),
            ]
        widgets = (i for i in _widgets)
        del _widgets
        
        def check(widget):
            exec(f"from fkivymd.uix.{widget[1]} import {widget[0]}")
            widget_ = eval(f"{widget[0]}")
            if isinstance(self, widget_):
                return widget[0]
            
            try:
                return check(next(widgets))
            except StopIteration:
                pass
        
        return check(next(widgets))
    
    def add_attr(self, widget):
        if not widget:
            return

        if widget in ["FBaseButton", "FIconButton", "FSpeedDialButton"]:
            self.disabled_bg_opacity = 0.4
            self.disabled_line_opacity = 0.4
            self.disabled_fg_opacity = 0.4

        elif widget in ["FFrame", "FCard"]:
            self.disabled_bg_opacity = 0.12 if self.style == "outlined" else 0.38

        elif self._state_widget in ["FLabel", "FIcon"]:
            self.disabled_fg_opacity = 0.38

        elif widget == "FListItem":
            self.disabled_bg_opacity = 0.38
            self.disabled_leading_avatar_opacity = 0.38

        elif widget == "FCheckBox":
            self.disabled_bg_opacity = 0.38

    def set_properties_widget(self) -> None:
        """Fired `on_release/on_press/on_enter/on_leave` events."""

        if not self.state_effect:
            return

        if not self.disabled:
            self._restore_properties()
            self._set_state_layer_color()

    def on_disabled(self, instance, value) -> None:
        return
        if not self.state_effect:
            return
        
        if value and not self._is_already_disabled:
            self._is_already_disabled = True
            if self._state_widget == "FBaseButton":
                self.state_layer_color = (
                    (self.theme_cls.onSurfaceColor[:-1] + [self.disabled_bg_opacity]
                    if self.style not in ["text", "outlined"] else self.theme_cls.transparentColor)
                    if not self.md_bg_color_disabled
                    else self.md_bg_color_disabled
                )
            elif self._state_widget == "FIconButton":
                self.state_layer_color = (
                    (self.theme_cls.onSurfaceColor[:-1] + [self.disabled_bg_opacity]
                    if self.style not in ["standard", "outlined"] else self.theme_cls.transparentColor)
                    if not self.md_bg_color_disabled
                    else self.md_bg_color_disabled
                )

            elif self._state_widget == "FCard":
                self.state_layer_color = (
                    {
                        "filled": self.theme_cls.surfaceColor[:-1] + [self.disabled_bg_opacity],
                        "outlined": self.theme_cls.outlineColor[:-1] + [self.disabled_bg_opacity],
                        "elevated": self.theme_cls.surfaceVariantColor[:-1] + [self.disabled_bg_opacity]
                    }[self.style]
                    if not self.md_bg_color_disabled
                    else self.md_bg_color_disabled
                )

            elif self._state_widget == "FListItem":
                self.state_layer_color = (
                    (self.theme_cls.onSurfaceColor[:-1] + [self.disabled_bg_opacity])
                    if not self.md_bg_color_disabled
                    else self.md_bg_color_disabled
                )

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
            if self._state_widget in ["FCard", "FListItem"]:
                target_color = self.theme_cls.onSurfaceColor
            elif self._state_widget == "FBaseButton":
                target_color = (
                    self.theme_cls.onPrimaryColor
                    if self.style == "filled"
                    else self.theme_cls.primaryColor
                    )
                
            elif self._state_widget == "FIconButton":
                if self.style == "filled":
                    target_color = self.theme_cls.onPrimaryColor
                elif self.style == "tonal":
                    target_color = self.theme_cls.onSecondaryContainerColor
                elif self.style in ["outlined", "standard"]:
                    target_color = self.theme_cls.primaryColor
            
            elif self._state_widget == "FSpeedDialButton":
                target_color = self.theme_cls.onPrimaryColor

            elif self._state_widget == "FCheckBox":
                target_color = (
                    self.theme_cls.primaryColor
                    if self.active
                    else self.theme_cls.onSurfaceColor
                )
            else:
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
                    self.state_layer_color = target_color[:-1] + [self._state]
                else:
                    self.state_layer_color = self.focus_color
            elif self._state == self.state_press:
                self.state_layer_color = target_color[:-1] + [self._state]
            elif not self._state:
                self.state_layer_color = target_color[:-1] + [self._state]
