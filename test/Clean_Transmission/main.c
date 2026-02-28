#include <msp430.h>
#include "include/adc.h"
#include "include/assert.h"
#include "include/mcu_init.h"
#include "include/timer.h"
#include "include/uart.h"
#include "intrinsics.h"
#include <stdint.h>

// Flags
volatile uint8_t flag_adc = 0;
volatile uint8_t flag_uart = 0;

// Buffers
volatile uint32_t muestra_entrada[20] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
volatile uint16_t muestra;

int main(void) {
	WDTCTL = WDTPW | WDTHOLD;	// stop watchdog timer

	//Inicializo modulos
	pin_init();
	init_DCO();
	init_adc(&flag_adc, &muestra);
	init_timer();
	init_uart(&flag_uart, &muestra_entrada);

	// 1. Seleccionar la función de I/O de propósito general para P1.4
    // P1SEL.4 = 0 y P1SEL2.4 = 0 seleccionan la función de I/O digital [3, 6, 7].
    P1SEL &= ~BIT4;  // Limpiar el bit 4 en el registro P1SEL
    P1SEL2 &= ~BIT4; // Limpiar el bit 4 en el registro P1SEL2

    // 2. Configurar la dirección del pin P1.4 como salida
    // P1DIR.4 = 1 configura el pin 1.4 como salida [8, 9].
    P1DIR |= BIT4;   // Poner a 1 el bit 4 en el registro P1DIR

	__enable_interrupt();

	volatile uint8_t pos = 0;

	while(1){
		if (flag_adc == 1) {
			muestra_entrada[pos] = (muestra & 0x0000FFFF) * 32768;
			flag_adc = 0;
			pos++;
		}
		if (pos == 20) {
			pos = 0;
			uart_TX();
		}
	}

	return 0;
}
