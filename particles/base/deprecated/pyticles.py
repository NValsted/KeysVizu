import numpy as np
import time
from collections import deque

from . import fluids

class Particle:
    coords = [] # x,y
    velocity = []
    size = None
    age = 0
    #mass = None

    def __init__(self,**kwargs):
        for k,v in kwargs.items():
            exec(f"self.{k}={v}")

class ParticleSystem:
    particles = deque()
    fluid = None

    def __init__(self,fluid):
        self.fluid = fluid

    def spawn_particles(self,N = 1,
                        angle = 0, speed = 1, size = 1,
                        angle_spread = 0.1,
                        magnitude_spread = 0.1,
                        size_spread = 0.1,
                        distribution=np.random.uniform):
        
        for particle in range(N):
            randomized_angle = angle + distribution(-angle_spread,angle_spread)
            randomized_speed = speed + distribution(-magnitude_spread,magnitude_spread)
            randomized_size  = size  + distribution(-size_spread,size_spread)

            randomized_velocity = [np.cos(randomized_angle)*randomized_speed,
                                   np.sin(randomized_angle)*randomized_speed]

            p = Particle(coords = [0,0],
                         velocity = randomized_velocity,
                         size = 1)

            self.particles.append(p)

    def iterate(self):
        to_be_popped_count = 0
        for particle in self.particles:
            if particle.age > 42:
                to_be_popped_count += 1
            
            particle.velocity[0] += self.fluid.velocity_x[int(particle.coords[0])+32][int(particle.coords[1])+32]
            particle.velocity[1] += self.fluid.velocity_y[int(particle.coords[0])+32][int(particle.coords[1])+32]
            
            particle.velocity[0] -= (particle.velocity[0] * 0.05) # drag
            particle.velocity[1] -= (particle.velocity[1] * 0.05) # drag 

            particle.coords[0] += particle.velocity[0]
            particle.coords[1] += particle.velocity[1]
            
            if particle.coords[0] > 31:
                particle.coords[0] = 31

            if particle.coords[1] > 31:
                particle.coords[1] = 31

            if particle.coords[0] < -32:
                particle.coords[0] = -32

            if particle.coords[1] < -32:
                particle.coords[1] = -32

            particle.age += 1

        while to_be_popped_count:
            self.particles.popleft()
            to_be_popped_count -= 1


def main():
    FluidField = fluids.Fluid(64,0.01,0.01,0.01)

    particle_system = ParticleSystem(FluidField)
    particle_system.spawn_particles(N=3)
    for i in range(100):
        
        print("At iteration:", i)
        for p in particle_system.particles:
            print(p.coords)

        particle_system.iterate()
        time.sleep(0.2)

if __name__ == '__main__':
    main()