from kivy.config import Config
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '640')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

from base.deprecated import pyticles

import random

N = 64
class ParticleScene(FloatLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.particle_system = pyticles.ParticleSystem()
        Clock.schedule_interval(lambda dt: self.update_system(),1/30)
        
    def update_system(self):
        self.particle_system.spawn_particles(N=10,speed=0.5,angle_spread=3.14,magnitude_spread=1)
        self.particle_system.iterate()

        self.canvas.clear()
        with self.canvas:
            for particle in self.particle_system.particles:
                Color(random.random(),(42-particle.age)/42,1,(42-particle.age)/42)
                Rectangle(pos=((particle.coords[0]+N//2)*10,(particle.coords[1]+N//2)*10),size=(3,3))

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