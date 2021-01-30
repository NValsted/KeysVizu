#include <bits/stdc++.h>
#include "particle_system.h"

using namespace std;
using namespace particles;

Particle::Particle(double c[2], double v[2], double s, int a = 0)
{
    for (int i = 0; i < 2; i++)
    {
        coords[i] = c[i];
        velocity[i] = v[i];
    }

    size = s;
    age = a;
};

Particle::~Particle()
{
    //delete [] coords;
    //delete [] velocity;
};

ParticleSystem::ParticleSystem(fluids::FluidField *FF, double d = 0.5)
{
    fluid = FF;
    drag_coef = d;
    randomGenerator.seed(time(nullptr));
};

ParticleSystem::~ParticleSystem()
{
};

void ParticleSystem::spawnParticles(int N,
                                    double angle, double speed, double size, double position[2],
                                    double angleSpread, double speedSpread, double sizeSpread,
                                    double positionSpread[2], char distribution = 'u') // want to add support for other types of distributions
{
    uniform_real_distribution<double> aDistribution(-angleSpread,angleSpread);
    uniform_real_distribution<double> spDistribution(-speedSpread,speedSpread);
    uniform_real_distribution<double> siDistribution(-sizeSpread,sizeSpread);
    uniform_real_distribution<double> xpDistribution(-positionSpread[0],positionSpread[0]);
    uniform_real_distribution<double> ypDistribution(-positionSpread[1],positionSpread[1]);

    double randomizedAngle, randomizedSpeed, randomizedSize, randomizedCoords[2];

    for (int i = 0; i < N; i++)
    {
        
        randomizedAngle = angle + aDistribution(randomGenerator);
        randomizedSpeed = speed + spDistribution(randomGenerator);
        
        randomizedSize  = size  + siDistribution(randomGenerator);
        if (randomizedSize < 0) { randomizedSize = 0; }

        randomizedCoords[0] = position[0] + xpDistribution(randomGenerator);
        randomizedCoords[1] = position[1] + ypDistribution(randomGenerator);

        double randomizedVelocity[2] = {cos(randomizedAngle) * randomizedSpeed,
                                        sin(randomizedAngle) * randomizedSpeed};
        
        Particle *p = new Particle(randomizedCoords,randomizedVelocity,randomizedSize);
        
        particles.push_back(p);
    }
};


void ParticleSystem::enforceBoundaries(Particle &p)
{
    if (p.coords[0] > ((fluid->N) >> 1) ) { p.coords[0] = (fluid->N) >> 1; } // might need ((fluid->N) >> 1) - 1
    if (p.coords[1] > ((fluid->N) >> 1) ) { p.coords[1] = (fluid->N) >> 1; }
    if (p.coords[0] < -((fluid->N) >> 1) ) { p.coords[0] = -(fluid->N) >> 1; }
    if (p.coords[1] < -((fluid->N) >> 1) ) { p.coords[1] = -(fluid->N) >> 1; }
};

void ParticleSystem::updateVelocity(Particle &p)
{
    int i = int(p.coords[0]) + ( (fluid->N) >> 1 );
    int j = int(p.coords[1]) + ( (fluid->N) >> 1 );

    // advection
    p.velocity[0] += fluid->velocity_x[ fluid->IDX(i,j) ];
    p.velocity[1] += fluid->velocity_y[ fluid->IDX(i,j) ];

    // drag
    p.velocity[0] -= (p.velocity[0] * fluid->viscosity * drag_coef);
    p.velocity[1] -= (p.velocity[1] * fluid->viscosity * drag_coef);
};

void ParticleSystem::updatePosition(Particle &p)
{
    p.coords[0] += p.velocity[0];
    p.coords[1] += p.velocity[1];
    enforceBoundaries(p);
};

void ParticleSystem::removeDeadParticles(int n)
{
    while (n--)
    {
        particles.pop_front();
    }
};

void ParticleSystem::iterate()
{
    int deadParticles = 0;

    for (auto particle : particles)
    {
        if ((*particle).age > 42)
        {
            deadParticles++;
            continue;
        }

        updateVelocity(*particle);
        updatePosition(*particle);
        (*particle).age++;
    }

    removeDeadParticles(deadParticles);
};

int main()
{
    fluids::FluidField FF(32,0.1,0.1,0.1);
    ParticleSystem PS(&FF);

    double standardCoords[2] = {0,0};
    double standardPositionSpread[2] = {0,0};
    PS.spawnParticles(3,0,1,1,standardCoords,0.1,0.1,0.1,standardPositionSpread);
    cout << (*PS.particles[0]).coords[0] << endl;

    int iterations = 3;
    while (iterations--)
    {
        PS.iterate();
        cout << (*PS.particles[0]).coords[0] << endl;    
    }
    
    return 0;
}