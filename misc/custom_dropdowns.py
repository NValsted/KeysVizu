from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty
from kivy.clock import Clock

class StaticDropdown(Button):
    base_text = StringProperty("Select")
    options = ListProperty([None])

    def __init__(self, **kwargs):
        super(StaticDropdown, self).__init__(**kwargs)

        self.dropdown = DropDown()
        Clock.schedule_once(lambda dt: self.__create_dropdown_fields(self.options),1)

        self.bind(on_release = self.dropdown.open)

        self.dropdown.bind(on_select = lambda instance, x: setattr(self, 'text', x))

    def __create_dropdown_fields(self,options):
        for option in options:
            btn = Button(text = str(option), size_hint_y = None, height=30)
            btn.bind(on_release = lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)