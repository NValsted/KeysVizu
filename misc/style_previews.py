from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty
from kivy.clock import Clock

import c_utils
config = c_utils.load_config()

class NoteStylePreview(Widget):
    stage_preview = ObjectProperty(None)
    channel_styles = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.init_preview_event = Clock.schedule_interval(lambda dt:
                                                          self.__initialize_preview(),
                                                          1/config['main']['init_update_freq'])
        
    def __initialize_preview(self):
        if self.pos != [0,0] and self.channel_styles != None:
            self.init_preview_event.cancel()
            Clock.schedule_once(lambda dt: self.stage_preview.keybed.draw_keybed(key_range=["C2","B3"]))
            
            # There is currently redundant code between these and the __update_preview method in StyleSettings
            Clock.schedule_once(lambda dt: self.stage_preview.pianoroll.init_schedule("UI/menu/note_style_preview_MIDI.mid",
                                                                                      self.channel_styles))
            Clock.schedule_once(lambda dt: self.stage_preview.pianoroll.scroll_schedule(1/2))