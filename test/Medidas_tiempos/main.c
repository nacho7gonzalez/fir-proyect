#include <msp430.h>
#include "include/timer.h"
#include "include/fir.h"
#include "intrinsics.h"
#include "include/adc.h"

volatile uint16_t buffer_muestras[20] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20};
volatile int32_t dato_main;
volatile uint16_t muestra;

int main(void) {
    
    WDTCTL = WDTPW | WDTHOLD; // Stop watchdog timer

    init_DCO();
    init_fir(&buffer_muestras);
    __enable_interrupt();

    // Configuración del pin P1.4 para emitir SMCLK en un MSP430G2553

// 1. Seleccionar la función periférica SMCLK para P1.4
//    Según [1], esto requiere P1SEL.4 = 1 y P1SEL2.4 = 0.
//    El bit 4 se controla con la máscara 0x10.

//P1SEL.4 = 1: Ponemos a 1 el bit 4 de P1SEL sin afectar otros bits.
P1SEL |= 0x10;   // Pone a 1 el bit 4 (P1.4) de P1SEL [1]

// P1SEL2.4 = 0: Ponemos a 0 el bit 4 de P1SEL2 sin afectar otros bits.
P1SEL2 &= ~0x10; // Pone a 0 el bit 4 (P1.4) de P1SEL2 [1]

// 2. Configurar la dirección del pin como salida para el periférico
//    Según [1], la función SMCLK es una salida ("Direction 1: Output").
//    Esto requiere P1DIR.4 = 1.

// P1DIR.4 = 1: Ponemos a 1 el bit 4 de P1DIR sin afectar otros bits.
P1DIR |= 0x10;   // Configura P1.4 como salida [1]

volatile uint8_t f;

dato_main = 0x12345678;
init_uart(&f, &dato_main);

uart_TX();


//init_timer();
//init_adc(f, muestra);

init_fir(buffer_muestras);

dato_main = fir();

    while (1) {

    }
    return 0;
}
