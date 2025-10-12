#ifndef _UTILS_H
#define _UTILS_H

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

#define ERROR_PRINT_THEN_EXIT(msg...) \
    do { \
        fprintf(stderr, ##msg); \
        exit(1); \
    } while(0)

#endif