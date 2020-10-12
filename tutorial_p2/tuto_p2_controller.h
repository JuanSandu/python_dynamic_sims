#include <iostream>
#include <cstdlib>

// Model Parameters
double k_MODEL = 1.0;
double a_MODEL = 1.0;
// Controller Parameters
double K_C1 = 50.0;

// Controller Prototype
extern "C" double nonlinear_control( double tau, double tau_ref, double taup_ref );
