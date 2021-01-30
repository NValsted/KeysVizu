#ifndef PARTICLESYS
#define PARTICLESYS

#include <random>
#include <deque>
#include "base/fluids_base.h"

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

            ParticleSystem(fluids::FluidField *FF, double d);
            ~ParticleSystem();

            void spawnParticles(int N,
                                double angle, double speed, double size, double position[2],
                                double angleSpread, double speedSpread, double sizeSpread,
                                double positionSpread[2], char distribution);
            void iterate();

        private:
            fluids::FluidField *fluid;
            double drag_coef;
            std::default_random_engine randomGenerator;

            void enforceBoundaries(Particle &p);
            void updateVelocity(Particle &p);
            void updatePosition(Particle &p);
            void removeDeadParticles(int n);
    };
}

#endif