#include <stdio.h>

// Code snippet from 'https://dev.to/pauljlucas/generic-in-c-i48'.
#include <wchar.h>

#define PRINTF_FORMAT(T)       \
  _Generic( (T),               \
    _Bool             : "%d",   \
    char              : "%c",   \
    signed char       : "%hhd", \
    unsigned char     : "%hhu", \
    short             : "%hd",  \
    int               : "%d",   \
    long              : "%ld",  \
    long long         : "%lld", \
    unsigned short    : "%hu",  \
    unsigned int      : "%u",   \
    unsigned long     : "%lu",  \
    unsigned long long: "%llu", \
    float             : "%f",   \
    double            : "%f",   \
    long double       : "%Lf",  \
    char*             : "%s",   \
    char const*       : "%s",   \
    wchar_t*          : "%ls",  \
    wchar_t const*    : "%ls",  \
    void*             : "%p",   \
    void const*       : "%p"    \
  )

#define PRINTF_PREAMBLE(T) \
  _Generic( (T),           \
    _Bool             : "<ret> = (bool) ",               \
    char              : "<ret> = (char) ",               \
    signed char       : "<ret> = (char) ",               \
    unsigned char     : "<ret> = (unsigned char) ",      \
    short             : "<ret> = (short) ",              \
    int               : "<ret> = (int) ",                \
    long              : "<ret> = (long) ",               \
    long long         : "<ret> = (long long) ",          \
    unsigned short    : "<ret> = (unsigned short) ",     \
    unsigned int      : "<ret> = (unsigned int) ",       \
    unsigned long     : "<ret> = (unsigned long) ",      \
    unsigned long long: "<ret> = (unsigned long long) ", \
    float             : "<ret> = (float) ",              \
    double            : "<ret> = (double) ",             \
    long double       : "<ret> = (long double) ",        \
    char*             : "<ret> = (char*) ",              \
    char const*       : "<ret> = (const char*) ",        \
    wchar_t*          : "<ret> = (wchar_t*) ",           \
    wchar_t const*    : "<ret> = (const wchar_t*) ",     \
    void*             : "<ret> = (void*) ",              \
    void const*       : "<ret> = (const void*) "         \
  )

#define PRINT(X) ( \
        printf(PRINTF_PREAMBLE((X))),    \
        printf(PRINTF_FORMAT((X)), (X)), \
        printf("\n") )

#define RAW_PRINT(X) printf(PRINTF_FORMAT((X)), (X))

#define PRINT_ARRAY(P, L) do { \
        if (__builtin_classify_type(P) == 5) \
            printf(PRINTF_PREAMBLE((P)));    \
            printf("[");                     \
            for (int I = 0; I < L; I++) {    \
                RAW_PRINT(P[I]);             \
                if (I < L-1) printf(", ");   \
            }                                \
            printf("]");                     \
    } while (0)

int main() {
    int i = 10;
    double d = 10.10;
    const char *s = "asdf";
    int ss[10] = { 1, 1, 1, 2, 2, 2 };
    PRINT(i);
    PRINT(d);
    PRINT(s);
    PRINT_ARRAY(ss, 10);
    return 0;
}
