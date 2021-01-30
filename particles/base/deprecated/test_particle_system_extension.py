import particle_system_ext
import time

from base.deprecated import fluids
from base.deprecated import pyticles

PS = particle_system_ext.PyParticleSystem(0.5,64,0.1,0.1,0.01)

print("C++ implementation")
start_time = time.time()
count = 0
for i in range(3000):
    PS.spawn_particles(50,
                       0, 1, 1,
                       0.1, 0.1, 0.1,
                       ord('u'[0]))

    PS.iterate()
    for i in range(PS.get_number_of_particles()):
        PS.get_particle_coords(i)
    
    count += 1
    if time.time() - start_time > 1:
        print(f"iterations per seconds: {count/(time.time() - start_time)}")
        count = 0
        start_time = time.time()

####

FluidField = fluids.Fluid(64,0.01,0.01,0.01)
particle_system = pyticles.ParticleSystem(FluidField)

print("Python implementation")
start_time = time.time()
count = 0
for i in range(300):
    particle_system.spawn_particles(N=50)
    FluidField.iterate()
    particle_system.iterate()
    for particle in particle_system.particles:
        particle

    count += 1
    if time.time() - start_time > 1:
        print(f"iterations per seconds: {count/(time.time() - start_time)}")
        count = 0
        start_time = time.time()