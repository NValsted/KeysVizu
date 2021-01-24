# distutils: language = c++

cimport numpy as np
import numpy as np

from fluids_base cimport FluidField

cdef class pyFluidField:
    cdef FluidField *c_FF
    cdef np.ndarray density_array

    def __cinit__(self, int a, double b, double c, double d, **kwargs):
        cdef np.ndarray[np.double_t, ndim=1] density_array
        density_array = np.ascontiguousarray(np.zeros((a*a,)), dtype=np.double)

        self.density_array = density_array

        self.c_FF = new FluidField(a,b,c,d,&density_array[0])

    def __dealloc__(self):
        del self.c_FF

    def get_density_array(self):
        return self.density_array

    def IDX(self, int i, int j):
        return self.c_FF.IDX(i,j)

    def get_density(self, int i, int j):
        return self.c_FF.getDensity(i,j)

    def get_velocity_x(self, int i, int j):
        return self.c_FF.getVelocityX(i,j)

    def get_velocity_y(self, int i, int j):
        return self.c_FF.getVelocityY(i,j)

    def pass_array(self):
        
        cdef np.ndarray[np.double_t, ndim=1] tmp
        tmp = np.ascontiguousarray(np.zeros((5*5,)), dtype=np.double)
        self.c_FF.passArray(&tmp[0])
        print(tmp)

    def add_density(self, int x, int y, double amount):
        self.c_FF.addDensity(x,y,amount)

    def add_velocity(self, int x, int y, double amount_x, double amount_y):
        self.c_FF.addVelocity(x,y,amount_x,amount_y)

    def iterate(self):
        self.c_FF.iterate()