from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty, ObjectProperty, ListProperty

import numpy as np

import c_utils
config = c_utils.load_config()


class ColorGradientBar(BoxLayout):
    bar_texture = ObjectProperty(Texture)
    default_color_properties = c_utils.load_json(
        f"{config['project']['projects_location']}{config['project']['default']}"
    )["particles"]["style"]["color"]
    
    def __init__(self, **kwargs):
        super(ColorGradientBar, self).__init__(**kwargs)
        self.bar_texture = self.create_gradient_texture(
            self.default_color_properties
        )

    def create_gradient_texture(self, color_properties, resolution=(64, 64)):
        texture = Texture.create(size=resolution, colorfmt="rgba")

        buf = np.zeros((*resolution, 4), dtype=np.ubyte)
        for i in range(resolution[0]):
            RGBA_val = c_utils.interpolate_color(color_properties, i / 64)
            for j in range(4):
                buf[:,i,j] = RGBA_val[j] * 255
        
        texture.blit_buffer(buf.ravel(), colorfmt="rgba", bufferfmt="ubyte")
        return texture
