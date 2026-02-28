
# Filtros Digitales: Análisis comparativo de coeficientes (FIR9)

FIR9 es un proyecto de un filtro digital desarrollado en Code Composer Studio (CCSv20) utilizando el microcontrolador msp430g2553 de Texas Instrument junto con un Analog Discovery 2 como fuente de señal y un TTL-232R-3V3-PCB para la comunicación serial entre el uC y la PC. Se busca analizar el funcionamiento de un filtro digital con distintos tipos de datos.

## Demo

[Video Demo FIR9](https://youtu.be/LP_dkhqu6FU)

## Running Tests

Para realizar pruebas, debe ejecutarse elsiguiente comando:

```bash
  python serialScope.py
```
### Considerations

Si se quiere probar el filtro con coeficientes enteros de 16 bits deben realizarse los siguientes cambios:

- En el archivo 'serialScope.py', en la función 'conversionADC' debe descomentarse la linea referida a int16 y comentarse las referidas a int8 y float
- Dentro del archivo 'src/timer.c' debe cambiarse el valor del registro 'TA0CCR0' a 'fs_int16'
- En el archivo 'test/Filtered_Transmission/main.c' debe descomentarse la linea marcada como int16 y comentarse las lineas señaladas con int8 y float

Si se quiere probar el filtro con coeficientes enteros de 8 bits deben realizarse los siguientes cambios:

- En el archivo 'serialScope.py', en la función 'conversionADC' debe descomentarse la linea referida a int8 y comentarse las referidas a int16 y float
- Dentro del archivo 'src/timer.c' debe cambiarse el valor del registro 'TA0CCR0' a 'fs_int8'
- En el archivo 'test/Filtered_Transmission/main.c' debe descomentarse la linea marcada como int8 y comentarse las lineas señaladas con int16 y float

Si se quiere probar el filtro con coeficientes tipo float deben realizarse los siguientes cambios:

- En el archivo 'serialScope.py', en la función 'conversionADC' debe descomentarse la linea referida a float y comentarse las referidas a int16 e int8
- Dentro del archivo 'src/timer.c' debe cambiarse el valor del registro 'TA0CCR0' a 'fs_float'
- En el archivo 'test/Filtered_Transmission/main.c' debe descomentarse la linea marcada como float y comentarse las lineas señaladas con int16 e int8

## Authors

- [Ignacio Gonzalez](linkedin.com/in/ignaciogonzalez-eng)
- Pedro Arsuaga
- Camila Assereto
