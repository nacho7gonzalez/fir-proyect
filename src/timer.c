#include <msp430.h>
#include "../include/timer.h"
#include "msp430g2553.h"

volatile uint16_t fs_int16 = 20000; //800Hz
volatile uint16_t fs_int8 = 17300; //925Hz
volatile uint16_t fs_float = 27119; //590Hz

void init_DCO(){
	DCOCTL = 0x00;
/*
    Ajuste fino del DCO
    DCO = 011b =  3
*/
	DCOCTL = CALDCO_16MHZ;//DCO0 + DCO2;
/*
    Ajuste grueso del DCO
    RSEL = 1111b = 15
*/
	BCSCTL1 |= CALBC1_16MHZ;//RSEL0 + RSEL1 + RSEL2 + RSEL3;
/*
    Division del MCLK
    DIVM_0: /1
    Division del SCLK:
    DIVS_0: /1
*/
	BCSCTL2 |= DIVM_0 + DIVS_0;
}

void init_timer(){
/*
		TASSEL_2 : Timer_A0 clock source select = SMCLK
		ID_0 : Input divider = 1
		MC_1 : Mode control = Up mode
*/
	TA0CTL |= TASSEL_2 | ID_0 | MC_1;
/*
		CCIE : Interrupt enable for the CCIFG
*/
	TA0CCTL0 |= CCIE;
/*
		Sample rate for the ADC
*/
	TA0CCR0 = fs_int16;
}

#pragma vector = TIMER0_A0_VECTOR
__interrupt void TIMER_A0_ISR(){
	//ADC10CTL0 &= ~ENC;
	//P1OUT ^= BIT4;
	//P1OUT |= BIT4;
	ADC10CTL0 |= ENC | ADC10SC;
}
