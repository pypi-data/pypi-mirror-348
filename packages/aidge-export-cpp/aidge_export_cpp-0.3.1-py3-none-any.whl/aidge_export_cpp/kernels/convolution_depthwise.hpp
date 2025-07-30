#ifndef __AIDGE_EXPORT_CPP_KERNELS_CONVOLUTION_DEPTHWISE__
#define __AIDGE_EXPORT_CPP_KERNELS_CONVOLUTION_DEPTHWISE__

#include "network/typedefs.hpp"
#include "network/rescaling_utils.hpp"
#include "network/utils.hpp"
#include "network/macs.hpp"
#include "network/activation_utils.hpp"

template<int NB_CHANNELS, 
         int CHANNELS_HEIGHT, int CHANNELS_WIDTH,
         int NB_OUTPUTS,
         int OUTPUTS_HEIGHT, int OUTPUTS_WIDTH,
         int PADDING_Y, int PADDING_X,
         int STRIDE_Y, int STRIDE_X,
         int DILATION_Y, int DILATION_X,
         int KERNEL_HEIGHT, int KERNEL_WIDTH,
         ActivationFunction_T ACTIVATION,
         typename Input_T, typename Output_T,
         typename Weight_T, typename Bias_T,
         typename Rescaling_T>
__attribute__((always_inline)) inline
void convolution_depthwise_forward(
    const Input_T* __restrict inputs,
    Output_T* __restrict outputs,
    const Weight_T* __restrict weights,
    const Bias_T* __restrict biases,
    const Rescaling_T& __restrict rescaling)
{
    static_assert(NB_OUTPUTS % NB_CHANNELS == 0,
        "NB_OUTPUTS should be a multiple of NB_CHANNELS.");

    constexpr int DILATED_KERNEL_HEIGHT 
            = KERNEL_HEIGHT + (DILATION_Y - 1) * (KERNEL_HEIGHT - 1);

    constexpr int DILATED_KERNEL_WIDTH 
            = KERNEL_WIDTH + (DILATION_X - 1) * (KERNEL_WIDTH - 1);

    constexpr int OUTPUTS_HEIGHT_NOPAD
        = (CHANNELS_HEIGHT - DILATION_Y * (KERNEL_HEIGHT - 1) - 1 + STRIDE_Y) / STRIDE_Y;
    constexpr int OUTPUTS_WIDTH_NOPAD
        = (CHANNELS_WIDTH - DILATION_X * (KERNEL_WIDTH - 1) - 1 + STRIDE_X) / STRIDE_X;

    for (int oy = 0; oy < OUTPUTS_HEIGHT; ++oy) {
        const int syMin = (PADDING_Y == 0) ? 0
            : max(PADDING_Y - (oy * STRIDE_Y), 0);
        const int syMax = (PADDING_Y == 0
                && OUTPUTS_HEIGHT == OUTPUTS_HEIGHT_NOPAD) ? DILATED_KERNEL_HEIGHT
            : clamp(CHANNELS_HEIGHT + PADDING_Y - (oy * STRIDE_Y), 
                    0, DILATED_KERNEL_HEIGHT);
        const int iy = (oy * STRIDE_Y) - PADDING_Y;

#ifdef _OPENMP
#pragma omp parallel for collapse(2)
#endif
        for (int ox = 0; ox < OUTPUTS_WIDTH; ++ox) {
            for (int output = 0; output < NB_OUTPUTS; ++output) {
                // moved to inner loop for collapsing -->
                const int sxMin = (PADDING_X == 0) ? 0
                    : max(PADDING_X - (ox * STRIDE_X), 0);
                const int sxMax = (PADDING_X == 0
                        && OUTPUTS_WIDTH == OUTPUTS_WIDTH_NOPAD)
                            ? DILATED_KERNEL_WIDTH
                    : clamp(CHANNELS_WIDTH + PADDING_X - (ox * STRIDE_X), 
                            0, DILATED_KERNEL_WIDTH);
                const int ix = (ox * STRIDE_X) - PADDING_X;

                const int oPos = (ox + OUTPUTS_WIDTH * oy);
                const int oOffset = NB_OUTPUTS * oPos;
                // <--

                const int channel = (output * NB_CHANNELS) / NB_OUTPUTS;

                Bias_T weightedSum = biases ? biases[output] : 0;

                for (int sy = 0; sy < KERNEL_HEIGHT; ++sy) {
                    if ((PADDING_Y != 0
                            || OUTPUTS_HEIGHT != OUTPUTS_HEIGHT_NOPAD)
                        && ((sy*DILATION_Y < syMin) || (sy*DILATION_Y >= syMax)))
                    {
                        continue;
                    }

                    const int iPos = ix + CHANNELS_WIDTH * (iy + sy*DILATION_Y);
                    const int iOffset = NB_CHANNELS * iPos;

                    const int wOffset = (output*KERNEL_HEIGHT + sy) 
                                        * KERNEL_WIDTH;

                    if (DILATION_X == 1 && ((PADDING_X == 0
                            && OUTPUTS_WIDTH == OUTPUTS_WIDTH_NOPAD)
                        || sxMax - sxMin == KERNEL_WIDTH))
                    {
                        macsOnRange<KERNEL_WIDTH, NB_CHANNELS>(
                            inputs + iOffset + channel, 
                            weights + wOffset, 
                            weightedSum);
                    }
                    else {
                        for (int sx = 0; sx < KERNEL_WIDTH; ++sx) {
                            if ((PADDING_X != 0
                                    || OUTPUTS_WIDTH != OUTPUTS_WIDTH_NOPAD)
                                && ((sx*DILATION_X < sxMin) || (sx*DILATION_X >= sxMax)))
                            {
                                continue;
                            }

                            const int iOffsetInRange = iOffset
                                + sx * DILATION_X * NB_CHANNELS;

                            weightedSum += inputs[iOffsetInRange + channel]
                                * weights[wOffset + sx];
                        }
                    }
                }

                outputs[oOffset + output] = activation_forward_value<Output_T>(weightedSum, output, ACTIVATION, rescaling);
            }
        }
    }
}

// Template specialization when biases are not given to the convolution
template<int NB_CHANNELS,
         int CHANNELS_HEIGHT, int CHANNELS_WIDTH,
         int NB_OUTPUTS,
         int OUTPUTS_HEIGHT, int OUTPUTS_WIDTH,
         int PADDING_Y, int PADDING_X,
         int STRIDE_Y, int STRIDE_X,
         int DILATION_Y, int DILATION_X,
         int KERNEL_HEIGHT, int KERNEL_WIDTH,
         ActivationFunction_T ACTIVATION,
         typename Input_T, typename Output_T,
         typename Weight_T,
         typename Rescaling_T>
__attribute__((always_inline)) inline
void convolution_depthwise_forward(
    const Input_T* __restrict inputs,
    Output_T* __restrict outputs,
    const Weight_T* __restrict weights,
    std::nullptr_t __restrict,
    const Rescaling_T& __restrict rescaling)
{
    const float* b = nullptr;

    convolution_depthwise_forward<NB_CHANNELS,
                        CHANNELS_HEIGHT,
                        CHANNELS_WIDTH,
                        NB_OUTPUTS,
                        OUTPUTS_HEIGHT,
                        OUTPUTS_WIDTH,
                        PADDING_Y,
                        PADDING_X,
                        STRIDE_Y,
                        STRIDE_X,
                        DILATION_Y,
                        DILATION_X,
                        KERNEL_HEIGHT,
                        KERNEL_WIDTH,
                        ACTIVATION>
                        (inputs, outputs, weights, b, rescaling);
}

#endif  // __AIDGE_EXPORT_CPP_KERNELS_CONVOLUTION_DEPTHWISE__
