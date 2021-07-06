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
            int type;
            int age;

            Particle(double c[2], double v[2], double s, int t, int a);
            ~Particle();

            void changeType(int t);
    };

    class ParticleSystem
    {
        public:
            std::deque<Particle*> particles;

            ParticleSystem(fluids::FluidField *FF, double d, int lt);
            ~ParticleSystem();

            void spawnParticles(int N, int t,
                                double angle, double speed, double size, double position[2],
                                double angleSpread, double speedSpread, double sizeSpread,
                                double positionSpread[2], char distribution);
            void iterate();

        private:
            fluids::FluidField *fluid;
            double drag_coef;
            int lifetime;
            std::default_random_engine randomGenerator;

            void enforceBoundaries(Particle &p);
            void updateVelocity(Particle &p);
            void updatePosition(Particle &p);
            void removeDeadParticles(int n);
    };
}

#endif