from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty
from kivy.clock import Clock

from copy import deepcopy

import c_utils
config = c_utils.load_config()

from settings_tabs.settings_tab import SettingsTab

class StyleSettings(SettingsTab):
    note_style_preview = ObjectProperty(None)
    velocity_scaling_slider = ObjectProperty(None)

    project_properties = c_utils.load_json(f"{config['project']['projects_location']}{config['project']['default']}")
    channel_styles = None
    active_channel = NumericProperty(0)
    
    pianoroll = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.channel_styles = {i : deepcopy(self.project_properties['style'])
                               for i in range(16)} # currently a bit wasteful since all 16 MIDI channels will practically never be used

        self.preview_references_event = Clock.schedule_interval(lambda dt:
                                                                self.__pass_references_to_preview(),
                                                                1/config['main']['init_update_freq'])

    def __pass_references_to_preview(self):
        if self.note_style_preview != None:
            self.note_style_preview.channel_styles = self.channel_styles
            self.preview_references_event.cancel()

    def __update_preview(self):
        self.note_style_preview.stage_preview.pianoroll.clear_widgets()
        
        self.note_style_preview.stage_preview.pianoroll.init_schedule("UI/menu/note_style_preview_MIDI.mid",
                                                                      {0: self.channel_styles[self.active_channel]})
        self.note_style_preview.stage_preview.pianoroll.scroll_schedule(1/2)

    def change_channel(self,difference):
        self.active_channel += difference
        self.active_channel = self.active_channel % 16

        self.__update_preview()
        self.velocity_scaling_slider.slider.value = self.channel_styles[self.active_channel]['notes']['velocity_scaling']

    def load_color_wheel(self,callback):
        self.show_color_chooser(callback)

    def change_channel_attribute(self,attribute_name,value):
        pass

    def change_white_key_color(self,color):
        self.channel_styles[self.active_channel]['notes']['white_key_color'] = color[:-1] # alpha is the last entry and is excluded for note color
        
        self.__update_preview()

    def change_velocity_scaling(self):
        self.channel_styles[self.active_channel]['notes']['velocity_scaling'] = self.velocity_scaling_slider.slider.value
        self.__update_preview()