cdef extern from "fluids_base.cpp":
    pass

cdef extern from "fluids_base.h" namespace "fluids":
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