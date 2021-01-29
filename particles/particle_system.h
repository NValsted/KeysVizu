#ifndef PARTICLESYS
#define PARTICLESYS

#include "base/fluids_base.h"
#include <random>
#include <deque>

namespace particles {
    
    class Particle
    {
        public:
            double coords[2];
            double velocity[2];
            double size;
            int age;

            Particle(double c[2], double v[2], double s, int a);
            ~Particle();
    };

    class ParticleSystem
    {
        public:
            std::deque<Particle*> particles;

            ParticleSystem(fluids::FluidField *F, double d);
            ~ParticleSystem();

            void spawnParticles(int N,
                                double angle, double speed, double size,
                                double angleSpread, double speedSpread,
                                double sizeSpread, char distribution);
            void iterate();

        private:
            fluids::FluidField *Fluid;
            double drag_coef;
            std::default_random_engine randomGenerator;

            void enforceBoundaries(Particle &p);
            void updateVelocity(Particle &p);
            void updatePosition(Particle &p);
            void removeDeadParticles(int n);
    };
}

#endif