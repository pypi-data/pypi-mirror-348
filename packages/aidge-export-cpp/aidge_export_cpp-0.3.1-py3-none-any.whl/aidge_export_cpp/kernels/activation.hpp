#ifndef __AIDGE_EXPORT_CPP_KERNELS_ACTIVATION__
#define __AIDGE_EXPORT_CPP_KERNELS_ACTIVATION__

#include "network/activation_utils.hpp"
#include "network/rescaling_utils.hpp"

template<int NB_DATA,
         ActivationFunction_T ACTIVATION,
         typename Input_T, typename Output_T, typename Rescaling_T>
__attribute__((always_inline)) inline
void activation_forward (
    const Input_T* __restrict inputs,
    Output_T* __restrict outputs,
    const Rescaling_T& __restrict rescaling)
{
    for (int i = 0; i < NB_DATA; ++i)
    {
        outputs[i] = activation_forward_value<Output_T>(inputs[i], i, ACTIVATION, rescaling);
    }

}


#endif  // __AIDGE_EXPORT_CPP_KERNELS_ACTIVATION__
