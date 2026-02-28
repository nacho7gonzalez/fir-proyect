/**
* @file timer.h
* @brief Definiciones y declaraciones para el moulo de manejo del timer.
*
* Este archivo contiene las declaraciones de las funciones utilizadas para
* inicializar el timer que se utilizara para controlar el ADC.
*
* @version 1.0
* @date 15/05/25
*
* @author Ignacio Gonzalez
* @author Camila Assereto
* @author Pedro Arsuaga
*/

#ifndef TIMER_H
#define TIMER_H

#include <stdint.h>

/**
* @brief Inicializa el timer para la frecuencia de muestreo
*/
void init_timer();

void init_DCO();

#endif
