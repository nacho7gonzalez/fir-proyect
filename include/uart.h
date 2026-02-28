/**
* @file uart.h
* @brief Definiciones y declaraciones para el moulo UART.
*
* Este archivo contiene las declaraciones de las funciones utilizadas para
* inicializar el UART y para enviar la senial filtrada a la computadora
*
* @version 1.0
* @date 15/05/25
*
* @author Ignacio Gonzalez
* @author Camila Assereto
* @author Pedro Arsuaga
*/

#ifndef UART_H
#define UART_H

#include <stdint.h>

/**
* @brief Configuracion inicial del modulo UART. Datos de 8 bits, 9600bps
* y sin paridad.
*
* @param uint8_t Puntero a bandera en main que indica dato transmitido
* por completo
*/
void init_uart(uint8_t*,uint32_t*);

/**
* @brief Transmite una cadena de caracteres mediante el modulo UART.
*/
void uart_TX();

#endif
