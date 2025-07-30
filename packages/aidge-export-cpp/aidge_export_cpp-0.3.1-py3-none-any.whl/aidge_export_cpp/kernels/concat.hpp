#ifndef __AIDGE_EXPORT_CPP_KERNELS_CONCAT__
#define __AIDGE_EXPORT_CPP_KERNELS_CONCAT__

template<int AXIS_SIZE_POST,
         int AXIS_SIZE_PRE,
         unsigned int NB_INPUTS,
         typename T>
__attribute__((always_inline)) inline static
void concat_forward (
    const T* const * __restrict inputs,
    const unsigned int* __restrict sizes,
    T* __restrict output)
{
    unsigned int total_concat_axis_size = 0;
    for (unsigned int n = 0; n < NB_INPUTS; ++n)
        total_concat_axis_size += sizes[n];

    for (int i = 0; i < AXIS_SIZE_PRE; ++i) {
        // Loop over post-axis (e.g., dims after axis 1)
        for (int j = 0; j < AXIS_SIZE_POST; ++j) {
            unsigned int axis_offset = 0;

            // Loop over each input tensor
            for (unsigned int n = 0; n < NB_INPUTS; ++n) {
                for (unsigned int k = 0; k < sizes[n]; ++k) {
                    const int input_idx  = i * sizes[n] * AXIS_SIZE_POST + k * AXIS_SIZE_POST + j;

                    output[i * total_concat_axis_size * AXIS_SIZE_POST + (axis_offset + k) * AXIS_SIZE_POST + j] =
                        inputs[n][input_idx];
                }

                axis_offset += sizes[n];  // move along axis in output
            }
        }
    }

}

#endif  // __AIDGE_EXPORT_CPP_KERNELS_CONCAT__