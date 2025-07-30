#pragma once

// ---------------------------------------------------
// ----------------- Saturate Utils ------------------
// ---------------------------------------------------

static int64_t toInt64(uint32_t lo, uint32_t hi) {
    return (int64_t) (((uint64_t) hi) << 32ull) | ((uint64_t) lo);
}

static int64_t smlal(int32_t lhs, int32_t rhs, 
                     uint32_t accumLo, uint32_t accumHi) 
{
    return ((int64_t) lhs) * ((int64_t) rhs) + toInt64(accumLo, accumHi);
}

// ---------------------------------------------------
// --------------- Scaling by Shifting ---------------
// ---------------------------------------------------

template<int SHIFT>
struct SingleShiftScaling {

    template<typename Sum_T>
    Sum_T operator()(Sum_T weightedSum, size_t /*output*/) const 
    {
        return (SHIFT != 0) ? ((weightedSum >> (SHIFT - 1)) + 1) >> 1   // Rounding
                            : weightedSum;   
    }

    // // Shift attribute
    // static const int mShift = SHIFT;
    // static const Scaling_T mScalingType = SingleShift;

    // // FP Attribute
    // static const int32_t mScaling = 0;
    // static const int64_t mFractionalBits = 0;

};

// ---------------------------------------------------
// --------------- Fixed Point Scaling ---------------
// ---------------------------------------------------

template<int64_t SHIFT, int32_t COEF>
struct FixedPointScaling {

    template<typename Sum_T>
    Sum_T operator()(Sum_T weightedSum, size_t /*output*/) const 
    {
        return smlal(weightedSum, COEF, HALF_LO, HALF_HI) >> SHIFT; 
    }

    // Attributes
    static const uint32_t HALF_LO = (SHIFT > 0)
        ? (1ull << (SHIFT - 1)) & 0xFFFFFFFF : 0;
    static const uint32_t HALF_HI = (SHIFT > 0)
        ? (1ull << (SHIFT - 1)) >> 32u : 0;
    
    // static const int32_t mScaling = SCALING;
    // static const int64_t mFractionalBits = FRACTIONAL_BITS;
    // static const Scaling_T mScalingType = FixedPoint;
    // static const int mShift = 0;
};

// ---------------------------------------------------
// ------------------- No Scaling --------------------
// ---------------------------------------------------

struct NoScaling {

    template<typename Sum_T>
    Sum_T operator()(Sum_T weightedSum, unsigned int /*output*/) const 
    {
        return weightedSum;
    }

};
