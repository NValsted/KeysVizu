from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty
from kivy.clock import Clock

from settings_tabs.settings_tab import SettingsTab
from particles.particle_system_manager import ParticleSystemManager

import c_utils
config = c_utils.load_config()

class ParticlesSettings(SettingsTab):
    spawn_N_slider = ObjectProperty(None)
    angle_slider = ObjectProperty(None)
    speed_slider = ObjectProperty(None)
    size_slider = ObjectProperty(None)
    angle_spread_slider = ObjectProperty(None)
    speed_spread_slider = ObjectProperty(None)
    size_spread_slider = ObjectProperty(None)

    project_properties = c_utils.load_json(f"{config['project']['projects_location']}{config['project']['default']}")
    PSM = ParticleSystemManager()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.PSM.init_master(self.project_properties["particles"])
        self.system_idx = 0

    def __update_preview(self):
        # Work on making a preview of the active particle system
        pass

    def toggle_particles(self,state):
        self.PSM.ON_status = state == "down"

    def change_slider_setting(self,callback_args):
        self.PSM.update_style_parameters(self.system_idx,{callback_args[0]:callback_args[1].value})
        self.__update_preview()