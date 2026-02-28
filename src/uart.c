#include <msp430.h>
#include "../include/uart.h"
#include "msp430g2553.h"

static uint8_t* flag;
static uint32_t* dato;
static uint32_t dato_TX;
static uint8_t dato_UPUP;
static uint8_t dato_UP;
static uint8_t dato_DOWN;
static uint8_t dato_DOWNDOWN;
static uint8_t cont = 0;
static uint8_t pos = 0;

void init_uart(uint8_t* flag_main, uint32_t* dato_main){
/*
		UCSWRST : Software reset enable
		UCSSEL_2 : USCI clock source select = SMCLK
*/
	UCA0CTL1 |= UCSWRST;
	UCA0CTL1 |= UCSSEL_2;
/*
		Clock prescaler setting of the baud-rate generator
*/
	UCA0BR0 = 8;
	UCA0BR1 = 0;
/*
		Second modulation stage select
*/
	UCA0MCTL = UCBRS_0;
/*
		Pin configuration
*/
	P1SEL = BIT1 | BIT2;
	P1SEL2 = BIT1 | BIT2;
/*
		Software reset disable
*/
	UCA0CTL1 &= ~UCSWRST;

	flag = flag_main;
	dato = dato_main;
}

void uart_TX(){
	//P1OUT |= BIT4;
	pos = 0;
	IE2 |= UCA0TXIE;
}

#pragma vector = USCIAB0TX_VECTOR
__interrupt void UART_TX_ISR(){
	switch (cont) {
		case 0:
			UCA0TXBUF = 0xFF;
			cont++;
			break;
		case 1:
			dato_UPUP = ((dato[pos]) >> 24) & 0xFF;
			UCA0TXBUF = dato_UPUP;
			cont++;
			break;
		case 2:
			dato_UP = ((dato[pos]) >> 16) & 0xFF;
			UCA0TXBUF = dato_UP;
			cont++;
			break;
		case 3:
			dato_DOWN = ((dato[pos]) >> 8) & 0xFF;
			UCA0TXBUF = dato_DOWN;
			cont++;
			break;
		case 4:
			dato_DOWNDOWN = (dato[pos]) & 0xFF;
			UCA0TXBUF = dato_DOWNDOWN;
			cont = 0;
			pos++;
			if (pos == 20) {
				IE2 &= ~UCA0TXIE;
				//P1OUT &= ~BIT4;
			}
			break;
	}
}
