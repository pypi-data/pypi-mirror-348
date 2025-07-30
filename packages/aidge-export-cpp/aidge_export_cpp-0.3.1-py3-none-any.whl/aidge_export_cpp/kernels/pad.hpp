#ifndef __AIDGE_EXPORT_CPP_KERNELS_PAD2D__
#define __AIDGE_EXPORT_CPP_KERNELS_PAD2D__

#include "network/typedefs.hpp"
#include "network/utils.hpp"

// Todo add border value and border type (Reflect, Constant, Wrap...) and add the two missing pad value (bottom and right)

template<int NB_BATCHES, int NB_CHANNELS,
         int CHANNELS_HEIGHT, int CHANNELS_WIDTH,
         int NB_OUTPUTS,
         int OUTPUTS_HEIGHT, int OUTPUTS_WIDTH,
         int PADDING_TOP,
         int PADDING_LEFT,
         int PADDING_BOTTOM,
         int PADDING_RIGHT,
         typename Input_T, typename Output_T>
__attribute__((always_inline)) inline
void pad_forward(
    double borderValue,
    const Input_T* __restrict inputs,
    Output_T* __restrict outputs
    )
{
    const unsigned int oySize = CHANNELS_HEIGHT + PADDING_TOP + PADDING_BOTTOM;
    const unsigned int oxSize = CHANNELS_WIDTH + PADDING_LEFT + PADDING_RIGHT;

    for (unsigned int batch = 0; batch < NB_BATCHES; ++batch) {
        for (unsigned int ch = 0; ch < NB_CHANNELS; ++ch) {
            const unsigned int preIndex = batch * NB_CHANNELS * CHANNELS_HEIGHT * CHANNELS_WIDTH + ch * CHANNELS_HEIGHT * CHANNELS_WIDTH;

            for (unsigned int oy = 0; oy < oySize; ++oy) {
                for (unsigned int ox = 0; ox < oxSize; ++ox) {
                    const unsigned int outIndex = batch * NB_CHANNELS * oySize * oxSize + ch * oySize * oxSize + oy * oxSize + ox;

                    outputs[outIndex] = borderValue;

                    const unsigned int inputX = ox - PADDING_LEFT;
                    const unsigned int inputY = oy - PADDING_TOP;

                    if (inputY >= 0 and inputY < CHANNELS_HEIGHT and inputX >= 0 and inputX < CHANNELS_WIDTH)
                    {
                        outputs[outIndex] = inputs[preIndex + inputY * CHANNELS_WIDTH + inputX];
                    }
                }
            }
        }
    }
}

#endif  // __AIDGE_EXPORT_CPP_KERNELS_PAD2D__
