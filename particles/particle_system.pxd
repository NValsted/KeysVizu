from libcpp.deque cimport deque
from base.fluids_base cimport FluidField

cdef extern from "particle_system.cpp":
    pass

cdef extern from "particle_system.h" namespace "particles":
    cdef cppclass Particle:
        Particle(double *, double *, double, int)
        double *coords
        int age
        double size

    cdef cppclass ParticleSystem:
        ParticleSystem(FluidField *, double) except +
        deque[Particle*] particles
        
        void spawnParticles(int,
                            double, double, double, double*,
                            double, double, double, double*,
                            char)
        
        void iterate()