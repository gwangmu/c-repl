#include <stdio.h>

struct __test_struct__ {
    int x;
    float y;
    char *z;
};

union __test_union__ {
    int x;
    float y;
    char *z;
};

struct __test_ml_struct__ {
    int x;
    float y;
    char *z;
    struct __test_ml2_struct__ {
        int p;
        float q;
    } ml2;
    struct {
        int a;
        float b;
    } noname;
    union __test_ml3_union__ {
        int e;
        float f;
    } un;
    struct __test_struct__ sss;
};

enum __test_enum__ {
    ENUM_ELEM_1,
    ENUM_ELEM_2
};

typedef struct __test_ml_struct__ __test_typedef__;
typedef __test_typedef__ __test_typedef2__;
typedef __test_typedef2__ __test_typedef3__;
typedef float my_float;

struct __test_struct_2__ {
    int x;
    float y;
    char *z;
    struct __test_struct__ sss;
};

int foo() {
    struct __test_struct__ s1;
    union __test_union__ u1;
    struct __test_ml_struct__ s2;
    __test_typedef__ s3;
    return 0;
}
