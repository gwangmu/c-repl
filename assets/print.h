// Code snippet partially from 'https://dev.to/pauljlucas/generic-in-c-i48'.

#include <stdio.h>
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
    void const*       : "%p",   \
    default           : ""      \
  )

#define RAW_PRINT(X) dprintf(3, PRINTF_FORMAT((X)), (X))
