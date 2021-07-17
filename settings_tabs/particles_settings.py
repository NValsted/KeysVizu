from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty
from kivy.clock import Clock

from settings_tabs.settings_tab import SettingsTab
from particles.particle_system_manager import ParticleSystemManager
from misc.custom_buttons import ChannelGrid
from misc.numeric_setting import NumericSliderSetting
from misc.gradient_setting import ColorGradientBar

import c_utils
config = c_utils.load_config()


class ParticlesSettings(SettingsTab):
    lifetime_slider = ObjectProperty(NumericSliderSetting)  # Need to properly implement this - should probably make adjustments to c++ source

    spawn_N_slider = ObjectProperty(NumericSliderSetting)
    angle_slider = ObjectProperty(NumericSliderSetting)
    speed_slider = ObjectProperty(NumericSliderSetting)
    size_slider = ObjectProperty(NumericSliderSetting)
    
    angle_spread_slider = ObjectProperty(NumericSliderSetting)
    speed_spread_slider = ObjectProperty(NumericSliderSetting)
    size_spread_slider = ObjectProperty(NumericSliderSetting)

    color_gradient_bar = ObjectProperty(ColorGradientBar)

    active_system = NumericProperty(0)
    active_channels = ObjectProperty(ChannelGrid)

    project_properties = c_utils.load_json(f"{config['project']['projects_location']}{config['project']['default']}")
    PSM = ParticleSystemManager()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.PSM.init_master(self.project_properties["particles"])
        self.active_channels.callback = self.update_channel_map

        Clock.create_trigger(self._set_slider_references)()
        Clock.create_trigger(lambda *args: self.change_system(0))()  # initializes style parameter to proper values

    def _set_slider_references(self, *args):
        self.sliders = [
            self.spawn_N_slider, self.angle_slider,
            self.speed_slider, self.size_slider, 
            self.angle_spread_slider, self.speed_spread_slider,
            self.size_spread_slider
        ]

    def __update_preview(self):
        # Work on making a preview of the active particle system
        pass

    def toggle_particles(self, state):
        self.PSM.ON_status = state == "down"

    def change_system(self, difference):
        self.active_system = min(
            max(self.active_system + difference, 0),
            len(self.PSM.systems) - 1
        )
        self.__update_preview()
        
        # Update style parameters to new active system
        for i in range(16):
            self.active_channels.channel_buttons[i].state = "normal"
            if self.active_system in self.PSM.channel_map[i]:
                self.active_channels.channel_buttons[i].state = "down"

        for slider in self.sliders:
            parameter = self.PSM.styles[self.active_system]
            keys = slider.callback_args[0].split("/")
            for key in keys:
                parameter = parameter[key]
            slider.slider.value = parameter

    def add_system(self):
        self.PSM.add_slave(self.project_properties["particles"])
        self.change_system(float("inf"))  # Always changes to newly added system

    def delete_system(self):
        self.PSM.delete_slave(self.active_system, self.project_properties)
        self.change_system(-1)

    def update_channel_map(self, button):
        channel_map = self.PSM.channel_map[button.channel_id]
        if button.state == "down":
            channel_map.add(self.active_system)
        elif self.active_system in channel_map:  # should never be false at this point, but double check in case of unexpected behaviour
            channel_map.remove(self.active_system)

    def change_slider_setting(self, callback_args):
        self.PSM.update_style_parameters(
            self.active_system,
            {callback_args[0]: callback_args[1].value}
        )
        self.__update_preview()
