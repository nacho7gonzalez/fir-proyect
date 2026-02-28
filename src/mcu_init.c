#include <msp430.h>
#include "../include/mcu_init.h"

void pin_init(){
	P2OUT = 0x00;
	P2DIR = 0xFF;
	P3OUT = 0x00;
	P3DIR = 0xFF;
}
