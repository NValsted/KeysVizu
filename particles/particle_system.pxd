from libcpp.deque cimport deque
from base.fluids_base cimport FluidField

cdef extern from "particle_system.cpp":
    pass

cdef extern from "particle_system.h" namespace "particles":
    cdef cppclass Particle:
        Particle(double *, double *, double, int, int)
        double *coords
        int age
        int type
        double size

        void changeType(int)

    cdef cppclass ParticleSystem:
        ParticleSystem(FluidField *, double, int) except +
        deque[Particle*] particles
        
        void spawnParticles(int, int,
                            double, double, double, double*,
                            double, double, double, double*,
                            char)
        
        void iterate()
