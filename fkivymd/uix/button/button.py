"""
Changes between MDButton and FButton
------------------------------------

<To use button widgets in kv file, `import FKivyMD` in your program>

- Blurry text bug fixed
Sometime button text look blurry in MDButton,
but FButton solves this problem


- Vertical positioned sub widgets: (by orientation)
    FButton:
        orientation: 'vertical'
        FButtonIcon:
            icon: 'navigation'
        FButtonText:
            text: 'Navigate'


- Order of the sub widgets matter:
ex.
(MDButton)
    MDButton:
        MDButtonText:
            text: 'Navigate'
        MDButtonIcon:
            icon: 'navigation'

    MDButton:
        MDButtonIcon:
            icon: 'navigation'
        MDButtonText:
            text: 'Navigate'   # same result as before

(FButton)
    FButton:
        FButtonText:
            text: 'Navigate'
        FButtonIcon:
            icon: 'navigation'  # icon to the right / bottom(orientation=vertical)

    FButton:
        FButtonIcon:
            icon: 'navigation'
        FButtonText:
            text: 'Navigate'   # text to the right / bottom(orientation=vertical)


- Custom size problem solved
If user wants to set custom width for button, for MDButton it
sticks to left position and user needs to mess with positions 
of the sub widgets to position those in center and that may not 
even work when window is resized. But with FButton user can set 
any custom width and sub widgets will be positioned in center 
automatically.
ex.
(MDButton)
    MDButton:
        theme_width: "Custom"
        size_hint_x: .5
        MDButtonIcon:
            x: text.x - (self.width + dp(10)) # to fix position
            icon: "plus"
        MDButtonText:
            id: text
            text: "Add Item"
            pos_hint: {"center_x": .5, "center_y": .5} # to fix position

(FButton)
    FButton:
        theme_width: 'Custom'
        size_hint_x: .5
        FButtonIcon:
            icon: 'plus'
        FButtonText:
            text: 'Add Item'


- Change side paddings and space between text and icon:
    FButton:
        horizontal_pad: '30dp'
        vertical_pad: '25dp'
        spacing: '10dp'
        FButtonIcon:
            icon: 'plus'
        FButtonText:
            text: 'Add Item'

            
- Change in modifying radius:
(MDButton)
    MDButton:
        radius: 0

(FButton)
    FButton:
        theme_radius: 'Custom'
        radius: 0


- Ripple color matching with button color:
Unlike for MDButton having a constant grey ripple color,
FButton ripple color matches with theme and button color


- Can be used as FIconButton:
(though it's recommended to use FIconButton)
    FButton:
        FButtonIcon:
            icon: 'heart-outline'
"""

from __future__ import annotations

__all__ = (
    'FBaseButton',
    'FButton',
    'FButtonText',
    'FButtonIcon',
    'FButton2'
    'FIconButton',
    'StateLayerBehavior'
)

import os

from kivy import platform
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    ColorProperty,
    NumericProperty,
    DictProperty,
    OptionProperty,
    ObjectProperty, 
    StringProperty, 
    BooleanProperty,
    VariableListProperty, 
)
from kivy.animation import Animation
from fkivymd.uix.behaviors.extended_background import ExtendedBackgroundBehavior
from fkivymd.uix.behaviors import FBackgroundColorBehavior
from fkivymd.uix.behaviors import FCommonElevationBehavior
from fkivymd.uix.label import FLabel, FIcon
from FKivyMD import uix_path
from kivymd import fonts_path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.behaviors import (
    DeclarativeBehavior, 
    RectangularRippleBehavior, 
    HoverBehavior
)
from kivymd.theming import ThemableBehavior
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.icon_definitions import md_icons
from fkivymd.uix.behaviors import FStateLayerBehavior

with open(os.path.join(uix_path, "button", "button.kv"), encoding="utf-8") as kvfile:
    Builder.load_string(kvfile.read())


class FButtonText(FLabel):
    # kivymd.uix.button.button.MDButton object.
    _button = ObjectProperty()


class FButtonIcon(FIcon):
    # FKivyMD.uix.button.button.FButton object.
    _button = ObjectProperty()

class FBaseButton(
    RectangularRippleBehavior, 
    ThemableBehavior,
    FCommonElevationBehavior, 
    FBackgroundColorBehavior, 
    FStateLayerBehavior
):
    elevation_levels = DictProperty(
        {
            0: 0,
            1: dp(4),
            2: dp(8),
            3: dp(12),
            4: dp(16),
            5: dp(18),
        }
    )
    style = OptionProperty(
        "elevated", options=("elevated", "filled", "tonal", "outlined", "text")
    )
    horizontal_pad = dp(20)
    vertical_pad = dp(10.5)
    md_bg_color_disabled = ColorProperty(None)
    radius = VariableListProperty([dp(20),], length=4)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shadow_update()

    def shadow_update(self, *args):
        if self.disabled:
            self.shadow_color = self.theme_cls.transparentColor
        else:
            self.shadow_color = ((self.theme_cls.shadowColor[:-1] + [.5]
                                 if self.theme_shadow_color == "Primary"
                                 else self.shadow_color) if self.style 
                                 not in ["outlined", "text"] else 
                                 self.theme_cls.transparentColor)

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

        if (
            self._state == self.state_hover
            and self.focus_behavior
            or self._state == self.state_press
        ):
            self._elevation_level = (
                1
                if self.theme_elevation_level == "Primary"
                else self.elevation_level
            )
            self._shadow_softness = (
                0
                if self.theme_shadow_softness == "Primary"
                else self.shadow_softness
            )

            if self.style == "elevated":
                if not self.disabled:
                    if self._state == self.state_hover and self.focus_behavior:
                        self.elevation_level = 2
                        self.shadow_softness = 2
                    elif self._state == self.state_press:
                        self.elevation_level = 2
                        self.shadow_softness = 2
                    elif not self._state:
                        self.elevation_level = 1
                        self.shadow_softness = 0


class FButton2(FBaseButton, ButtonBehavior, FLabel):
    theme_width = OptionProperty("Primary", options=("Primary", "Custom"))
    theme_height = OptionProperty("Primary", options=("Primary", "Custom"))
    icon = StringProperty("blank")
    icon_size = NumericProperty(dp(20))
    icon_pos_offset = NumericProperty(0)

    def on_icon(self, instance, icon):
        self.text = f"[font={fonts_path}/MaterialDesignIcons.ttf][size={int(self.icon_size)}]{md_icons[icon]}[/size][/font]  {self.text}"


class FButton(DeclarativeBehavior, FBaseButton, ButtonBehavior, BoxLayout):
    theme_width = OptionProperty("Primary", options=("Primary", "Custom"))
    theme_height = OptionProperty("Primary", options=("Primary", "Custom"))
    theme_radius = OptionProperty("Primary", options=['Primary', 'Custom'])
    # FKivyMD.uix.button.button.FButtonIcon object.
    _button_icon = ObjectProperty(None)
    # FKivyMD.uix.button.button.FButtonText object.
    _button_text = ObjectProperty(None)
    _last_size = None
    _nChild = 0
    button_widgets = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.set_size, 0.2)
        Clock.schedule_once(self.set_pos, 0.2)
        Window.bind(size=Clock.schedule_once(self.set_size))
        Window.bind(on_maximize=Clock.schedule_once(self.set_size))
        Window.bind(on_restore=Clock.schedule_once(self.set_size))

    def on_disabled(self, instance_button, is_disabled):
        if is_disabled:
            for child in self.children:
                child.disabled = True
        self.shadow_update()
        super().on_disabled(instance_button, is_disabled)

    def on_size_hint(self, *args):
        check_hints = []
        if self.theme_width == "Primary":
            check_hints.append(0)
        else:
            check_hints.append(1)

        if self.theme_height == "Primary":
            check_hints.append(0)
        else:
            check_hints.append(1)

        if any(check_hints):
            Clock.schedule_once(self.set_size)

    def on_orientation(self, *args):
        Clock.schedule_once(self.set_size)
        Clock.schedule_once(self.set_pos)

    def add_widget(self, widget, *args, **kwargs):
        if isinstance(widget, FButtonText):
            if self._button_text is not None:
                return
            self._button_text = widget
        elif isinstance(widget, FButtonIcon):
            if self._button_icon is not None:
                return
            self._button_icon = widget
        if isinstance(widget, (FButtonText, FButtonIcon)):
            widget._button = self
            widget.bind(text=lambda x, y:
            Clock.schedule_once(lambda z: self.set_size))
            self.button_widgets.append(widget)
            self._nChild += 1
        super().add_widget(widget, *args, **kwargs)

    def set_size(self, *args):
        def set_size(x):
            children_widths = []
            children_heights = []

            for child in self.button_widgets:
                child_tex_size = getattr(child, "texture_size")
                children_widths.append(child_tex_size[0])
                children_heights.append(child_tex_size[1])

            size_func = [sum, max]
            width_func = sum if self.orientation == "horizontal" else max
            size_func.remove(width_func)
            height_func = size_func[0]

            def get_primary_width():
                width = width_func(children_widths) + self.horizontal_pad * 2
                if self._nChild > 1:
                    width += self.spacing if self.orientation == "horizontal" else 0
                return width

            def get_primary_height():
                height = height_func(children_heights) + self.vertical_pad * 2
                if self._nChild > 1:
                    height += self.spacing if self.orientation == "vertical" else 0
                return height

            if self.theme_width == "Primary":
                self.size_hint_x = None
                if self._nChild == 1 and isinstance(self.button_widgets[-1], FButtonIcon):
                    self.width = children_widths[0] + self.vertical_pad * 2
                else:
                    self.width = get_primary_width()
            elif self.theme_width == "Custom":
                self.size_hint_min_x = get_primary_width()

            if self.theme_height == "Primary":
                self.size_hint_y = None
                if self._nChild == 1 and isinstance(self.button_widgets[-1], FButtonIcon):
                    self.height = children_heights[0] + self.vertical_pad * 2
                else:
                    self.height = get_primary_height()
            elif self.theme_height == "Custom":
                self.size_hint_min_y = get_primary_height()
            if self._nChild > 1:
                padding = (((self.width + self.padding[0] + self.padding[2] - sum(children_widths)) / 2)
                           if self.orientation == "horizontal" else
                           (self.height + self.padding[1] + self.padding[3] - sum(children_heights)) / 2)
                for widget, width, height in zip(self.button_widgets, children_widths, children_heights):
                    if self.orientation == "horizontal":
                        size_hint_x = (padding + width) / self.width
                        if isinstance(widget, FButtonIcon):
                            size_hint_x -= 0.03
                        widget.size_hint_x = size_hint_x
                        widget.size_hint_y = 1
                        widget.text_size = size_hint_x * self.width, None
                    elif self.orientation == "vertical":
                        size_hint_y = (padding + height) / self.height
                        widget.size_hint_y = size_hint_y
                        widget.size_hint_x = 1
                        widget.text_size = None, size_hint_y * self.height
            else:
                self.button_widgets[-1].size_hint = 1, 1

            self._last_size = self.size.copy()

        if self._nChild and (self.size != self._last_size or args[0] == "<texture>"):
            Clock.schedule_once(set_size)

    def set_pos(self, *args):
        def set_pos(*args):
            if self._nChild > 1:
                if self.orientation == "horizontal":
                    self.button_widgets[0].halign = "right"
                    self.button_widgets[1].halign = "left"
                elif self.orientation == "vertical":
                    self.button_widgets[1].valign = "top"
                    self.button_widgets[0].valign = "bottom"
        if self._nChild:
            Clock.schedule_once(set_pos)

class FIconButton(RectangularRippleBehavior, ButtonBehavior, FIcon):
    style = OptionProperty("standard", options=("standard", "filled", "tonal", "outlined"))
    md_bg_color_disabled = ColorProperty(None)


class FSpeedDialHintText(FLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opacity = 0

from kivy.uix.label import Label
class FSpeedDialButton(
    DeclarativeBehavior,
    ThemableBehavior,
    RectangularRippleBehavior,
    ExtendedBackgroundBehavior,
    FBackgroundColorBehavior,
    FCommonElevationBehavior, 
    ButtonBehavior,
    Label, 
    FStateLayerBehavior,
    HoverBehavior):
    # FKivyMD.uix.button.button.FSpeedDialActionHintText object
    _hint_text = ObjectProperty(None)
    # FKivyMD.uix.button.button.FSpeedDialButtons object
    _sub_master = None
    _master = None
    _padding_ = None

    role = OptionProperty("large", options=["large", "medium", "small"])
    icon = StringProperty("blank")
    source = StringProperty(None, allownone=True)
    icon_color = ColorProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opacity = 0

    def on__padding(self, instance, _padding):
        if not self._padding_:
            self._padding_ = _padding

    def add_widget(self, widget, index=0, canvas=None):
        if not isinstance(widget, FSpeedDialHintText):
            return
        if not self._hint_text:
            self._hint_text = widget

        super().add_widget(widget)

    def on_icon_color(self, instance_label, color: list | str) -> None:
        if self.theme_icon_color == "Custom":
            if self.theme_cls.theme_style_switch_animation:
                Animation(
                    color=color,
                    d=self.theme_cls.theme_style_switch_animation_duration,
                    t="linear",
                ).start(self)
            else:
                self.color = color

    def on_enter(self):
        if self._sub_master:
            self._sub_master.on_enter(self)

    def on_leave(self):
        if self._sub_master:
            self._sub_master.on_leave(self)

class FSpeedDialButtons(DeclarativeBehavior, ThemableBehavior, FloatLayout):
    button_text_offset = NumericProperty(dp(38))
    label_direction = OptionProperty("right", options=["left", "right"])
    stack_button_direction = OptionProperty("top", options=["top", "bottom"])
    state = OptionProperty("close", options=("close", "open"))
    auto_dismiss = BooleanProperty(True)
    _padding = NumericProperty(0)
    
    # Colors
    hint_text_color = ColorProperty(None)
    button_bg_color = ColorProperty(None)
    button_icon_color = ColorProperty(None)
    hint_text_color_disabled = ColorProperty(None)
    button_bg_color_disabled = ColorProperty(None)
    button_icon_color_disabled = ColorProperty(None)

    # Animation
    hint_animation = BooleanProperty(False)
    opening_transition = StringProperty("out_cubic")
    closing_transition = StringProperty("out_cubic")
    opening_time = NumericProperty(0.5)
    closing_time = NumericProperty(0.2)

    # class variables
    _anim_buttons_data = {}
    _anim_labels_data = {}
    _direction_vals = {'right': 1, 'top': 1,
                       'left': -1, 'bottom': -1}
    _touch_started_inside = None
    _children = []
    _child_pos = {}
    _anim_x_widget = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = None, None
        self.size = 0, 0
        self.register_event_type("on_open")
        self.register_event_type("on_close")
        self.register_event_type("on_press_stack_button")
        self.register_event_type("on_release_stack_button")

    def on_enter(self, button):
        if self.state == "open":
            label = button._hint_text
            if isinstance(label, FSpeedDialHintText) and self.hint_animation:
                _padding = button._padding_ if button._padding_ else 0
                Animation.cancel_all(label)
                Animation(
                    _canvas_width=((label.width + self.button_text_offset + _padding) * 
                                   self._direction_vals[self.label_direction]),
                    _padding=_padding,
                    d=self.opening_time, 
                    t=self.opening_transition,
                ).start(button)
                Animation(opacity=1, d=self.opening_time*2, t=self.opening_transition).start(label)

    def on_leave(self, button):
        if self.state == "open":
            label = button._hint_text
            if isinstance(label, FSpeedDialHintText) and self.hint_animation:
                Animation.cancel_all(label)
                Animation(
                    _canvas_width=0,
                    _padding=0,
                    d=self.opening_time,
                    t=self.opening_transition,
                ).start(button)
                Animation(opacity=0, d=0.1, t=self.opening_transition).start(label)

    def add_widget(self, widget, *args, **kwargs):
        if not isinstance(widget, FSpeedDialButton):
            return
        
        widget.bind(
                on_press=lambda x: self.dispatch("on_press_stack_button"),
                on_release=lambda x: self.dispatch("on_release_stack_button"),
            )
        widget._sub_master = self
        widget._master = self.parent
        self._children.append(widget)

    def set_pos_label(self, label: FSpeedDialHintText) -> None:
        if not self.parent:
            return

        label.center = label.parent.center
        label.center_x += ((label.width/2 + self.button_text_offset)
                           * self._direction_vals[self.label_direction])

    def set_pos_button(self, button: FSpeedDialButton) -> None:
        if not self.parent:
            return
        if self.state == "open":
            button.center_x = button._master.center_x
            button.center_y = button._master.center_y + self._child_pos[button]
        else:
            button.center = button._master.center

        if button._hint_text:
            self.set_pos_label(button._hint_text)
        
    def open_stack(self, root_button):
        if self.state == "open":
            self.close_stack()
            return
        self.remove_widgets()
        self.add_widgets()
        self._update_pos_buttons()
        
        y = 10 * self._direction_vals[self.stack_button_direction]
        anim_buttons_data = {}
        anim_labels_data = {}

        for button in self._children:
            y += dp(56) * self._direction_vals[self.stack_button_direction]
            button.center_y += y
            self._child_pos[button] = y
            if not self._anim_buttons_data:
                anim_buttons_data[button] = Animation(
                    opacity=1,
                    d=self.opening_time,
                    t=self.opening_transition,
                )
            label = button._hint_text
            if isinstance(label, FSpeedDialHintText):
                label.center_y = button.center_y
                if not self._anim_labels_data:
                    anim_labels_data[label] = Animation(
                        opacity=1, d=self.opening_time
                    )

        if anim_buttons_data:
            self._anim_buttons_data = anim_buttons_data
        if anim_labels_data and not self.hint_animation:
            self._anim_labels_data = anim_labels_data

        self.state = "open"
        self.dispatch("on_open")
        self.do_animation_open_stack(self._anim_buttons_data)
        self.do_animation_open_stack(self._anim_labels_data)

    def close_stack(self):
        for i, button in enumerate(self._children):
            if isinstance(button, FSpeedDialButton):
                anim = Animation(
                    center_y=button._master.center_y,
                    d=self.closing_time,
                    t=self.closing_transition,
                    opacity=0)
                if i == len(self._children)-1:
                    anim.bind(on_complete=self.remove_widgets)
                self._anim_x_widget[anim] = button
                anim.start(button)
            label = button._hint_text
            if isinstance(label, FSpeedDialHintText):
                if label.opacity > 0:
                    Animation(opacity=0, d=0.01).start(label)

        self.state = "close"
        self.dispatch("on_close")
        self.remove_bindings()

    def on_state(self, *args):
        if self.state == "open" and len(self._anim_x_widget) > 0:
            for anim, widget in self._anim_x_widget.items():
                anim.stop(widget)
            else:
                self._anim_x_widget = {}

    def do_animation_open_stack(self, anim_data: dict) -> None:
        """
        anim_data = {
            FKivyMD.uix.button.FSpeedDialButton object :
            kivy.animation.Animation object
            }
        """
        def on_progress(animation, widget, value):
            if value >= 0.1:
                animation_open_stack()

        def animation_open_stack(*args):
            try:
                widget = next(widgets_list)
                animation = anim_data[widget]
                animation.bind(on_progress=on_progress)
                animation.start(widget)
            except StopIteration:
                self.add_bindings()
        

        widgets_list = iter(list(anim_data.keys()))
        animation_open_stack()

    def on_parent(self, instance_self, instance_parent):
        if instance_parent:
            if hasattr(instance_parent, "on_release") and hasattr(instance_parent, "on_press"):
                self.parent.bind(on_release=self.open_stack)
            else:
                raise ValueError("Parent Widget must be Clickable")

    def add_widgets(self):
        for child in self._children:
            Window.add_widget(child)

    def remove_widgets(self, *args):
        for child in self._children:
            try:
                Window.remove_widget(child)
            except ValueError:
                pass

    def add_bindings(self):
        Window.bind(on_resize=self._update_pos_buttons)
        Window.bind(on_maximize=self._update_pos_buttons)
        Window.bind(on_restore=self._update_pos_buttons)

        Window.bind(on_touch_down=self.touch_down)
        Window.bind(on_touch_move=self.touch_move)
        Window.bind(on_touch_up=self.touch_up)

    def remove_bindings(self):
        Window.unbind(on_resize=self._update_pos_buttons)
        Window.unbind(on_maximize=self._update_pos_buttons)
        Window.unbind(on_restore=self._update_pos_buttons)

        Window.unbind(on_touch_down=self.touch_down)
        Window.unbind(on_touch_move=self.touch_move)
        Window.unbind(on_touch_up=self.touch_up)

    def touch_down(self, instance_window, touch):
        """ touch down event handler. """
        texts = [button._hint_text for button in self._children if button._hint_text]
        self._touch_started_inside = any([widget.collide_point(*touch.pos)
                                          for widget in (self._children + texts)])
        if not self.auto_dismiss or self._touch_started_inside:
            Window.on_touch_down(touch)
        return True

    def touch_move(self, instance_window, touch):
        """ touch moved event handler. """
        if not self.auto_dismiss or self._touch_started_inside:
            Window.on_touch_move(touch)
        return True

    def touch_up(self, instance_window, touch):
        """ touch up event handler. """
        if self.auto_dismiss and self._touch_started_inside is False:
            self.close_stack()
        else:
            Window.on_touch_up(touch)
        self._touch_started_inside = None
        return True

    def _update_pos_buttons(self, *args):
        for child in self._children:
            self.set_pos_button(child)

    def on_open(self, *args):
        """Called when a stack is opened."""

    def on_close(self, *args):
        """Called when a stack is closed."""

    def on_press_stack_button(self, *args):
        """Called at the on_press event for the stack button"""

    def on_release_stack_button(self, *args):
        """Called at the on_release event for the stack button"""