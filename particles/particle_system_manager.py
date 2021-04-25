from kivy.graphics import Color, Rectangle

from copy import deepcopy
import random

import numpy as np

import c_utils
config = c_utils.load_config()

from particles import particle_system_ext as pse

class ParticleSystemManager:
    systems = [None] # 0 is master system
    styles = [None]
    stage = None
    active_particles = []
    ON_status = False

    def __init__(self):
        pass

    def init_master(self,parameters):
        self.styles[0] = deepcopy(parameters)
        self.systems[0] = pse.PyMasterParticleSystem(self.styles[0]["init"]["drag_coef"],
                                                     self.styles[0]["init"]["lifetime"],
                                                     self.styles[0]["init"]["fluid_N"],
                                                     self.styles[0]["init"]["diffusivity"],
                                                     self.styles[0]["init"]["viscosity"],
                                                     self.styles[0]["init"]["dt"])

        self.fluid_N = self.styles[0]["init"]["fluid_N"]
        self.particle_lifetime = self.styles[0]["init"]["lifetime"]

    def add_slave(self,parameters):
        self.styles.append(deepcopy(parameters))
        new_system = pse.PySlaveParticleSystem(self.styles[-1]["init"]["drag_coef"],
                                               self.styles[-1]["init"]["lifetime"],
                                               self.systems[0])
        
        self.systems.append(new_system)

    def update_style_parameters(self,system_idx,kwargs):        
        parameter = self.styles[system_idx]
        for k,v in kwargs.items():
            keys = k.split("/")
            for key in keys[:-1]:
                parameter = parameter[key]
            parameter[keys[-1]] = v

    def update(self):
        
        for system in self.systems:
            system.iterate()
        
        for system in self.systems:
            self.redraw_particles(system)

    def _map_pos_fts(self,pos):
        x = pos[0] - self.fluid_N//2
        y = pos[1] - self.fluid_N//2

        x /= self.fluid_N
        y /= self.fluid_N

        x *= self.stage.width
        y *= self.stage.height

        x += self.stage.center_x
        y += self.stage.center_y
        
        return (x,y)

    def _map_pos_pts(self,pos):
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
        y /= self.stage.height

        x *= self.fluid_N
        y *= self.fluid_N

        x += self.fluid_N//2
        y += self.fluid_N//2

        return (x,y)

    def _map_pos_stp(self,pos):
        x = pos[0] - self.stage.center_x
        y = pos[1] - self.stage.center_y
        
        x /= self.stage.width
        y /= self.stage.height

        x *= self.fluid_N
        y *= self.fluid_N

        return (x,y)

    def redraw_particles(self,particle_system):
        while self.active_particles:
            self.stage.canvas.remove(self.active_particles.pop())

        for i in range(particle_system.get_number_of_particles()):

            particle_coords = self._map_pos_pts(particle_system.get_particle_coords(i))
            particle_size = particle_system.get_particle_size(i)
            particle_age = particle_system.get_particle_age(i)

            particle_col = Color(random.random(),
                                 (self.particle_lifetime-particle_age)/self.particle_lifetime,
                                 1,
                                 (self.particle_lifetime-particle_age)/self.particle_lifetime)

            particle_rect = Rectangle(pos=(particle_coords[0],particle_coords[1]),size=(particle_size,particle_size))
            
            self.stage.canvas.add(particle_col)
            self.stage.canvas.add(particle_rect)
            self.active_particles.append(particle_col)
            self.active_particles.append(particle_rect)

    def spawn_particles(self,pos):
        for i,system in enumerate(self.systems):
            mapped_pos = self._map_pos_stp(pos)
            
            system.spawn_particles(self.styles[i]["spawn"]["N"],
                                   self.styles[i]["spawn"]["angle"], self.styles[i]["spawn"]["speed"],
                                   self.styles[i]["spawn"]["size"], np.array(mapped_pos,dtype=np.float64),
                                   self.styles[i]["spawn"]["angle_spread"], self.styles[i]["spawn"]["speed_spread"],
                                   self.styles[i]["spawn"]["size_spread"], np.array(self.styles[i]["spawn"]["position_spread"],dtype=np.float64),
                                   ord(self.styles[i]["spawn"]["distribution"][0]))

    def strike_fluid(self,pos):
        mapped_pos = self._map_pos_stf(pos)
        
        self.systems[0].add_velocity(int(mapped_pos[0]),
                                     int(mapped_pos[1])+random.randint(0,5),
                                     random.uniform(-1,1),
                                     random.uniform(-0.5,1))

    def trigger_hit(self,pos): # velocity could be passed as well to adjust strike_fluid strength
        if self.ON_status:
            self.spawn_particles(pos)
            self.strike_fluid(pos)

def main():
    pass

if __name__ == '__main__':
    main()