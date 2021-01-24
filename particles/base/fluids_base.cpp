// Implementation is based on Stam, J. (2003, March). Real-time fluid dynamics for games. In Proceedings of the game developer conference (Vol. 18, p. 25).

#include <bits/stdc++.h>
#include "fluids_base.h"

using namespace std;
using namespace fluid;

#define SWAP(arr_aux,arr) {double *tmp=arr_aux; arr_aux=arr; arr=tmp;}

FluidField::FluidField(int a, double b, double c, double d, double *densityArray)
{
    N = a;
    diffusivity = b;
    viscosity = c;
    dt = d;

    density = densityArray;
    density_aux = new double[N*N];

    velocity_x = new double[N*N];
    velocity_y = new double[N*N];

    velocity_x_aux = new double[N*N];
    velocity_y_aux = new double[N*N];
};

FluidField::~FluidField()
{
    delete [] density;
    delete [] density_aux;
    delete [] velocity_x;
    delete [] velocity_y;
    delete [] velocity_x_aux;
    delete [] velocity_y_aux;
};

int FluidField::IDX(int i, int j)
{
    return i + N * j;
};

double FluidField::getDensity(int i, int j)
{
    return density[IDX(i,j)];
};

double FluidField::getVelocityX(int i, int j)
{
    return velocity_x[IDX(i,j)];
};

double FluidField::getVelocityY(int i, int j)
{
    return velocity_y[IDX(i,j)];
};

void FluidField::passArray(double *someArray)
{
    
    for (int i = 0; i<5; i++)
    {
        someArray[i]++;
    }
};

void FluidField::addDensity(int x, int y, double amount)
{
    density[IDX(x,y)] += amount;
};

void FluidField::addVelocity(int x, int y, double amountX, double amountY)
{
    velocity_x[IDX(x,y)] += amountX;
    velocity_y[IDX(x,y)] += amountY;
};

void FluidField::iterate()
{
    // Update velocity vector field
    
    SWAP(velocity_x, velocity_x_aux); SWAP(velocity_y, velocity_y_aux);
    
    diffuse(1, velocity_x, velocity_x_aux, viscosity);
    diffuse(2, velocity_y, velocity_y_aux, viscosity);

    project();

    SWAP(velocity_x, velocity_x_aux); SWAP(velocity_y, velocity_y_aux);

    advect(1,velocity_x, velocity_x_aux);
    advect(2,velocity_y, velocity_y_aux);

    project();
    
    // Update density field
    SWAP(density, density_aux);

    diffuse(0, density, density_aux, diffusivity);

    SWAP(density, density_aux);

    advect(0, density, density_aux);
};

void FluidField::updateBounds(int b, double *arr)
{
    for (int i = 1; i < N-1; i++)
    {
        if (b == 1)
        {
            arr[IDX(0,i)]   = -arr[IDX(1,i)];
            arr[IDX(N-1,i)] = -arr[IDX(N-2,i)];
        }
        else
        {
            arr[IDX(0,i)]   = arr[IDX(1,i)];
            arr[IDX(N-1,i)] = arr[IDX(N-2,i)];
        }
            
        if (b == 2)
        {
            arr[IDX(i,0)]   = -arr[IDX(i,1)];
            arr[IDX(i,N-1)] = -arr[IDX(i,N-2)];
        }
        else
        {
            arr[IDX(i,0)]   = arr[IDX(i,1)];
            arr[IDX(i,N-1)] = arr[IDX(i,N-2)];
        }
        
    }

    arr[IDX(0,0)]     = 0.5 * ( arr[IDX(1,0)] + arr[IDX(0,1)] );
    arr[IDX(0,N-1)]   = 0.5 * ( arr[IDX(1,N-1)] + arr[IDX(0,N-2)] );
    arr[IDX(N-1,0)]   = 0.5 * ( arr[IDX(N-1,0)] + arr[IDX(N-1,1)] );
    arr[IDX(N-1,N-1)] = 0.5 * ( arr[IDX(N-2,N-1)] + arr[IDX(N-1,N-2)] );
};

void FluidField::GaussSeidel(int b, double *arr, double *arr_aux, double a, int iterations = 5)
{
    double recip_denom = 1.0 / (1.0 + 4.0*a);
    while (iterations)
    {
        for (int j = 1; j < N-1; j++)
        {
            for (int i = 1; i < N-1; i++)
            {
                arr[IDX(i,j)] = ( arr_aux[IDX(i,j)] + a * ( arr[IDX(i-1,j)] + arr[IDX(i+1,j)]
                                                           +arr[IDX(i,j-1)] + arr[IDX(i,j+1)] ) ) * recip_denom;
            }
        }

        updateBounds(b,arr);
        iterations--;
    }
};

void FluidField::project()
{
    double cell_length = 1.0 / N;

    for (int j = 1; j < N-1; j++)
    {
        for (int i = 1; i < N-1; i++)
        {
            velocity_y_aux[IDX(i,j)] = -0.5 * ( velocity_x[IDX(i+1,j)] - velocity_x[IDX(i-1,j)]
                                                +velocity_y[IDX(i,j+1)] - velocity_y[IDX(i,j-1)]) * cell_length;
            velocity_x_aux[IDX(i,j)] = 0;
        }
    }

    updateBounds(0, velocity_y_aux);
    updateBounds(0, velocity_x_aux);
    GaussSeidel(0, velocity_x_aux, velocity_y_aux, 1);

    for (int j = 1; j < N-1; j++)
    {
        for (int i = 1; i < N-1; i++)
        {
            velocity_x[IDX(i,j)] -= 0.5 * ( velocity_x_aux[IDX(i+1,j)] - velocity_x_aux[IDX(i-1,j)] ) * N;
            velocity_y[IDX(i,j)] -= 0.5 * ( velocity_y_aux[IDX(i,j+1)] - velocity_y_aux[IDX(i,j-1)] ) * N;
        }
    }

    updateBounds(1, velocity_x);
    updateBounds(2, velocity_y);
};

void FluidField::diffuse(int b, double *arr, double *arr_aux, double resistance)
{
    double a = dt * resistance * (N-2) * (N-2);
    GaussSeidel(b, arr, arr_aux, a);
};

void FluidField::advect(int b, double *arr, double *arr_aux)
{
    double x, y;
    int i_left, i_right, j_top, j_bottom;
    double s0, s1, t0, t1;

    double dt_scaled = dt * (N-2);

    for (int j = 1; j < N-1; j++)
    {
        for (int i = 1; i < N-1; i++)
        {
            x = i - dt_scaled * velocity_x[IDX(i,j)];
            y = j - dt_scaled * velocity_y[IDX(i,j)];

            if (x < 0.5) { x = 0.5; }
            if (x > N - 2 + 0.5) { x = N - 2 + 0.5; }
            
            if (y < 0.5) { y = 0.5; }
            if (y > N - 2 + 0.5) { y = N - 2 + 0.5; }

            i_left = int(x);
            i_right = i_left + 1;
            j_top = int(y);
            j_bottom = j_top + 1;

            s1 = x - double(i_left);
            s0 = 1 - s1;
            t1 = y - double(j_top);
            t0 = 1 - t1;

            arr[IDX(i,j)] = s0 * (t0 * arr_aux[IDX(i_left,j_top)] + t1 * arr_aux[IDX(i_left,j_bottom)])
                          + s1 * (t0 * arr_aux[IDX(i_right,j_top)] + t1 * arr_aux[IDX(i_right,j_bottom)]);
        }
    }
    updateBounds(b,arr);
};

int main()
{
    /*
    FluidField FF(32,0.2,0.1,0.001);
    
    for (int u = 0; u < 10; u++)
    {
        FF.addVelocity(15,15,0.5,0.5);    
        FF.iterate();

        cout << u << " " << FF.velocity_x[FF.IDX(15,15)] << '\n';
    }
    */
    return 0;
}