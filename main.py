from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty
from kivy.core.window import Window
from kivy.clock import Clock
#from kivy.lang import Builder

import c_utils
from midi_handling import schedules

#Global scope
config = c_utils.load_config()
#Builder.load_file(config['main']['kv_location'])

class WhiteKey(Widget):
    note = StringProperty(None)

class BlackKey(Widget):
    note = StringProperty(None)

class Keybed(Widget):
    note_lookup = c_utils.load_json(config['theory']['note_lookup_location'])
    keys = []

    def draw_keybed(self,k,key_range=["A0","C7"]):
        """
        Ignoring key_range for now.
        Could be nice to be able to specify which keys are shown
        For 88 keys
        52 white keys
        36 black keys
        """
        
        next_wk_pos = 0
        next_bk_pos = 0
        for i in range(88):
            note = self.note_lookup['12-tone_scale'][i % 12]
            if len(note) == 1:
                
                key = WhiteKey()
                key.note = note
                key.width = self.width/60
                key.height = self.height

                key.center_x = self.width*next_wk_pos + key.width/2
                
                next_wk_pos += 1/52
                next_bk_pos = next_wk_pos

                self.keys.append(key)
                #self.add_widget(key)
        
            else:
                key = BlackKey()
                key.note = note
                key.width = self.width/80
                key.height = self.height*0.75

                key.center_x = self.width*next_bk_pos
                key.y = self.height - key.height
                
                next_bk_pos = next_wk_pos + 1/(52*2)

                self.keys.append(key)
                #self.add_widget(key)
        
        for i in range(88):
            note = self.note_lookup['12-tone_scale'][i % 12]
            if len(note) == 1:
                self.add_widget(self.keys[i])
        
        for i in range(88):
            note = self.note_lookup['12-tone_scale'][i % 12]
            if len(note) == 2:
                self.add_widget(self.keys[i])

    def resize_children(self):
        """
        Resizes keys on window resize.
        TODO: work on removing redundant code similar to draw_keybed function
        """

        next_wk_pos = 0
        next_bk_pos = 0

        for key in self.keys:
            if len(key.note) == 1:
                key.width = self.width/60
                key.height = self.height

                key.center_x = self.width*next_wk_pos + key.width/2
                
                next_wk_pos += 1/52+0.01
                next_bk_pos = next_wk_pos
            else:
                key.width = self.width/80
                key.height = self.height*0.75

                key.center_x = self.width*next_bk_pos
                key.y = self.height - key.height
                
                next_bk_pos = next_wk_pos + 1/(52*2)

class PianoNote(Widget):
    note = StringProperty(None)

class PianoRoll(Widget):
    NS = None
    pianonote = None

    def init_schedule(self,k):
        self.NS = schedules.NoteSchedule('midi_data/test_midi.mid')
        
        for channel in self.NS.channels.values():
            channel.sort()
            
            for note in channel:
                
                corresponding_key = self.parent.keybed.keys[note.note-9]

                pianonote = PianoNote()
                
                norm_time = note.norm_time(self.NS.schedule_meta_data.ticks_per_beat)
                
                pianonote.width = corresponding_key.width 
                pianonote.height = ( norm_time[1] - norm_time[0] ) # Norm time might be unnecessary since ticks per beat is also used in update which should compensate for any differences
                
                pianonote.y = self.height + norm_time[0]
                pianonote.x = corresponding_key.x #self.width * ((note.note-9) / 88)
                self.add_widget(pianonote)

    def resize_children(self):
        pass

    def update(self,dt):
        TPS = self.NS.schedule_meta_data.ticks_per_beat * self.NS.get_BPM() / 60 # With norm_time 96 should be used as ticks per beat
        
        for child in self.children:
            child.y -= TPS*dt # Use this to adjust speed and then use fixed note size

class Stage(Widget):
    keybed = ObjectProperty(None)
    pianoroll = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.maximize()
        Window.bind(on_resize=self.on_window_resize)

    def on_window_resize(self, window, width, height):
        Clock.schedule_once(self.resize_children,0)

    def resize_children(self,k):
        for child in self.children:
            try:
                child.resize_children()
            except AttributeError:
                pass

    def update(self,dt):
        self.pianoroll.update(dt)

class Workbench(Widget): #Could be root widget with stage as one primary child and some other widget for tuning parameters and loading midi file
    pass

class KeysVizuApp(App):

    def build(self):
        self.load_kv(config['main']['kv_location'])
        
        stage = Stage()
        
        Clock.schedule_once(stage.keybed.draw_keybed)
        Clock.schedule_once(stage.pianoroll.init_schedule)

        Clock.schedule_interval(stage.update, 1.0/60.0)
        
        return stage

def main():
    KeysVizu = KeysVizuApp()
    KeysVizu.run()

if __name__ == '__main__':
    main()