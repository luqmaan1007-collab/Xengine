// xengine/src/math/matrix.h
// Math Matrix Types

#ifndef XENGINE_MATH_MATRIX_H
#define XENGINE_MATH_MATRIX_H

namespace xengine {

struct Mat3 {
    float m[9];
    
    Mat3() {
        for (int i = 0; i < 9; i++) m[i] = 0.0f;
    }
};

struct Mat4 {
    float m[16];
    
    Mat4() {
        for (int i = 0; i < 16; i++) m[i] = 0.0f;
    }
    
    static Mat4 identity() {
        Mat4 result;
        result.m[0] = 1.0f;
        result.m[5] = 1.0f;
        result.m[10] = 1.0f;
        result.m[15] = 1.0f;
        return result;
    }
};

} // namespace xengine

#endif // XENGINE_MATH_MATRIX_H
