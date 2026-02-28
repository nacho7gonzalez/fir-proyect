/**
* @file assert.h
* @brief Implementacion de ASSERT
*
* @version 1.0
* @date 15/05/25
*
* @author Ignacio Gonzalez
* @author Camila Assereto
* @author Pedro Arsuaga
*/

#ifndef ASSERT_H
#define ASSERT_H

#define DEBUG

#ifdef DEBUG
#define ASSERT(expr) {\
	if (!(expr)) {\
		P1OUT |= BIT6;\
		while(1){};\
	}\
}
#else
#define ASSERT(expr)

#endif

#endif
