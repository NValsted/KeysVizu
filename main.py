# Configuration
import c_utils
from kivy.config import Config

# Global scope
config = c_utils.load_config()

# Kivy config variables
Config.read(config["main"]["kivy_config"])

# Kivy-specific imports
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.graphics import Color, Rectangle

# Built-in python libraries
import os
import time
import random
from collections import deque

# Third-party libraries
import numpy as np

# Custom libraries
from midi_tools import schedules
from video_tools import video_manager

from misc.custom_buttons import *
from misc.numeric_setting import *
from misc.style_previews import *
from misc.linked_fields import *
from misc.custom_dropdowns import *

from settings_tabs.project_settings import ProjectSettings 
from settings_tabs.style_settings import StyleSettings
from settings_tabs.export_settings import ExportSettings
from settings_tabs.particles_settings import ParticlesSettings

class PianoKey(Widget):
    note = StringProperty(None)

class BlackKey(PianoKey):
    standard_color = ListProperty([0.1,0.1,0.1])

class WhiteKey(PianoKey):
    standard_color = ListProperty([1,1,1])

class GuideLine(Widget):
    standard_color = ListProperty([0.15,0.15,0.15,0.5])
    guideline_width = NumericProperty(1.5)
    points = ListProperty([None])

class Keybed(Widget):
    note_lookup = c_utils.load_json(config['theory']['note_lookup_location'])
    marker_notes = {"C"} #{"C","F"}
    
    key_width_offset = 2
    white_black_width_ratio = (13/16) / (15/32)
    white_black_length_ratio = 23 / 16

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keys = []
        self.first_key_offset = 0 # Offset from A1

    def draw_keybed(self,key_range=["A1","C8"]):
        """
        Initializes the keybed from a given range of keys.
        """
        
        # Should assert that key range never has black keys as endpoints. Could possible do this in GUI with a dropdown that only contains notes white keys.
        keys,white_keys,black_keys = self.__keys_in_range(key_range)

        next_wk_pos = 0
        next_bk_pos = 0
        marker_keys = []

        for note in keys:
            if len(note) == 1:
                key = WhiteKey()
                key.note = note
                key.width = self.width/(len(white_keys)) - self.key_width_offset
                key.height = self.height

                key.center_x = self.width*next_wk_pos + key.width/2 + self.key_width_offset/2 + self.x
                key.y = self.y
                
                next_wk_pos += 1/(len(white_keys))
                next_bk_pos = next_wk_pos

                self.keys.append(key)
                self.add_widget(key,index=-1)

            else:
                key = BlackKey()
                key.note = note
                key.width = self.width/(len(white_keys)) / self.white_black_width_ratio
                key.height = self.height / self.white_black_length_ratio

                key.center_x = self.width*next_bk_pos + self.x
                key.y = self.height - key.height + self.y
                
                next_bk_pos = next_wk_pos + 1/(len(white_keys)*2)

                self.keys.append(key)
                self.add_widget(key)
                
            if note in self.marker_notes:
                marker_keys.append(key)
        
        self.__add_vertical_guidelines(marker_keys)

    def __key_range_len(self,key_range): # Function is not quite right, since it assumes the labelling goes A0, A#, ... G#0, A1, ... 
        # Should implement checks somewhere that note_0 is lower than note_1
        note_0 = self.note_lookup['12-tone_to_int'][key_range[0][:-1]]
        note_1 = self.note_lookup['12-tone_to_int'][key_range[1][:-1]]

        octave_range = int(key_range[1][-1]) - int(key_range[0][-1])
        if note_1 - note_0 < 0:
            octave_range -= 1

        base_interval = octave_range * 12
        
        return base_interval + ((note_1 - note_0) % 12) + 1

    def __keys_in_range(self,key_range):
        white_keys = []
        black_keys = []
        keys = []

        self.first_key_offset = self.__key_range_len(["A1",key_range[0]]) - 1
        range_end = self.first_key_offset + self.__key_range_len(key_range)
        
        for i in range(self.first_key_offset,range_end):
            note = self.note_lookup['12-tone_scale'][i % 12]
            
            if len(note) == 1: # Currently not using white_keys and black_keys lists for other than their length
                white_keys.append(note)
            else:
                black_keys.append(note)
            
            keys.append(note)

        return keys, white_keys, black_keys

    def __add_vertical_guidelines(self,marker_keys):
        for key in marker_keys: # Should tie together with options to choose keybed interval
            guideline = GuideLine()
            guideline.points = ([key.x,self.y+self.parent.height,
                                 key.x,self.y+self.height])
            self.add_widget(guideline,index=-1)

    def resize_children(self):
        """
        Resizes keys on window resize.
        """
        pass

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

    PSM_reference = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def init_schedule(self,midi_location,channel_styles):
        """
        TODO:
        need to properly reset all values and remove notes on screen when re-initializing schedule.
        Might implement checks to see whether file was changed or if it's the same one. In the latter, case the schedule should resume at the same location.
        """
        
        self.NS = schedules.NoteSchedule(midi_location)
        self.ticks_passed = 0

        self.note_widgets = deque() # Might implement custom deque to not rely on overloading __lt__
        pianonotes = []
        
        for channelID,channel in self.NS.channels.items():
            channel.sort()
            
            for note in channel:
                pianonote = PianoNote()
                
                key_idx = (note.note-(21+self.parent.keybed.first_key_offset))
                pianonote.key_idx = key_idx
                corresponding_key = self.parent.keybed.keys[key_idx]

                pianonote.note = self.note_lookup['12-tone_scale'][key_idx % 12]
                pianonote.start_time = note.time[0]
                pianonote.channel = channelID

                """
                velocity_intensity = note.velocity / (127*self.velocity_intensity_scale) + (1 - 1/self.velocity_intensity_scale)
                if channelID == 0:
                    pianonote.color = [0.2,0.2,0.8,velocity_intensity]
                else:
                    pianonote.color = [0.8,0.3,0.4,velocity_intensity]
                """

                velocity_intensity = note.velocity / (127*channel_styles[channelID]['notes']['velocity_scaling']) + (1 - 1/channel_styles[channelID]['notes']['velocity_scaling'])
                pianonote.color = [*channel_styles[channelID]['notes']['white_key_color'],velocity_intensity]

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
        TPS = self.NS.schedule_meta_data.ticks_per_beat * self.NS.get_BPM() / 60 # With norm_time, 96 should be used as ticks per beat
        
        self.add_notes()

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
                corresponding_key.canvas.add(Rectangle(size=corresponding_key.size,pos=corresponding_key.pos))
                
                self.PSM_reference.spawn_particles((corresponding_key.center_x,corresponding_key.top))

            child.y -= TPS*dt # Use this to adjust speed and then use fixed note size
        
        self.ticks_passed += TPS*dt

        while dormant_children:
            self.remove_widget(dormant_children[-1])
            dormant_children.pop()

    def update(self,dt):
        self.scroll_schedule(dt)

class Stage(Widget):
    keybed = ObjectProperty(None)
    pianoroll = ObjectProperty(None)
    
    #fluid_N = 64
    #particle_system = pse.PyMasterParticleSystem(2,fluid_N,0.01,0.01,0.01)
    #active_particles = []
    
    VM_reference = None
    PSM_reference = None

    def resize_children(self):
        for child in self.children:
            if 'resize_children' in child.__dir__():
                child.resize_children()

    """
    def _test_PS(self):
        self.particle_system.spawn_particles(3,
                                             0,1.5,2,np.array([0,0],dtype=np.float64),
                                             3.14,1.5,0.5,np.array([0,0],dtype=np.float64),
                                             ord('u'[0]))
        self.particle_system.iterate()

        while self.active_particles:
            self.canvas.remove(self.active_particles.pop()) 
        
        for i in range(self.particle_system.get_number_of_particles()):
            particle_coords = self.particle_system.get_particle_coords(i)
            particle_size = self.particle_system.get_particle_size(i)
            particle_age = self.particle_system.get_particle_age(i)

            particle_col = Color(random.random(),(42-particle_age)/42,1,(42-particle_age)/42)
            particle_rect = Rectangle(pos=((particle_coords[0]*10)+400,(particle_coords[1]*10)+500),size=(particle_size,particle_size))
            self.canvas.add(particle_col)
            self.canvas.add(particle_rect)
            self.active_particles.append(particle_col)
            self.active_particles.append(particle_rect)
    """

    def update(self,dt):
        self.pianoroll.update(dt)
        self.keybed.update(dt)
        self.PSM_reference.update()

class ProjectTimeline(Widget):
    stage = ObjectProperty(None)
    play_button = ObjectProperty(None)
    stop_button = ObjectProperty(None)
    
    stage_update_event = None

    def toggle_play(self): # Implement checks to make sure stage_update_event isn't triggered when no schedule is loaded 
        if self.play_button.state == "down":
            self.stage_update_event = Clock.schedule_interval(self.stage.update, 1.0/60.0)
        else:
            self.stage_update_event.cancel()

class Menu(Widget):
    project_settings = ObjectProperty(None)
    style_settings = ObjectProperty(None)
    particles_settings = ObjectProperty(None)
    export_settings = ObjectProperty(None)
    tabbed_panel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_TPTs_event = Clock.schedule_interval(lambda dt:
                                                       self.__load_tabbed_panel_tabs(),
                                                       1/config['main']['init_update_freq'])

    def __load_tabbed_panel_tabs(self):
        if len(self.tabbed_panel.tab_list) > 1:
            self.load_TPTs_event.cancel()
            
            for tab in reversed(self.tabbed_panel.tab_list):
                Clock.schedule_once(lambda dt: self.tabbed_panel.switch_to(tab))

class Workbench(Widget):
    stage = ObjectProperty(None)
    project_timeline = ObjectProperty(None)
    menu = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_resize=self.on_window_resize)
        
        self.__pass_references_to_menu()
        self.__init_stage()

    def on_window_resize(self, window, width, height):
        Clock.schedule_once(self.resize_children,0)
    
    def __pass_references_to_menu(self):
        self.menu.project_settings.pianoroll = self.stage.pianoroll
        self.menu.project_settings.menu = self.menu
        
        self.menu.style_settings.pianoroll = self.stage.pianoroll
        
        self.menu.export_settings.stage = self.stage
        self.menu.export_settings.menu = self.menu

        self.project_timeline.stage = self.stage
        
        self.stage.VM_reference = self.menu.export_settings.VM
        self.stage.PSM_reference = self.menu.particles_settings.PSM
        self.stage.PSM_reference.stage = self.stage
        self.stage.pianoroll.PSM_reference = self.menu.particles_settings.PSM

    def __init_stage(self):
        Clock.schedule_once(lambda dt: self.stage.keybed.draw_keybed())

    def resize_children(self,k):
        for child in self.children:
            if 'resize_children' in child.__dir__():
                child.resize_children()

    def update(self,dt):
        pass

class KeysVizuApp(App):

    def build(self):
        self.load_kv(config['main']['kv_location'])
        #Window.maximize() # The whole maximization thing is a mess. Currently only scales window to Full HD resolution. 
        # Could possibly implement functionality that checks the user's current resolution and updates the kivy_config.ini file.
        
        workbench = Workbench()
        
        return workbench

def main():
    KeysVizu = KeysVizuApp()
    KeysVizu.run()

if __name__ == '__main__':
    main()