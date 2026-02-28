#include "../include/fir.h"
#include "../include/utils.h"
#include "msp430g2553.h"

static int32_t* buffer;
static int16_t coefs16[20] = {-2,
   -10,
   -33,
   -65,
   -27,
   311,
  1286,
  3052,
  5183,
  6688,
  6688,
  5183,
  3052,
  1286,
   311,
   -27
   -65,
   -33,
   -10,
    -2};
static int8_t coefs8[20] = {-2, -3, -4, -2, 7, 24, 51, 83, 111, 127, 127, 111, 83, 51, 24, 7, -2, -4, -3, -2};
static float coefsF[20] = {-0.002547079619331138,
-0.003900450048219113,
-0.005710997903564586,
-0.004481658246002947,
 0.005276562163313125,
 0.028012622612323856,
 0.063749337932417452,
 0.106395206220625840,
 0.145067904210716610,
 0.168138552677720820,
 0.168138552677720820,
 0.145067904210716610,
 0.106395206220625840,
 0.063749337932417452,
 0.028012622612323856,
 0.005276562163313125,
-0.004481658246002947,
-0.005710997903564586,
-0.003900450048219113,
-0.002547079619331138};

void init_fir(uint32_t* bufferDatos){
	buffer = bufferDatos;
	volatile uint8_t i = 0;
	//for(i = 0; i < MAX_TAPS; i++) coefs8[i] = (coefs16[i] >> 8) & 0xFF;
}

int32_t fir16(uint8_t index){
	volatile uint8_t i = 0;
	volatile int32_t res = 0;
	P1OUT |= BIT4;
	for(i = 0; i < MAX_TAPS; i++) res += (int32_t)(coefs16[i])*(buffer[(index - i + 20) % 20]);
	P1OUT &= ~BIT4;
	return res;
}

int32_t fir8(uint8_t index){
	volatile uint8_t i = 0;
	volatile int32_t res = 0;
	P1OUT |= BIT4;
	for(i = 0; i < MAX_TAPS; i++) res += (int32_t)(coefs8[i])*(int32_t)(buffer[(index - i + 20) % 20]);
	P1OUT &= ~BIT4;
	return res;
}

float firF(uint8_t index){
	volatile uint8_t i = 0;
	volatile float res = 0;
	P1OUT |= BIT4;
	for(i = 0; i < MAX_TAPS; i++) res += coefsF[i]*(float)(buffer[(index - i + 20) % 20]);
	P1OUT &= ~BIT4;
	return res;
}