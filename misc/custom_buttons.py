from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty
from kivy.core.window import Window
from kivy.clock import Clock


class HoverButton(Button):
    standard_color = ListProperty([1,1,1])
    hover_color = ListProperty([0.6,0.7,1])

    def __init__(self, **kwargs):
        super(HoverButton, self).__init__(**kwargs)
        Window.bind(mouse_pos = self.on_mouse_pos)

    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return

        if self.collide_point(*pos):
            Clock.schedule_once(self._mouse_enter,0)
        else:
            Clock.schedule_once(self._mouse_leave,0)
    
    def _mouse_enter(self,k):
        self.color = self.hover_color
    
    def _mouse_leave(self,k):
        self.color = self.standard_color


class ChannelGrid(BoxLayout):
    channel_buttons = [ToggleButton(text=str(i)) for i in range(16)]
    callback = lambda *args : None
    
    def __init__(self, **kwargs):
        super(ChannelGrid, self).__init__(**kwargs)
        
        for idx, button in enumerate(self.channel_buttons):
            setattr(button, "channel_id", idx)
            button.bind(on_press=self.callback)
        
        self.top_row = BoxLayout(orientation="horizontal")
        self.bottom_row = BoxLayout(orientation="horizontal")
        for button in self.channel_buttons[:8]:
            self.top_row.add_widget(button)
        for button in self.channel_buttons[8:]:
            self.bottom_row.add_widget(button)

        self.add_widget(self.top_row)
        self.add_widget(self.bottom_row)
