/*
    This code has been developed by Juan Sandubete Lopez and all the rights
    belongs to him.
    Distribution or commercial use of the code is not allowed without previous
    agreement with the author.
*/

#include "tuto_p3_controller.h"


extern "C" double nonlinear_control(double tau, double tau_ref, double taup_ref){
  double u_val = 0;

  double v = taup_ref - K_C1*(tau-tau_ref);
  u_val = a_MODEL*tau + v/k_MODEL;

  return u_val;
}
