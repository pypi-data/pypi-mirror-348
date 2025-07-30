/********************************************************************************
 * Copyright (c) 2023 CEA-List
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 *
 * SPDX-License-Identifier: EPL-2.0
 *
 ********************************************************************************/

#ifndef __AIDGE_EXPORT_CPP_KERNELS_TRANSPOSE__
#define __AIDGE_EXPORT_CPP_KERNELS_TRANSPOSE__

/**
 * @brief Transposes an N-dimensional tensor based on the specified permutation.
 *
 * This function rearranges the dimensions of an N-dimensional tensor according to the
 * permutation array provided. The input tensor is expected to have dimensions specified
 * by `in_dims`, and the output tensor will have dimensions reordered as specified by the
 * `permute` array.
 *
 * Based on Tensor::copyTranspose from aidge.aidge_core
 *
 * @tparam T        Data type of the tensor elements.
 * @tparam NB_DIMS  Number of dimensions of the input tensor.
 * @param[in]  inputs      Pointer to the input tensor data stored in contiguous memory.
 * @param[in]  in_dims     Array containing the size of each dimension of the input tensor.
 * @param[in]  permute     Array of unsigned integers specifying the desired permutation
 *                         of dimensions. Each value should be in the range [0, NB_DIMS-1],
 *                         defining the new order of dimensions for the output tensor.
 * @param[in]  total_size  Total number of elements in the input/output tensor.
 * @param[out] outputs     Pointer to the pre-allocated memory for the transposed tensor.
 *                         Ensure this memory is appropriately sized to hold the transposed data.
 */
template <typename T,unsigned int NB_DIMS>
void transpose_ND_forward(const T *__restrict inputs,
                          const unsigned int *in_dims,
                          const unsigned int *permute,
                          const unsigned int total_size,
                          T *__restrict outputs)
{
    // Compute strides for input tensor
    unsigned int in_strides[NB_DIMS];
    in_strides[NB_DIMS - 1] = 1;
    for (int i = NB_DIMS - 2; i >= 0; --i)
    {
        in_strides[i] = in_strides[i + 1] * in_dims[i + 1];
    }

    // Compute dimensions and strides for output tensor
    unsigned int out_dims[NB_DIMS];
    unsigned int out_strides[NB_DIMS];
    out_strides[NB_DIMS - 1] = 1;
    for (unsigned int i = 0; i < NB_DIMS; ++i)
    {
        out_dims[i] = in_dims[permute[i]];
    }
    for (int i = NB_DIMS - 2; i >= 0; --i)
    {
        out_strides[i] = out_strides[i + 1] * out_dims[i + 1];
    }

    unsigned int current_idx[NB_DIMS];

    // Iterate over all elements in the input tensor
    for (unsigned int idx = 0; idx < total_size; ++idx)
    {

        unsigned int remaining = idx;
        for (unsigned int i = 0; i < NB_DIMS; ++i)
        {
            current_idx[i] = remaining / in_strides[i];
            remaining = remaining % in_strides[i];
        }

        unsigned int output_index = 0;
        for (unsigned int i = 0; i < NB_DIMS; ++i)
        {
            output_index += current_idx[permute[i]] * out_strides[i];
        }

        outputs[output_index] = inputs[idx];
    }
}

#endif // __AIDGE_EXPORT_CPP_KERNELS_TRANSPOSE__
