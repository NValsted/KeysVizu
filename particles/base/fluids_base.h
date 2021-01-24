#ifndef FLUIDF
#define FLUIDF

namespace fluid {
    class FluidField
    {
        public:
            int N;
            double diffusivity, viscosity, dt;
            
            double *density, *density_aux;
            
            double *velocity_x, *velocity_y;
            double *velocity_x_aux, *velocity_y_aux;

            FluidField(int a, double b, double c, double d, double *densityArray);
            ~FluidField();

            int IDX(int i, int j);
            double getDensity(int i, int j);
            double getVelocityX(int i, int j);
            double getVelocityY(int i, int j);
            void passArray(double *someArray);

            void addDensity(int x, int y, double amount);
            void addVelocity(int x, int y, double amountX, double amountY);
            
            void iterate();

        private:

            void updateBounds(int b, double *arr);
            void GaussSeidel(int b, double *arr, double *arr_aux, double a, int iterations);

            void project();
            void diffuse(int b, double *arr, double *arr_aux, double resistance);
            void advect(int b, double *arr, double *arr_aux);

    };
}

#endif