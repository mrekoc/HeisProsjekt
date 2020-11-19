/**
 * @file
 * @brief Door timer module
 */

#ifndef TIMER_H
#define TIMER_H

#include <stdlib.h>
#include <time.h>
#include <stdio.h>

#define TIME_LIMIT 3

/**
 * @brief Starts the timer.
 */
int timer_start(void);

/**
 * @brief Checks if timer has exceeded 3.
 * 
 * @return 1 if it exceeds 3, 0 otherwise.
 */
int timer_expire(void);

#endif