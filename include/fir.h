/**
* @file fir.h
* @brief Definiciones y declaraciones para la implementacion del FIR.
*
* Este archivo contiene las declaraciones de las funciones utilizadas para
* implementar el filtro FIR y manipular los datos asociados.
*
* @version 1.0
* @date 15/05/25
*
* @author Ignacio Gonzalez
* @author Camila Assereto
* @author Pedro Arsuaga
*/

#ifndef FIR_H
#define FIR_H

#include "machine/_stdint.h"
#include <stdint.h>

/**
* @brief Inicializacion de parametros a utilizar en el modulo FIR
*
* @param flag_main Puntero a bandera del main que indica salida lista
* @param int32_t Array con los ultimos MAX_TAPS datos
*/
void init_fir(uint32_t*);

/**
* @brief calcula la salida para las muestras en el buffer
*
* @param uint8_t indice de la cabeza del buffer circular
* @return int32_t Devuelve el valor de la salida para los MAX_TAPS datos
*/
int32_t fir16(uint8_t);

/**
* @brief calcula la salida para las muestras en el buffer
*
* @param uint8_t indice de la cabeza del buffer circular
* @return int32_t Devuelve el valor de la salida para los MAX_TAPS datos
*/
int32_t fir8(uint8_t);

/**
* @brief calcula la salida para las muestras en el buffer
*
* @param uint8_t indice de la cabeza del buffer circular
* @return float Devuelve el valor de la salida para los MAX_TAPS datos
*/
float firF(uint8_t);

#endif
