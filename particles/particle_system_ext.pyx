# distutils: language = c++

from libcpp.deque cimport deque
from particle_system cimport ParticleSystem, FluidField, Particle

# Could look into creating two separate classes that represent slave particle systems and a master particle system through which the fluid field is adjusted.

cdef class PyParticleSystem:
    cdef ParticleSystem *c_PS
    cdef FluidField *c_FF
    cdef deque[Particle*] pdeque

    def __cinit__(self,int d,int FF_N,double FF_diffusivity,double FF_viscosity,double FF_dt):
        
        self.c_FF = new FluidField(FF_N,FF_diffusivity,FF_viscosity,FF_dt)
        self.c_PS = new ParticleSystem(self.c_FF,d)

    def __dealloc__(self):
        del self.c_PS

    def spawn_particles(self, int N, double angle, double speed, double size, double angle_spread, double speed_spread, double size_spread, char distribution):
        self.c_PS.spawnParticles(N,angle,speed,size,angle_spread,speed_spread,size_spread,distribution)

    def iterate(self):
        self.c_PS.iterate()

    def get_number_of_particles(self):
        return self.c_PS.particles.size()

    def get_particle_coords(self,particle_idx):
        return [ self.c_PS.particles[particle_idx].coords[0],
                 self.c_PS.particles[particle_idx].coords[1] ]