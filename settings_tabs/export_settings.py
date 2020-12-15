from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty
from kivy.clock import Clock

from settings_tabs.settings_tab import SettingsTab

from video_tools import video_manager

import c_utils
config = c_utils.load_config()

class ExportSettings(SettingsTab):
    wh_group = ObjectProperty(None)
    
    stage = ObjectProperty(None)
    menu = ObjectProperty(None)

    export_path_icon_button = ObjectProperty(None)
    export_path_text_button = ObjectProperty(None)
    export_path = f"{config['video']['vid_output_location']}{config['video']['default_vid_name']}"

    VM = video_manager.VideoManager(config['video']['tmp_imgs_location'],
                                    width=1920,
                                    height=1080,
                                    FPS=10.0)#FPS=60.0)
    VM.formats = [".avi",".bongo"] # temporary for testing the drop-down menu and similar functionality

    def select_export_path_location(self):
        self.show_file_chooser(dialog_type = "save",
                               initial_directory = './video_tools/videos',
                               callback = self.update_export_path)

    def update_export_path(self,export_path):
        self.export_path = export_path
        self.export_path_text_button.text = export_path.split("/")[-1]

    def _update_stage(self,dt):
        self.stage.update(dt)
        self.VM.add_image(self.stage)

        self.TPS = self.stage.pianoroll.NS.schedule_meta_data.ticks_per_beat * self.stage.pianoroll.NS.get_BPM() / 60

    def export_video(self):
        print("we exportin'")
        
        self.stage.pianoroll.init_schedule(self.stage.pianoroll.NS.schedule_meta_data.file_path,
                                           self.menu.style_settings.channel_styles)
        
        self.VM.compute_derived_meta_data()
        
        self.stage_update_event = Clock.schedule_interval(self._update_stage, 1.0/60.0)
        
        self.TPS = 192
        
        while self.stage.pianoroll.ticks_passed < (self.TPS*(self.stage.pianoroll.NS.schedule_meta_data.length+6)):
            pass
        
        self.stage_update_event.cancel()
        self.VM.export_video(self.export_path)

        print("we done")