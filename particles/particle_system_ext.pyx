# distutils: language = c++

from libcpp.deque cimport deque
from particle_system cimport ParticleSystem, FluidField, Particle

cdef class ParticleSystemInterface:
    cdef ParticleSystem *c_PS
    cdef double[:] *position
    cdef double[:] *position_spread
    
    def __cinit__(self):
        pass

    def __dealloc__(self):
        pass

    def spawn_particles(self, int N, int t,
                        double angle, double speed, double size, double[:] position,
                        double angle_spread, double speed_spread, double size_spread,
                        double[:] position_spread, char distribution):
        
        self.c_PS.spawnParticles(N,t,angle,speed,size,&position[0],angle_spread,speed_spread,size_spread,&position_spread[0],distribution)

    def iterate(self):
        self.c_PS.iterate()

    def get_number_of_particles(self):
        return self.c_PS.particles.size()

    def get_particle_coords(self,particle_idx):
        return [ self.c_PS.particles[particle_idx].coords[0],
                 self.c_PS.particles[particle_idx].coords[1] ]

    def get_particle_size(self,particle_idx):
        return self.c_PS.particles[particle_idx].size

    def get_particle_age(self,particle_idx):
        return self.c_PS.particles[particle_idx].age

cdef class PyMasterParticleSystem(ParticleSystemInterface):
    cdef FluidField *c_FF
    cdef deque[Particle*] pdeque

    def __cinit__(self, int d, int lt,
                  int FF_N, double FF_diffusivity,
                  double FF_viscosity,double FF_dt):
                  
        self.c_FF = new FluidField(FF_N,FF_diffusivity,FF_viscosity,FF_dt)
        self.c_PS = new ParticleSystem(self.c_FF,d,lt)

    def __dealloc__(self):
        del self.c_PS
        del self.c_FF

    def IDX(self, int i, int j):
        return self.c_FF.IDX(i,j)

    def get_density(self, int i, int j):
        return self.c_FF.getDensity(i,j)

    def get_velocity_x(self, int i, int j):
        return self.c_FF.getVelocityX(i,j)

    def get_velocity_y(self, int i, int j):
        return self.c_FF.getVelocityY(i,j)

    def add_density(self, int x, int y, double amount):
        self.c_FF.addDensity(x,y,amount)

    def add_velocity(self, int x, int y, double amount_x, double amount_y):
        self.c_FF.addVelocity(x,y,amount_x,amount_y)

    def iterate(self):
        self.c_FF.iterate()
        self.c_PS.iterate()

cdef class PySlaveParticleSystem(ParticleSystemInterface):
    def __cinit__(self, int d, int lt, PyMasterParticleSystem master):
        self.c_PS = new ParticleSystem(master.c_FF,d,lt)

    def __dealloc__(self):
        del self.c_PS