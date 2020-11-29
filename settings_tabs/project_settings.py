from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty
from kivy.clock import Clock

from settings_tabs.settings_tab import SettingsTab

class ProjectSettings(SettingsTab):
    midi_load_button = ObjectProperty(None)
    midi_text_button = ObjectProperty(None)

    pianoroll = ObjectProperty(None)

    def load_schedule_location(self):
        self.show_file_chooser(filter_strings = ['*.mid'],
                               initial_directory = './midi_data',
                               callback = self.load_schedule)

    def load_schedule(self,filename):
        self.pianoroll.init_schedule(filename,
                                     self.menu.style_settings.channel_styles)
        
        self.midi_text_button.text = filename.split("/")[-1]