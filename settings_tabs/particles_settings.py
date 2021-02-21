from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty
from kivy.clock import Clock

from settings_tabs.settings_tab import SettingsTab
from particles.particle_system_manager import ParticleSystemManager

import c_utils
config = c_utils.load_config()

class ParticlesSettings(SettingsTab):

    project_properties = c_utils.load_json(f"{config['project']['projects_location']}{config['project']['default']}")
    PSM = ParticleSystemManager()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.PSM.init_master(self.project_properties["particles"])
        