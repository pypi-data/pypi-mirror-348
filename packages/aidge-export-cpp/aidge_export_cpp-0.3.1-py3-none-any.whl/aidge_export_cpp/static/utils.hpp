#ifndef __AIDGE_EXPORT_CPP_NETWORK_UTILS__
#define __AIDGE_EXPORT_CPP_NETWORK_UTILS__

#if SAVE_OUTPUTS
#include <sys/types.h>
#include <sys/stat.h>
#include <cstdio>      // fprintf
#include <type_traits> // std::is_floating_point
#endif

#if AIDGE_CMP
#include <string>
#endif

/**
 * @brief   Integer clamping
 * @param[in]  v   Value to be clamped
 * @param[in]  lo  Saturating lower bound
 * @param[in]  hi  Saturating higher bound
 * @returns         Value clamped between lo and hi
 *
 */
__attribute__((always_inline)) static inline
int clamp (int v, int lo, int hi)
{
    if(v < lo) {
        return lo;
    }
    else if(v > hi) {
        return hi;
    }
    else {
        return v;
    }
}

/**
 * @brief   Maximum of two integer values
 */
__attribute__((always_inline)) static inline
int max (int lhs, int rhs)
{
    return (lhs >= rhs) ? lhs : rhs;
}

/**
 * @brief   Minimum of two integer values
 */
__attribute__((always_inline)) static inline
int min (int lhs, int rhs)
{
    return (lhs <= rhs) ? lhs : rhs;
}


#if SAVE_OUTPUTS
enum class Format {
    Default,
    NCHW,
    NHWC,
    CHWN,
    NCDHW,
    NDHWC,
    CDHWN
};


template<typename Output_T>
inline void saveOutputs(
    int NB_OUTPUTS,
    int OUTPUTS_HEIGHT, int OUTPUTS_WIDTH,
    // int OUTPUT_MEM_CONT_OFFSET,
    // int OUTPUT_MEM_CONT_SIZE,
    // int OUTPUT_MEM_WRAP_OFFSET,
    // int OUTPUT_MEM_WRAP_SIZE,
    // int OUTPUT_MEM_STRIDE,
    const Output_T* __restrict outputs,
    FILE* pFile,
    Format format)
{
    // default is NHCW !
    if (format == Format::NHWC) {
        fprintf(pFile, "(");
        auto oOffset = 0;
        for(int oy = 0; oy < OUTPUTS_HEIGHT; oy++) {
            fprintf(pFile, "(");

            for(int ox = 0; ox < OUTPUTS_WIDTH; ox++) {
                fprintf(pFile, "(");

                // const int oPos = (ox + OUTPUTS_WIDTH * oy);
                // int oOffset = OUTPUT_MEM_STRIDE * oPos;

                // if (OUTPUT_MEM_WRAP_SIZE > 0
                //     && oOffset >= OUTPUT_MEM_CONT_SIZE)
                // {
                //     oOffset += OUTPUT_MEM_WRAP_OFFSET - OUTPUT_MEM_CONT_OFFSET
                //                 - OUTPUT_MEM_CONT_SIZE;
                // }

                for (int output = 0; output < NB_OUTPUTS; output++) {
                    if (std::is_floating_point<Output_T>::value)
                        fprintf(pFile, "%f", static_cast<float>(outputs[oOffset]));
                    else
                        fprintf(pFile, "%d", static_cast<int>(outputs[oOffset]));
                    oOffset += 1;

                    fprintf(pFile, ", ");
                }

                fprintf(pFile, "), \n");
            }

            fprintf(pFile, "), \n");
        }

        fprintf(pFile, ")\n");
    }
    else if (format == Format::NCHW || format == Format::Default) {
        auto ofst = 0;
        for(int output = 0; output < NB_OUTPUTS; output++) {
            fprintf(pFile, "%d:\n", output);
            for(int oy = 0; oy < OUTPUTS_HEIGHT; oy++) {
                for(int ox = 0; ox < OUTPUTS_WIDTH; ox++) {
                    fprintf(pFile, "%d",  static_cast<int>(outputs[ofst]));
                    fprintf(pFile, " ");
                    ofst += 1;
                }

                fprintf(pFile, "\n");
            }

            fprintf(pFile, "\n");
        }

        fprintf(pFile, "\n");
    }
    else {
        printf("Warning unsupported dataformat.\n");
    }
}
#endif // SAVE_OUTPUTS

#if AIDGE_CMP

template<int NB_OUTPUTS, int OUT_WIDTH, int OUT_HEIGHT, typename AidgeOutput_T, typename DevOutput_T>
void aidge_cmp(std::string layer_name, AidgeOutput_T* aidge_output, DevOutput_T* dev_output) {

    printf("[AIDGE COMPARE] - %s\n", layer_name.c_str());

    for (auto out = 0; out < NB_OUTPUTS; ++out) {
        for (auto h = 0; h < OUT_HEIGHT; ++h) {
            for (auto w = 0; w < OUT_WIDTH; ++w) {
                const int aidge_ofst = out * OUT_HEIGHT * OUT_WIDTH + h * OUT_WIDTH + w;
                const int dev_ofst = h * OUT_WIDTH * NB_OUTPUTS + w * NB_OUTPUTS + out;
                if (aidge_output[aidge_ofst] != dev_output[dev_ofst]) {
                    if (std::is_floating_point<DevOutput_T>::value) {
                        printf("[ERROR] - First error detected at %dx%dx%d (out x h x w) : aidge_out = %f vs dev_out = %f\n",
                                out, h, w, static_cast<double>(aidge_output[aidge_ofst]), static_cast<double>(dev_output[dev_ofst]));
                    } else {
                        printf("[ERROR] - First error detected at %dx%dx%d (out x h x w) : aidge_out = %d vs dev_out = %d\n",
                              out, h, w, static_cast<int>(aidge_output[aidge_ofst]), static_cast<int>(dev_output[dev_ofst]));
                    }
                    printf("Abort program.\n");
                    exit(1);
                }
            }
        }
    }
    printf("[SUCCESS]\n\n");
}

#endif  // AIDGE_CMP

#endif // __AIDGE_EXPORT_CPP_NETWORK_UTILS__
