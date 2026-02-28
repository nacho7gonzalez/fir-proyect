#include <msp430.h>
#include "../include/adc.h"

volatile uint8_t* flag;
volatile int16_t* dato; 

void init_adc(uint8_t* flag_main, int16_t* dato_main){
/*
		SREF_1 : (VR+ = Vref+) , (VR- = Vss)
		ADC10SHT_0 : ADC sample and hold time = 4 cycles
		REFON : Reference generator ON
		REF2_5V : Vref+ = 2.5V
		ADC10ON : ADC10 ON
		ADC10IE : Interrupt enable
*/
	ADC10CTL0 |= SREF_1 | ADC10SHT_0 | REFON | REF2_5V | ADC10ON | ADC10IE;
/*
		INCH_7 : Input channel select = A7
		SHS_0 : Sample and hold source = ADC10SC bit
		ADC10DIV_0 : Clock divider = 1
		ADC10SSEL_2 : Clock source select = SMCLK
		CONSEQ_0 : Single-channel Single-conversion mode
*/
	ADC10CTL1 |= INCH_7 | SHS_0 | ADC10DIV_0 | ADC10SSEL_2 | CONSEQ_0;
/*
		BIT7 : Analog enable pin A7
*/
	ADC10AE0 |= BIT7;
/*
		ADC10CT : Data is transferred continuously
*/
	ADC10DTC0 |= ADC10CT;
/*
		20 Transfers per block
*/
	ADC10DTC1 = 1;
/*
		En dato_main se van a guardar los datos
		Data transfer start adress
*/
	ADC10SA = dato_main;
/*
		Espero que se estabilice la Ref del ADC
*/
	__delay_cycles(1000);

	dato = dato_main;
	flag = flag_main;
}

#pragma vector = ADC10_VECTOR
__interrupt void ADC10_ISR(void){
	ADC10CTL0 &= ~ENC;
	//P1OUT &= ~BIT4;
	*flag = 1;
}
