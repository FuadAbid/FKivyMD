"""
Dialog creation using kv file:
------------------------------

    from kivy.lang import Builder
    from kivymd.app import MDApp
    import FKivyMD
    from FKivyMD.uix.dialog import FDialog
    

    KV = '''
    #: import Factory kivy.factory.Factory

    <MyDialog@FDialog>
        FDialogIcon:
            icon: 'refresh'
        FDialogHeadlineText:
            text: 'Reset settings?'
        FDialogSupportingText:
            text: 
                "This will reset your app preferences back to their " \
                "default settings. The following accounts will also " \
                "be signed out:"
        FDialogContentContainer:
            orientation: 'vertical'
            FDivider:
            FListItem:
                theme_bg_color: "Custom"
                md_bg_color: self.theme_cls.transparentColor
                FListItemLeadingIcon:
                    icon: 'gmail'
                FListItemSupportingText:
                    text: 'KivyMD-library@yandex.com'
            FListItem:
                theme_bg_color: "Custom"
                md_bg_color: self.theme_cls.transparentColor
                FListItemLeadingIcon:
                    icon: 'gmail'
                FListItemSupportingText:
                    text: 'kivydevelopment@gmail.com'
            FDivider:
        FDialogButtonContainer:
            spacing: '8dp'
            FButton:
                style: 'text'
                state_effect: True
                ripple_effect: True
                FButtonText:
                    text: 'Cancel'
            FButton:
                style: 'filled'
                state_effect: True
                ripple_effect: True
                FButtonText:
                    text: 'Accept'
            
    MDScreen:
        md_bg_color: self.theme_cls.backgroundColor

        FButton:
            pos_hint: {'center_x': .5, 'center_y': .5}
            on_release: Factory.MyDialog().open()

            FButtonText:
                text: "Show dialog"
    '''


    class Example(MDApp):
        def build(self):
            return Builder.load_string(KV)


    Example().run()


Dialog creation using py file:
------------------------------

    from kivy.lang import Builder

    from kivymd.app import MDApp
    from FKivyMD.uix.button import FButton, FButtonText
    from FKivyMD.uix.dialog import (
        FDialog,
        FDialogIcon,
        FDialogHeadlineText,
        FDialogSupportingText,
        FDialogButtonContainer,
        FDialogContentContainer,
    )
    from FKivyMD.uix.divider import FDivider
    from FKivyMD.uix.list import (
        FListItem,
        FListItemLeadingIcon,
        FListItemSupportingText,
    )

    KV = '''       
    MDScreen:
        md_bg_color: self.theme_cls.backgroundColor

        FButton:
            pos_hint: {'center_x': .5, 'center_y': .5}
            on_release: app.show_alert_dialog()

            FButtonText:
                text: "Show dialog"
    '''


    class Example(MDApp):
        def build(self):
            return Builder.load_string(KV)

        def show_alert_dialog(self):
            FDialog(
                # ----------------------------Icon-----------------------------
                FDialogIcon(
                    icon="refresh",
                ),
                # -----------------------Headline text-------------------------
                FDialogHeadlineText(
                    text="Reset settings?",
                ),
                # -----------------------Supporting text-----------------------
                FDialogSupportingText(
                    text="This will reset your app preferences back to their "
                    "default settings. The following accounts will also "
                    "be signed out:",
                ),
                # -----------------------Custom content------------------------
                FDialogContentContainer(
                    FDivider(),
                    FListItem(
                        FListItemLeadingIcon(
                            icon="gmail",
                        ),
                        FListItemSupportingText(
                            text="KivyMD-library@yandex.com",
                        ),
                        theme_bg_color="Custom",
                        md_bg_color=self.theme_cls.transparentColor,
                    ),
                    FListItem(
                        FListItemLeadingIcon(
                            icon="gmail",
                        ),
                        FListItemSupportingText(
                            text="kivydevelopment@gmail.com",
                        ),
                        theme_bg_color="Custom",
                        md_bg_color=self.theme_cls.transparentColor,
                    ),
                    FDivider(),
                    orientation="vertical",
                ),
                # ---------------------Button container------------------------
                FDialogButtonContainer(
                    FButton(
                        FButtonText(text="Cancel"),
                        style="text",
                    ),
                    FButton(
                        FButtonText(text="Accept"),
                        style="filled",
                    ),
                    spacing="8dp",
                ),
                # -------------------------------------------------------------
            ).open()


    Example().run()
"""

__all__ = [
    'FDialog', 
    'FDialogHeadlineText', 
    'FDialogIcon', 
    'FDialogSupportingText', 
    'FDialogContentContainer', 
    'FDialogButtonContainer'
]


import os

from kivy.core.window import Window
from kivy.properties import (
    ColorProperty, 
    ObjectProperty, 
    OptionProperty, 
    NumericProperty, 
    BooleanProperty, 
    VariableListProperty
)
from kivy.metrics import dp
from kivy.lang.builder import Builder
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import  RelativeLayout
from kivymd.uix.behaviors import (
    DeclarativeBehavior, 
    ScaleBehavior
)
from fkivymd.uix.card import FFrame
from fkivymd.uix.label import FLabel, FIcon
from fkivymd import uix_path

with open(
    os.path.join(uix_path, "dialog", "dialog.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class FDialogHeadlineText(FLabel):
    pass

class FDialogIcon(FIcon):
    pass

class FDialogSupportingText(FLabel):
    pass

class FDialogContentContainer(DeclarativeBehavior, BoxLayout):
    pass

class FDialogContentContainer(DeclarativeBehavior, BoxLayout):
    pass

class FDialogButtonContainer(DeclarativeBehavior, BoxLayout):
    pass

class FDialogScrim(RelativeLayout):
    color = ColorProperty([0,0,0,0])


class FDialog(ScaleBehavior, FFrame):
    """
    :Events:
        `on_pre_open`:
            Fired before the MDDialog is opened. When this event is fired
            MDDialog is not yet added to window.
        `on_open`:
            Fired when the MDDialog is opened.
        `on_pre_dismiss`:
            Fired before the MDDialog is closed.
        `on_dismiss`:
            Fired when the MDDialog is closed. If the callback returns True,
            the dismiss will be canceled.
    """
    auto_dismiss = BooleanProperty(True)
    scrim_color = ColorProperty([0, 0, 0, .4])
    button_anchor = OptionProperty("right", options=['left', 'center', 'right'])
    minimum_width = NumericProperty(dp(280))
    padding = VariableListProperty([dp(24),])
    spacing = NumericProperty(dp(16))

    _anim_duration = NumericProperty(0.3)
    _is_open = BooleanProperty(False)
    _touch_started_inside = None
    # FKivyMD.uix.dialog.dialog.FDialogScrim object
    _scrim = ObjectProperty()
    _widgets_sorted = BooleanProperty(False)
    _widget_classes = [FDialogIcon, FDialogHeadlineText, FDialogSupportingText, 
                    FDialogContentContainer, FDialogButtonContainer]

    __events__ = ('on_pre_open', 'on_open', 'on_pre_dismiss', 'on_dismiss')

    def __init__(self, *args, **kwargs):
        self._parent = None
        super().__init__(*args, **kwargs)
        #self.opacity = 0

    def open(self, *_args, **kwargs):
        """Display the modal in the Window.

        When the view is opened, it will be faded in with an animation. If you
        don't want the animation, use::

            view.open(animation=False)

        """
        if self._is_open:
            return
        
        self._is_open = True
        self.dispatch('on_pre_open')
        if not self._scrim:
            self._scrim = FDialogScrim(color=self.scrim_color, 
                                       size=Window.size, 
                                       opacity=0)
            self._scrim.add_widget(self)
        Window.add_widget(self._scrim)
        Window.bind(on_keyboard=self._handle_keyboard)

        if kwargs.get('animation', True):
            anim = Animation(opacity=1, d=self._anim_duration)
            anim.bind(on_complete=lambda *_args: self.dispatch('on_open'))
            anim.start(self._scrim)
        else:
            self._scrim.opacity = 1
            self.dispatch('on_open')

    def dismiss(self, *_args, **kwargs):
        """ Close the view if it is open.

        When the view is dismissed, it will be faded out before being
        removed from the parent. If you don't want this animation, use::

            view.dismiss(animation=False)

        """
        if not self._is_open:
            return
        self.dispatch('on_pre_dismiss')
        if self._scrim:
            if kwargs.get('animation', True):
                anim = Animation(opacity=0, d=self._anim_duration)
                anim.bind(on_complete=lambda *_args: self._real_remove_widget())
                anim.start(self._scrim)
            else:
                self._scrim.opacity = 0

    def on_touch_down(self, touch):
        """ touch down event handler. """
        self._touch_started_inside = self.collide_point(*touch.pos)
        if not self.auto_dismiss or self._touch_started_inside:
            super().on_touch_down(touch)
        return True

    def on_touch_move(self, touch):
        """ touch moved event handler. """
        if not self.auto_dismiss or self._touch_started_inside:
            super().on_touch_move(touch)
        return True

    def on_touch_up(self, touch):
        """ touch up event handler. """
        # Explicitly test for False as None occurs when shown by on_touch_down
        if self.auto_dismiss and self._touch_started_inside is False:
            self.dismiss()
        else:
            super().on_touch_up(touch)
        self._touch_started_inside = None
        return True

    def _real_remove_widget(self):
        if not self._is_open:
            return
        if self._scrim:
            self._scrim.remove_widget(self)
            Window.remove_widget(self._scrim)
        Window.unbind(
            on_keyboard=self._handle_keyboard)
        self._is_open = False

    def on_center(self, instance, center):
        self.scale_value_center = self.width/2, self.height/2

    def on_width(self, _, width):
        if width <= self.minimum_width:
            self.scale_value_x = self.scale_value_y = width/self.minimum_width

    def on_pre_open(self):
        """ default pre-open event handler. """
    
    def on_open(self):
        """ default open event handler. """

    def on_pre_dismiss(self):
        """ default pre-dismiss event handler. """

    def on_dismiss(self):
        """ default dismiss event handler. """

    def _handle_keyboard(self, _window, key, *_args):
        if key == 27 and self.auto_dismiss:
            self.dismiss()
            return True
        
    def add_widget(self, widget, *args, **kwargs):
        if widget.__class__ in self._widget_classes:
            return self.ids.container.add_widget(widget, *args, **kwargs)
        return super().add_widget(widget, *args, **kwargs)
    
    def on_kv_post(self, *args, **kwargs):
        self.sort_children()
        super().on_kv_post(*args, **kwargs)

    def sort_children(self):
        index = 0
        _children_classes = list(map(lambda x: x.__class__, self.ids.container.children))
        _widget_classes = [i for i in self._widget_classes if i in _children_classes]
        while index < len(self.ids.container.children):
            index2 = _widget_classes.index(_children_classes[index])
            self.ids.container.children[index], self.ids.container.children[index2] = (
                self.ids.container.children[index2], self.ids.container.children[index])
            index += 1

        self._widgets_sorted = True