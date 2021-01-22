# distutils: language = c++

from fluids_base cimport FluidField

cdef class pyFluidField:
    cdef FluidField *c_FF

    def __cinit__(self,int a, double b, double c, double d):
        self.c_FF = new FluidField(a,b,c,d)

    def __dealloc__(self):
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