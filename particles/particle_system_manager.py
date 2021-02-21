from kivy.graphics import Color, Rectangle

import random
import numpy as np

import c_utils
config = c_utils.load_config()

from particles import particle_system_ext as pse

class ParticleSystemManager:
    systems = [None] # 0 is master system
    styles = {}
    stage = None
    active_particles = []

    def __init__(self):
        pass

    def init_master(self,parameters):
        self.systems[0] = pse.PyMasterParticleSystem(parameters["init"]["drag_coef"],
                                                     parameters["init"]["fluid_N"],
                                                     parameters["init"]["diffusivity"],
                                                     parameters["init"]["viscosity"],
                                                     parameters["init"]["dt"])

        self.styles[self.systems[0]] = parameters["spawn"]
        self.fluid_N = parameters["init"]["fluid_N"]

    def add_slave(self,parameters):
        new_system = pse.PySlaveParticleSystem(parameters["init"]["drag_coef"],self.systems[0])
        
        self.systems.append(new_system)
        self.styles[new_system] = parameters["spawn"]

    def update(self):
        for system in self.systems:
            system.iterate()
        
        for system in self.systems:
            self.redraw_particles(system)

    def _map_pos_fts(self,pos):
        x = pos[0] / self.fluid_N
        y = pos[1] / self.fluid_N

        x *= self.stage.width
        y *= self.stage.height

        x += self.stage.center_x
        y += self.stage.center_y
        
        return (x,y)

    def _map_pos_stf(self,pos):
        x = pos[0] - self.stage.center_x
        y = pos[1] - self.stage.center_y
        
        x /= self.stage.width
        x *= self.fluid_N

        y /= self.stage.height
        y *= self.fluid_N
        
        return (x,y)

    def redraw_particles(self,particle_system):
        while self.active_particles:
            self.stage.canvas.remove(self.active_particles.pop())

        for i in range(particle_system.get_number_of_particles()):
            particle_coords = self._map_pos_fts(particle_system.get_particle_coords(i))
            particle_size = particle_system.get_particle_size(i)
            particle_age = particle_system.get_particle_age(i)
            particle_col = Color(random.random(),(42-particle_age)/42,1,(42-particle_age)/42)
            particle_rect = Rectangle(pos=(particle_coords[0],particle_coords[1]),size=(particle_size,particle_size))
            
            self.stage.canvas.add(particle_col)
            self.stage.canvas.add(particle_rect)
            self.active_particles.append(particle_col)
            self.active_particles.append(particle_rect)

    def spawn_particles(self,pos):
        for system in self.systems:
            mapped_pos = self._map_pos_stf(pos)
            system.spawn_particles(self.styles[system]["N"],
                                   self.styles[system]["angle"], self.styles[system]["speed"],
                                   self.styles[system]["size"], np.array(mapped_pos,dtype=np.float64),
                                   self.styles[system]["angle_spread"], self.styles[system]["speed_spread"],
                                   self.styles[system]["size_spread"], np.array(self.styles[system]["position_spread"],dtype=np.float64),
                                   ord(self.styles[system]["distribution"][0]))

def main():
    pass

if __name__ == '__main__':
    main()