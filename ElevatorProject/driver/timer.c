#include "timer.h"

/**
 * @brief Used to store value of @c time(NULL). 
 */
static int m_timeValue = -1;

int timer_start(void){

    m_timeValue = time(NULL);

    return 0;
}

int timer_expire(void){

    if (m_timeValue == -1) {
        return 0;
    }
    else {
        return (time(NULL)- m_timeValue >= TIME_LIMIT);
    }
}