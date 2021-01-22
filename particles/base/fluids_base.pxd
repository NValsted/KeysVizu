cdef extern from "fluids_base.cpp":
    pass

cdef extern from "fluids_base.h" namespace "fluid":
    cdef cppclass FluidField:
        FluidField(int, double, double, double) except +
        int N
        double diffusivity, viscosity, dt
        double *density, *density_aux
        double *velocity_x, *velocity_y
        double *velocity_x_aux, *velocity_y_aux

        int IDX(int, int)
        double getDensity(int, int)
        double getVelocityX(int, int)
        double getVelocityY(int, int)

        void addDensity(int, int, double)
        void addVelocity(int, int, double, double)
        void iterate()