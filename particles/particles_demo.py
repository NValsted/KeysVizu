from kivy.config import Config
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '640')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

from base.deprecated import pyticles
from base.deprecated import fluids

import random

N = 64
class ParticleScene(FloatLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.fluid_field = fluids.Fluid(64,0.01,0.01,0.01)
        self.particle_system = pyticles.ParticleSystem(self.fluid_field)
        Clock.schedule_interval(lambda dt: self.update_system(),1/30)
        
    def update_system(self):
        self.particle_system.spawn_particles(N=random.randint(-100,30),speed=0.5,angle_spread=3.14,magnitude_spread=1)
        #self.fluid_field.add_velocity(random.randint(27,37),random.randint(27,37),(random.random()-0.5)*5,(random.random()-0.5)*5)
        
        self.particle_system.iterate()
        self.fluid_field.iterate()

        self.canvas.clear()
        with self.canvas:
            for particle in self.particle_system.particles:
                Color(random.random(),(42-particle.age)/42,1,(42-particle.age)/42)
                Rectangle(pos=((particle.coords[0]+N//2)*10,(particle.coords[1]+N//2)*10),size=(3,3))

    def on_touch_down(self,touch):
        self.touch_down_pos = touch.pos

    def on_touch_up(self,touch):
        x_diff = touch.pos[0] - self.touch_down_pos[0]
        y_diff = touch.pos[1] - self.touch_down_pos[1]

        x_pos = int(self.touch_down_pos[0]/10)
        y_pos = int(self.touch_down_pos[1]/10)

        drag_multiplier = 0.5
        self.fluid_field.add_velocity(x_pos,y_pos,x_diff*drag_multiplier,y_diff*drag_multiplier)

class Scene(Widget):
    pass

class ParticlesDemoApp(App):

    def build(self):
        self.load_kv("particles_demo.kv")

def main():
    ParticlesDemo = ParticlesDemoApp()
    ParticlesDemo.run()

if __name__ == '__main__':
    main()