from kivy.uix.button import Button
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