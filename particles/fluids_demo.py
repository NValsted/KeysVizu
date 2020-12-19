from kivy.config import Config
Config.set('graphics', 'width', '320')
Config.set('graphics', 'height', '320')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import Callback

from fluids import Fluid

import random

class ParticleScene(FloatLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.FluidField = Fluid(32, 0.2, 0.1, 0.001)
        Clock.schedule_interval(lambda dt: self.update_field(),1/30)

    def update_field(self):
        self.FluidField.add_velocity(15,15,random.randint(-100,100),random.randint(-100,100))
        self.FluidField.add_density(15,15,2)
        self.FluidField.iterate()

        self.canvas.clear()
        with self.canvas:
            for i,row in enumerate(self.FluidField.density):
                for j,val in enumerate(row):
                    Color(0,val/2,val,1)
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