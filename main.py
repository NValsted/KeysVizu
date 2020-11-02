from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

import time
from collections import deque

import c_utils
from midi_tools import schedules
from video_tools import video_manager

#Global scope
config = c_utils.load_config()

global_flag = False

class PianoKey(Widget):
    note = StringProperty(None)

class BlackKey(PianoKey):
    standard_color = ListProperty([0.1,0.1,0.1])

class WhiteKey(PianoKey):
    standard_color = ListProperty([1,1,1])

class GuideLine(Widget):
    standard_color = ListProperty([0.15,0.15,0.15,0.5])
    points = ListProperty([None])

class Keybed(Widget):
    note_lookup = c_utils.load_json(config['theory']['note_lookup_location'])
    keys = []
    marker_notes = {"C"} #{"C","F"}

    def draw_keybed(self,k,key_range=["A0","C7"]):
        """
        Ignoring key_range for now.
        Could be nice to be able to specify which keys are shown
        For 88 keys
        52 white keys
        36 black keys
        """
        
        next_wk_pos = self.x
        next_bk_pos = self.x
        marker_keys = []

        for i in range(88):
            note = self.note_lookup['12-tone_scale'][i % 12]
            if len(note) == 1:
                
                key = WhiteKey()
                key.note = note
                key.width = self.width/60
                key.height = self.height

                key.center_x = self.width*next_wk_pos + key.width/2
                key.y = self.y
                
                next_wk_pos += 1/52
                next_bk_pos = next_wk_pos

                self.keys.append(key)
                self.add_widget(key,index=-1)

                if note in self.marker_notes:
                    marker_keys.append(key)
        
            else:
                key = BlackKey()
                key.note = note
                key.width = self.width/80
                key.height = self.height*0.75

                key.center_x = self.width*next_bk_pos
                key.y = self.height - key.height + self.y
                
                next_bk_pos = next_wk_pos + 1/(52*2)

                self.keys.append(key)
                self.add_widget(key)

        self.__add_vertical_guidelines(marker_keys)

        """
        for i in range(88):
            note = self.note_lookup['12-tone_scale'][i % 12]
            if len(note) == 1:
                self.add_widget(self.keys[i])
        
        for i in range(88):
            note = self.note_lookup['12-tone_scale'][i % 12]
            if len(note) == 2:
                self.add_widget(self.keys[i])
        """

    def __add_vertical_guidelines(self,marker_keys):
        for key in marker_keys: # Should tie together with options to choose keybed interval
            guideline = GuideLine()
            guideline.points = ([key.x,self.y+self.parent.height,
                                 key.x,self.y+self.height])
            self.add_widget(guideline,index=-1)

    def resize_children(self):
        """
        Resizes keys on window resize.
        TODO: work on removing redundant code similar to draw_keybed function
        Note, also doesn't work now with y coordinate
        """

        next_wk_pos = self.x
        next_bk_pos = self.x

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

    def update(self,dt):
        pass

class PianoNote(Widget):
    note = StringProperty(None)
    key_idx = NumericProperty(None)
    start_time = NumericProperty(None)
    channel = NumericProperty(None)

    color = ListProperty([0.2,0.3,0.9,1])
    stroke_color = ListProperty([0.1,0.1,0.1,0.75])

    def is_dormant(self,keybed):
        return (self.y + self.height) < (keybed.y + keybed.height)

    def hits_keybed(self,keybed):
        return self.y < (keybed.y + keybed.height)

    def __lt__(self,other):
        return self.start_time < other.start_time

class PianoRoll(Widget):
    note_lookup = c_utils.load_json(config['theory']['note_lookup_location'])
    
    NS = None
    note_widgets = None
    ticks_passed = 0
    velocity_intensity_scale = 1.5

    song_ended = False

    def init_schedule(self,k):
        """
        TODO:
        need to fix notes' behaviour when resizing.
        """

        self.NS = schedules.NoteSchedule('midi_data/ATC_TWSU_MIDI.mid')
        
        self.note_widgets = deque() # Might implement custom deque to not rely on overloading __lt__
        pianonotes = []

        for channelID,channel in self.NS.channels.items():
            channel.sort()
            
            for note in channel:
                
                corresponding_key = self.parent.keybed.keys[note.note-9]

                pianonote = PianoNote()
                
                key_idx = (note.note-9)
                pianonote.key_idx = key_idx
                pianonote.note = self.note_lookup['12-tone_scale'][key_idx % 12]
                pianonote.start_time = note.time[0]
                pianonote.channel = channelID

                velocity_intensity = note.velocity / (127*self.velocity_intensity_scale) + (1 - 1/self.velocity_intensity_scale)
                if channelID == 0:
                    pianonote.color = [0.8,0.2,0.2,velocity_intensity]
                else:
                    pianonote.color = [0.9,0.4,0.1,velocity_intensity]

                norm_time = note.norm_time(self.NS.schedule_meta_data.ticks_per_beat)
                
                pianonote.width = corresponding_key.width 
                pianonote.height = ( note.time[1] - note.time[0] ) # ( norm_time[1] - norm_time[0] ) # Norm time might be unnecessary since ticks per beat is also used in update which should compensate for any differences
                
                pianonote.y = self.height + self.y #pianonote.y = self.height + note.time[0] + self.y #norm_time[0]
                pianonote.x = corresponding_key.x

                pianonotes.append(pianonote)

        for pianonote in sorted(pianonotes):
            self.note_widgets.append(pianonote)

    def resize_children(self):
        pass

    def add_notes(self):
        while 1:
            if len(self.note_widgets) and self.note_widgets[0].start_time <= self.ticks_passed:
                self.add_widget(self.note_widgets.popleft())
            else:
                break

    def scroll_schedule(self,dt):
        global global_flag
        TPS = self.NS.schedule_meta_data.ticks_per_beat * self.NS.get_BPM() / 60 # With norm_time, 96 should be used as ticks per beat
        
        self.add_notes()

        if not len(self.note_widgets) and not self.song_ended:
            self.song_ended = True

        dormant_children = []

        for child in self.children: # Can also add lines that indicate bar and beats.
            corresponding_key = self.parent.keybed.keys[child.key_idx]

            if child.is_dormant(self.parent.keybed):
                dormant_children.append(child)
                
                corresponding_key.canvas.clear()
                corresponding_key.canvas.add(Color(*corresponding_key.standard_color) ) # breaks when resizing    
                corresponding_key.canvas.add(Rectangle(size=corresponding_key.size,pos=corresponding_key.pos))
            
            elif child.hits_keybed(self.parent.keybed):
                
                corresponding_key.canvas.clear()
                corresponding_key.canvas.add(Color(*child.color[:-1]) )
                #corresponding_key.canvas.add(Color(0.2,0.5,0.9)) # breaks when resizing
                corresponding_key.canvas.add(Rectangle(size=corresponding_key.size,pos=corresponding_key.pos))

            child.y -= TPS*dt # Use this to adjust speed and then use fixed note size
        
        self.ticks_passed += TPS*dt

        while dormant_children:
            self.remove_widget(dormant_children[-1])
            dormant_children.pop()

        if self.ticks_passed >= (TPS*(self.NS.schedule_meta_data.length+6)):
            global_flag = True

    def update(self,dt):
        self.scroll_schedule(dt)

class Stage(Widget):
    keybed = ObjectProperty(None)
    pianoroll = ObjectProperty(None)

    start_time = time.time()

    VM = video_manager.VideoManager(config['video']['tmp_imgs_location'],
                                    width=1920,
                                    height=1080)

    def resize_children(self):
        for child in self.children:
            if 'resize_children' in child.__dir__():
                child.resize_children()

    def update(self,dt):
        self.pianoroll.update(self.VM.meta_data['refresh_rate']) #self.pianoroll.update(dt)
        self.keybed.update(dt)
        self.VM.add_image(self)

        if global_flag: #(time.time() - self.start_time) > 30:
            self.VM.export_video(f"{config['video']['vid_output_location']}{config['video']['default_vid_name']}")
            exit()
        
class Menu(Widget):
    pass

class Workbench(Widget):
    stage = ObjectProperty(None)
    menu = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_resize=self.on_window_resize)

        self.init_stage()

    def on_window_resize(self, window, width, height):
        Clock.schedule_once(self.resize_children,0)

    def init_stage(self):
        Clock.schedule_once(self.stage.keybed.draw_keybed)
        Clock.schedule_once(self.stage.pianoroll.init_schedule)

        Clock.schedule_interval(self.stage.update, 1.0/60.0)

    def resize_children(self,k):
        for child in self.children:
            if 'resize_children' in child.__dir__():
                child.resize_children()

    def update(self,dt):
        pass

class KeysVizuApp(App):

    def build(self):
        
        self.load_kv(config['main']['kv_location'])
        Window.maximize()
        
        workbench = Workbench()
        return workbench

def main():
    KeysVizu = KeysVizuApp()
    KeysVizu.run()

if __name__ == '__main__':
    main()