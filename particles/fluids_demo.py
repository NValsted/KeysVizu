from kivy.config import Config
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '640')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

from base import fluids_base_ext

import random
globalFluidField = fluids_base_ext.pyFluidField(64,0.2,0.1,0.001)

class ParticleScene(FloatLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.FluidField = globalFluidField #Fluid(32, 0.2, 0.1, 0.001)
        Clock.schedule_interval(lambda dt: self.update_field(),1/30)
        
    def update_field(self):
        self.FluidField.add_velocity(31,31,random.randint(-100,100),random.randint(-100,100))
        self.FluidField.add_density(31,31,3)
        self.FluidField.iterate() # Benchmark fps without drawing to gauge performance if get_density gets improved - https://gist.github.com/GaelVaroquaux/1249305

        self.canvas.clear()
        with self.canvas:
            for j in range(64):
                for i in range(64):
                    Color(0,0,self.FluidField.get_density(i,j),1)
                    Rectangle(pos=(i*10,j*10),size=(10,10))
    
    def on_touch_down(self,touch):
        self.touch_down_pos = touch.pos

    def on_touch_up(self,touch):
        x_diff = touch.pos[0] - self.touch_down_pos[0]
        y_diff = touch.pos[1] - self.touch_down_pos[1]

        x_pos = int(self.touch_down_pos[0]/10)
        y_pos = int(self.touch_down_pos[1]/10)

        drag_multiplier = 30
        self.FluidField.add_velocity(x_pos,y_pos,x_diff*drag_multiplier,y_diff*drag_multiplier)
        self.FluidField.add_density(x_pos,y_pos,10)

class Scene(Widget):
    pass

class FluidsDemoApp(App):

    def build(self):
        self.load_kv("fluids_demo.kv")

def main():
    FluidsDemo = FluidsDemoApp()
    FluidsDemo.run()

if __name__ == '__main__':
    main()