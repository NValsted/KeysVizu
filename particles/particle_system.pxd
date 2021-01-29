from libcpp.deque cimport deque

cdef extern from "base/fluids_base.cpp":
    pass

cdef extern from "base/fluids_base.h":
    cdef cppclass FluidField:
        FluidField(int, double, double, double) except +
        int N
        double diffusivity, viscosity, dt
        double *density
        double *density_aux
        double *velocity_x
        double *velocity_y
        double *velocity_x_aux
        double *velocity_y_aux

        int IDX(int, int)
        double getDensity(int, int)
        double getVelocityX(int, int)
        double getVelocityY(int, int)

        void addDensity(int, int, double)
        void addVelocity(int, int, double, double)
        void iterate()

cdef extern from "particle_system.cpp":
    pass

cdef extern from "particle_system.h" namespace "particles":
    cdef cppclass Particle:
        Particle(double *, double *, double, int)
        double *coords
        double size

    cdef cppclass ParticleSystem:
        ParticleSystem(FluidField *, double) except +
        deque[Particle*] particles
        void spawnParticles(int, double, double, double, double, double, double, char)
        void iterate()