from kivy.config import Config
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '640')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

import particle_system_ext

import random
import numpy as np

N = 64
class ParticleScene(FloatLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.particle_system = particle_system_ext.PyMasterParticleSystem(2,20,N,0.01,0.01,0.01)
        self.slave_particle_system = particle_system_ext.PySlaveParticleSystem(10,10,self.particle_system)
        Clock.schedule_interval(lambda dt: self.update_system(),1/30)
        
    def update_system(self):
        self.particle_system.spawn_particles(random.randint(-100,30), 0,
                                             0,0.5,2,np.array([0,0],dtype=np.float64),
                                             3.14,0.5,0.1,np.array([0,0],dtype=np.float64),
                                             ord('u'[0]))
        self.particle_system.iterate()

        self.slave_particle_system.spawn_particles(random.randint(-100,30), 1,
                                                   0,0.5,1,np.array([0,0],dtype=np.float64),
                                                   3.14,0.5,2,np.array([10,10],dtype=np.float64),
                                                   ord('u'[0]))
        self.slave_particle_system.iterate()

        self.canvas.clear()
        with self.canvas:
            for i in range(self.particle_system.get_number_of_particles()):
                
                particle_coords = self.particle_system.get_particle_coords(i)
                particle_size = self.particle_system.get_particle_size(i)
                particle_age = self.particle_system.get_particle_age(i)

                Color(random.random(),(42-particle_age)/42,1,(42-particle_age)/42)
                Rectangle(pos=((particle_coords[0]+N//2)*10,(particle_coords[1]+N//2)*10),size=(particle_size,particle_size))

            for i in range(self.slave_particle_system.get_number_of_particles()):
                
                particle_coords = self.slave_particle_system.get_particle_coords(i)
                particle_size = self.slave_particle_system.get_particle_size(i)
                particle_age = self.slave_particle_system.get_particle_age(i)
                
                Color(0.9,random.random()/2,0.3,(42-particle_age)/42)
                Rectangle(pos=((particle_coords[0]+N//2)*10,(particle_coords[1]+N//2)*10),size=(particle_size,particle_size))

    def on_touch_down(self,touch):
        self.touch_down_pos = touch.pos
    
    def on_touch_up(self,touch):
        x_diff = touch.pos[0] - self.touch_down_pos[0]
        y_diff = touch.pos[1] - self.touch_down_pos[1]

        x_pos = int(self.touch_down_pos[0]/10)
        y_pos = int(self.touch_down_pos[1]/10)

        drag_multiplier = 0.5
        self.particle_system.add_velocity(x_pos,y_pos,x_diff*drag_multiplier,y_diff*drag_multiplier)
        
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
