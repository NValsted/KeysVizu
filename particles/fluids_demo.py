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

N = 64
globalFluidField = fluids_base_ext.pyFluidField(N,0.01,0.01,0.01)

class FluidScene(FloatLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.FluidField = globalFluidField
        Clock.schedule_interval(lambda dt: self.update_field(),1/30)

        self.square_val = {}
        for j in range(N):
            for i in range(N):
                self.square_val[f"{i},{j}"] = 0
        
    def update_field(self):
        self.FluidField.add_velocity(N//2,N//2,random.randint(-100,100),random.randint(-100,100))
        self.FluidField.add_density(N//2,N//2,10)
        self.FluidField.iterate()

        if random.randint(0,100) == 69:
            self.canvas.clear()
            for j in range(N):
                for i in range(N):
                    self.square_val[f"{i},{j}"] = 0

        with self.canvas:
            for j in range(N):
                for i in range(N):
                    # Look into this https://kivy.org/doc/stable/api-kivy.graphics.texture.html
                    # Introduced a scuffed way to detect what rectangles change significantly and only redraw those
                    if abs(self.FluidField.get_density(i,j) - self.square_val[f"{i},{j}"]) > 0.05:
                        Color(0,0,self.FluidField.get_density(i,j),1) 
                        Rectangle(pos=(i*10,j*10),size=(10,10))
                        self.square_val[f"{i},{j}"] = self.FluidField.get_density(i,j)
                    
    

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