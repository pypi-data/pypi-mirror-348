#ifndef __AIDGE_EXPORT_CPP_KERNELS_SOFTMAX__
#define __AIDGE_EXPORT_CPP_KERNELS_SOFTMAX__

#include "network/typedefs.hpp"
#include "network/utils.hpp"

#include <type_traits>
#include <cmath>
#include <algorithm>

template<int AXIS_SIZE,
         int AXIS_SIZE_POST,
         int AXIS_SIZE_PRE,
         typename Input_T, typename Output_T>
__attribute__((always_inline)) inline
void softmax_forward (
    const Input_T* __restrict inputs,
    Output_T* __restrict outputs)
{
    // Iterate over the "pre-axis" and "post-axis" slices.
    // For each slice along the axis, compute the maximum value,
    // the sum of exponentials, and then write the normalized softmax outputs.
    for (int i = 0; i < AXIS_SIZE_PRE; ++i) {
        for (int j = 0; j < AXIS_SIZE_POST; ++j) {
            // Compute the base index for this slice.
            const int baseIdx = i * AXIS_SIZE * AXIS_SIZE_POST + j;

            // Find the maximum value along the axis.
            Input_T maxVal = inputs[baseIdx];
            for (int k = 1; k < AXIS_SIZE; ++k) {
                const int idx = baseIdx + k * AXIS_SIZE_POST;
                maxVal = std::max(maxVal, inputs[idx]);
            }

            // Compute the sum of the exponentials along the axis.
            Input_T sumExp = 0;
            for (int k = 0; k < AXIS_SIZE; ++k) {
                const int idx = baseIdx + k * AXIS_SIZE_POST;
                outputs[idx] = std::exp(inputs[idx] - maxVal);
                sumExp += outputs[idx];
            }

            // Write the softmax values to the output.
            for (int k = 0; k < AXIS_SIZE; ++k) {
                const int idx = baseIdx + k * AXIS_SIZE_POST;
                outputs[idx] /= sumExp;
            }
        }
    }
}

#endif  // __AIDGE_EXPORT_CPP_KERNELS_SOFTMAX__
