/**
* @file adc.h
* @brief Definiciones y declaraciones para el moulo de manejo del adc.
*
* Este archivo contiene las declaraciones de las funciones utilizadas para
* inicializar el ADC, y para muestrear y convertir una senial analogica
* a digital
*
* @version 1.0
* @date 15/05/25
*
* @author Ignacio Gonzalez
* @author Camila Assereto
* @author Pedro Arsuaga
*/

#ifndef ADC_H
#define ADC_H

#include <stdint.h>

/**
* @brief Inicializa el ADC en Single-channel Single-conversion mode.
* Configura el ADC para recibir los datos de la senial y configura la
* bandera que sera utilizada para indicar cuando los datos sean validos
*
* @param int8_t Punteroa la bandera a configurar.
* @param int32_t Arreglo donde se guardan los datos
*/
void init_adc(uint8_t*, int16_t*);

#endif
