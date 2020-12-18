# Implementation is based on Stam, J. (2003, March). Real-time fluid dynamics for games. In Proceedings of the game developer conference (Vol. 18, p. 25).
# Memory and int-float conversion optimizations made based on section 5 of Possible optimizations to current technique in section 5 of Ash, M. (2005). Simulation and visualization of a 3d fluid. Master's thesis, Université d'Orléans France
# These optimizations may not be directly transferable to Python. Need to check this.

# Smoothed-particle hydrodynamics might be a viable improvement. Will have to look into it.

class Fluid:
    N = None

    diffusivity = None
    viscosity = None
    dt = None

    density = []
    density_prev = [] # The naming of *_prev arrays is not completely indicative of their use. They are sometimes used as scratch arrays. 
    
    velocity_x,velocity_y = [[]]*2
    velocity_x_prev,velocity_y_prev = [[]]*2

    def __init__(self,N,diffusivity,viscosity,dt):
        self.N = N # This implementation does not follow size convention from [Stam 2003]
        self.diffusivity = diffusivity
        self.viscosity = viscosity
        self.dt = dt

        self.density = [[0 for i in range(N)] for j in range(N)]
        self.density_prev = [[0 for i in range(N)] for j in range(N)]

        self.velocity_x = [[0 for i in range(N)] for j in range(N)]
        self.velocity_y = [[0 for i in range(N)] for j in range(N)]
        
        self.velocity_x_prev = [[0 for i in range(N)] for j in range(N)]
        self.velocity_y_prev = [[0 for i in range(N)] for j in range(N)]
    
    def __swap(self,arr,arr_prev): # Doesn't swap class attributes
        arr, arr_prev = arr_prev, arr

    def __update_bounds(self, b, arr):
        
        for i in range(1,self.N-1):    
            
            if b == 1:
                arr[0][i] = -arr[1][i]
                arr[self.N-1][i] = -arr[self.N-2][i]
            else:
                arr[0][i] = arr[1][i]
                arr[self.N-1][i] = arr[self.N-2][i]

            if b == 2:
                arr[i][0] = -arr[i][1]
                arr[i][self.N-1] = -arr[i][self.N-2]
            else:
                arr[i][0] = arr[i][1]
                arr[i][self.N-1] = arr[i][self.N-2]

        arr[0][0] = 0.5 * ( arr[1][0] + arr[0][1] )
        arr[0][self.N-1] = 0.5 * ( arr[1][self.N-1] + arr[0][self.N-2] )
        arr[self.N-1][0] = 0.5 * ( arr[self.N-1][0] + arr[self.N-1][1] )
        arr[self.N-1][self.N-1] = 0.5 * ( arr[self.N-2][self.N-1] + arr[self.N-1][self.N-2] )

    def __Gauss_Seidel(self, b, arr, arr_prev, a, iterations=5):
        recip_denom = 1 / (1 + 4*a)

        while iterations:
            for j in range(1, self.N-1):
                for i in range(1, self.N-1):
                    arr[i][j] = ( arr_prev[i][j] + a * ( arr[i-1][j] + arr[i+1][j]
                                                        +arr[i][j-1] + arr[i][j+1] ) ) * recip_denom
            self.__update_bounds(b,arr)
            iterations -= 1

    def __project(self): # Hodge decomposition black magic
        cell_length = 1/self.N

        for j in range(1, self.N-1):
            for i in range(1, self.N-1):
                self.velocity_y_prev[i][j] = -0.5* ( self.velocity_x[i+1][j] - self.velocity_x[i-1][j]
                                                    +self.velocity_y[i][j+1] - self.velocity_y[i][j-1]) * cell_length
                self.velocity_x_prev[i][j] = 0

        self.__update_bounds(0, self.velocity_y_prev)
        self.__update_bounds(0, self.velocity_x_prev)
        self.__Gauss_Seidel(0, self.velocity_x_prev, self.velocity_y_prev, 1)

        for j in range(1, self.N-1):
            for i in range(1, self.N-1):
                self.velocity_x[i][j] -= 0.5 * ( self.velocity_x_prev[i+1][j] - self.velocity_x_prev[i-1][j] ) * self.N
                self.velocity_y[i][j] -= 0.5 * ( self.velocity_y_prev[i][j+1] - self.velocity_y_prev[i][j-1] ) * self.N

        self.__update_bounds(1, self.velocity_x)
        self.__update_bounds(2, self.velocity_y)

    def __diffuse(self, b, arr, arr_prev, resistance):
        a = self.dt * resistance * ((self.N-2) ** 2) # This might be able to be pre-computed in __init__
        self.__Gauss_Seidel(b, arr, arr_prev, a)

    def __advect(self, b, arr, arr_prev):
        dt_scaled = self.dt * (self.N - 2)

        for j in range(1, self.N-1):
            for i in range(1, self.N-1):
                x = i - dt_scaled * self.velocity_x[i][j]
                y = j - dt_scaled * self.velocity_y[i][j]
                
                if (x < 0.5):
                    x = 0.5
                #x = max(0.5,x)
                
                if (x > self.N-2 + 0.5):
                    x = self.N-2 + 0.5
                #x = min(self.N+0.5,x)

                if (y < 0.5):
                    y = 0.5
                #y = max(0.5,y)
                
                if (y > self.N-2 + 0.5):
                    y = self.N-2 + 0.5
                #y = min(self.N+0.5,y)

                i_left = int(x)
                i_right = i_left + 1
                j_top = int(y)
                j_bottom = j_top + 1

                s1 = x - i_left
                s0 = 1 - s1
                t1 = y - j_top
                t0 = 1 - t1

                arr[i][j] = s0 * (t0 * arr_prev[i_left][j_top] + t1 * arr_prev[i_left][j_bottom])\
                          + s1 * (t0 * arr_prev[i_right][j_top] + t1 * arr_prev[i_right][j_bottom])

        self.__update_bounds(b, arr)

    def add_density(self, x, y, amount):
        self.density[x][y] += amount
    
    def add_velocity(self, x, y, amount_x, amount_y):
        self.velocity_x[x][y] += amount_x
        self.velocity_y[x][y] += amount_y

    def iterate(self):
        
        # Update velocity vector field
        self.velocity_x, self.velocity_x_prev = self.velocity_x_prev, self.velocity_x #self.__swap(self.velocity_x, self.velocity_x_prev)
        self.velocity_y, self.velocity_y_prev = self.velocity_y_prev, self.velocity_y #self.__swap(self.velocity_y, self.velocity_y_prev)

        self.__diffuse(1, self.velocity_x, self.velocity_x_prev, self.viscosity)
        self.__diffuse(2, self.velocity_y, self.velocity_y_prev, self.viscosity)

        self.__project()

        self.velocity_x, self.velocity_x_prev = self.velocity_x_prev, self.velocity_x #self.__swap(self.velocity_x, self.velocity_x_prev)
        self.velocity_y, self.velocity_y_prev = self.velocity_y_prev, self.velocity_y #self.__swap(self.velocity_y, self.velocity_y_prev)

        self.__advect(1, self.velocity_x, self.velocity_x_prev)
        self.__advect(1, self.velocity_y, self.velocity_y_prev)

        self.__project()
        
        # Update density field
        
        self.density, self.density_prev = self.density_prev, self.density #self.__swap(self.density, self.density_prev)
        
        self.__diffuse(0, self.density, self.density_prev, self.diffusivity)
        
        self.density, self.density_prev = self.density_prev, self.density #self.__swap(self.density, self.density_prev)

        self.__advect(0, self.density, self.density_prev )

def main():
    FluidField = Fluid(5, 0.1, 0.1, 0.001)
    
    for _ in range(5):
        FluidField.add_velocity(2,2,1,1)
        FluidField.iterate()

        print(FluidField.velocity_x)

if __name__ == '__main__':
    main()