#ifndef __AIDGE_EXPORT_CPP_KERNELS_BATCHNORM__
#define __AIDGE_EXPORT_CPP_KERNELS_BATCHNORM__

#include "network/typedefs.hpp"
#include "network/activation_utils.hpp"

#include <math.h>

// WARNING: this kernel only works for 32-bits floating point values

template<int NB_BATCHES, int NB_OUTPUTS,
         int OUTPUTS_HEIGHT, int OUTPUTS_WIDTH,
         ActivationFunction_T ACTIVATION,
         typename Input_T, typename Output_T,
         typename Param_T,
         typename Rescaling_T>
__attribute__((always_inline)) inline
void batchnorm_forward (
    const Input_T* __restrict inputs,
    Output_T* __restrict outputs,
    const Param_T* __restrict biases,
    const Param_T* __restrict variances,
    const Param_T* __restrict means,
    const Param_T* __restrict scales,
    const double epsilon,
    const Rescaling_T& __restrict rescaling)
{
    for (unsigned int batch = 0; batch < NB_BATCHES; ++batch) {
        for (unsigned int output = 0; output < NB_OUTPUTS; ++output) {
            // If the variance is 0, we need to avoid division by 0
            Output_T var = sqrt(variances[output] > 0.0 ? variances[output] + epsilon : epsilon);

            for (int oy = 0; oy < OUTPUTS_HEIGHT; ++oy) {
                for (int ox = 0; ox < OUTPUTS_WIDTH; ++ox) {
                    const int outputOffset = batch * OUTPUTS_WIDTH * OUTPUTS_HEIGHT * NB_OUTPUTS + output * OUTPUTS_WIDTH * OUTPUTS_HEIGHT + OUTPUTS_WIDTH * oy + ox;

                    const Output_T normalized = (inputs[outputOffset] - means[output]) / var;
                    const Output_T sAs = scales[output] * normalized + biases[output];
                    outputs[outputOffset] = activation_forward_value<Output_T>(sAs, output, ACTIVATION, rescaling);
                }
            }
        }
    }
}


#endif  // __AIDGE_EXPORT_CPP_KERNELS_BATCHNORM__
