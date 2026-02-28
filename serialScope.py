import numpy as np
import matplotlib.pyplot as plt
import serial
import time
from collections import deque

# --- Funciones auxiliares ---

def limpiar_y_validar_secuencia_bytes(secuencia_bytes_brutos):
    """
    Recibo una secuencia de bytes idealmente con el siguiente formato: 0xFF DATO DATO DATO DATO 0xFF...
    Debo quuedarme solo con datos validos, es decir, con todos los datos entre 2 0xFF siempre y cuanado entre estos 0xFF haya 4 datos.
    En caso de quqe esto no se cumpla descartar los bytes entre estos 0xFF hasta el siguiente 0xFF.
    """
    secuencia_limpia_solo_datos = bytearray()
    i = 0
    n = len(secuencia_bytes_brutos)

    '''
    # 1. Descartar datos hasta el primer 0xFF
    while i < n and secuencia_bytes_brutos[i] != 0xFF:
        i += 1

    # 2. Procesar la secuencia, validando el patrón
    while i < n:
        if secuencia_bytes_brutos[i] == 0xFF:
            # Encontramos un 0xFF. Ahora esperamos 4 bytes de datos.
            if i + 6 <= n:  # Asegurarse de que hay al menos 0xFF + 4 datos
                if i + 6 == n or secuencia_bytes_brutos[i + 6] == 0xFF:
                    # El patrón es válido: 0xFF DATO DATO DATO DATO 0xFF (o fin de secuencia)
                    for j in range(1, 5):
                        secuencia_limpia_solo_datos.append(secuencia_bytes_brutos[i + j])
                    i += 6  # Mover el índice al siguiente byte después de los 4 datos
                else:
                    # El patrón está roto: 0xFF DATO DATO DATO DATO <OTRO_BYTE_QUE_NO_ES_FF>
                    for j in range(1, 5):
                        secuencia_limpia_solo_datos.append(secuencia_bytes_brutos[i + j])
                    i += 5  # Avanzamos para después de los 4 datos válidos
                    # Ahora, descartar todos los bytes hasta el próximo 0xFF
                    while i < n and secuencia_bytes_brutos[i] != 0xFF:
                        i += 1
            else:
                # No hay suficientes bytes para un patrón completo después de 0xFF (menos de 4 datos),
                # descartamos lo que queda y terminamos.
                break
        else:
            # Si llegamos aquí, significa que el 'i' no está en un 0xFF.
            # Esto puede ocurrir si el patrón se rompió y estamos buscando el próximo 0xFF.
            i += 1
            while i < n and secuencia_bytes_brutos[i] != 0xFF:
                i += 1
            # El bucle principal se encargará de procesar el 0xFF encontrado
    '''
    # Descarto valores hasta el primer 0xFF
    while i < n and secuencia_bytes_brutos[i] != 0xFF:
        i += 1
    # Proceso la secuencia
    while i < n:
        if secuencia_bytes_brutos[i] == 0xFF:
            # Encontramos un 0xFF. Ahora esperamos 4 bytes de datos.
            if i + 5  <= n:
                if i + 5 == n or secuencia_bytes_brutos[i + 5] == 0xFF: #Datovalido o llegue al final
                    for j in range(1,5):
                        secuencia_limpia_solo_datos.append(secuencia_bytes_brutos[i + j])
                    i += 5
                else: #Dato invalido, menos de 4 bytes hasta el siguiente 0xFF
                    while i < n and secuencia_bytes_brutos[i] != 0xFF:
                        i += 1
            else: #Sin bytes suficientes
                break
        else:
            while i < n and secuencia_bytes_brutos[i] != 0xFF:
                i += 1

    return secuencia_limpia_solo_datos

"""
def limpiar_y_validar_secuencia_bytes(secuencia_bytes_bruta):
    """"""
    Limpia y valida una secuencia de bytes con el patrón 0xFF DATO DATO DATO DATO.
    Descarta datos iniciales hasta el primer 0xFF.
    Si el patrón se rompe (más de 4 datos después de un 0xFF antes del siguiente 0xFF),
    se descartan los bytes extra hasta el próximo 0xFF.
    Solo los 4 bytes de datos válidos se añaden a la secuencia limpia (sin los 0xFF).

    Args:
        secuencia_bytes_bruta: Un bytearray o bytes que contiene la secuencia completa.

    Returns:
        Un nuevo bytearray con solo los bytes de datos válidos, sin los 0xFF.
    """"""
    secuencia_limpia_solo_datos = bytearray()
    i = 0
    n = len(secuencia_bytes_bruta)

    # 1. Descartar datos hasta el primer 0xFF
    while i < n and secuencia_bytes_bruta[i] != 0xFF:
        i += 1

    # 2. Procesar la secuencia, validando el patrón
    while i < n:
        if secuencia_bytes_bruta[i] == 0xFF:
            # Encontramos un 0xFF. Ahora esperamos 4 bytes de datos.
            # Y después de esos 4 datos, esperamos el siguiente 0xFF.
            if i + 6 <= n:  # Asegurarse de que hay al menos 0xFF + 4 datos
                # Verificamos si el 5to byte es otro 0xFF (o si estamos al final de la secuencia)
                if i + 6 == n or secuencia_bytes_bruta[i + 6] == 0xFF:
                    # El patrón es válido: 0xFF DATO DATO DATO DATO 0xFF (o fin de secuencia)
                    # Añadimos solo los 4 bytes de datos a la secuencia limpia
                    for j in range(1, 5):
                        secuencia_limpia_solo_datos.append(secuencia_bytes_bruta[i + j])
                    i += 6  # Mover el índice al siguiente byte después de los 4 datos
                else:
                    # El patrón está roto: 0xFF DATO DATO DATO DATO <OTRO_BYTE_QUE_NO_ES_FF>
                    # Añadimos los 4 datos válidos asociados a este 0xFF
                    for j in range(1, 5):
                        secuencia_limpia_solo_datos.append(secuencia_bytes_bruta[i + j])
                    i += 5  # Avanzamos para después de los 4 datos válidos
                    # Ahora, descartar todos los bytes hasta el próximo 0xFF
                    while i < n and secuencia_bytes_bruta[i] != 0xFF:
                        i += 1
                    # El bucle principal se encargará de procesar el 0xFF encontrado
            else:
                # No hay suficientes bytes para un patrón completo después de 0xFF (menos de 4 datos),
                # descartamos lo que queda y terminamos.
                break
        else:
            # Si llegamos aquí, significa que el 'i' no está en un 0xFF.
            # Esto puede ocurrir si el patrón se rompió y estamos buscando el próximo 0xFF.
            # Avanzamos hasta encontrar el próximo 0xFF.
            i += 1
            while i < n and secuencia_bytes_bruta[i] != 0xFF:
                i += 1
            # El bucle principal se encargará de procesar el 0xFF encontrado
    return secuencia_limpia_solo_datos
"""
def bytes_a_enteros_32_bits(secuencia_solo_datos):
    """
    Convierte una secuencia de bytes (sin 0xFF) en una lista de enteros de 32 bits.

    Args:
        secuencia_solo_datos: Un bytearray o bytes que solo contiene bytes de datos válidos,
                              donde cada 4 bytes representan un entero de 32 bits.

    Returns:
        Una lista de enteros.
    """
    if len(secuencia_solo_datos) % 4 != 0:
        print("Advertencia: La longitud de la secuencia de datos no es un múltiplo de 4. "
              "Esto podría indicar datos incompletos o un error al final de la secuencia.")

    valores_enteros = []
    # Iteramos la secuencia de 4 en 4 bytes
    for i in range(0, len(secuencia_solo_datos), 4):
        # Tomamos el bloque de 4 bytes
        bloque_bytes = secuencia_solo_datos[i:i+4]

        # Solo si tenemos un bloque completo de 4 bytes, lo convertimos
        if len(bloque_bytes) == 4:
            # Convertimos el bloque de bytes a un entero usando big-endian
            valor_entero = int.from_bytes(bloque_bytes, "big")
            valores_enteros.append(valor_entero)
        # Si el último bloque no es de 4 bytes, significa que está incompleto
        # y no lo procesamos como un entero de 32 bits válido.

    return valores_enteros

def conversionADC(valores_enteros, Vref, ADC_res):
    """
    Convierte valores enteros de un ADC a voltajes.

    Args:
        valores_enteros (list): Lista de valores enteros leídos del ADC.
        Vref (float): Voltaje de referencia del ADC.
        ADC_res (int): Resolución del ADC (ej. 1024 para 10 bits, 2**32 para 32 bits).

    Returns:

        list: Lista de valores de voltaje convertidos.
    """
    valores_voltaje = []

    for valor in valores_enteros:
        # Convertimos el valor del ADC a voltaje
        # (ADC_res - 1) representa el valor máximo que el ADC puede producir (ej. 1023 para 10 bits)
        
        # # INT16:
        voltaje = ((valor / (2**15)) * (Vref / (ADC_res - 1)))
        
        # INT8:
        #voltaje = ((valor * 5312 / ((2**15)*127)) * (Vref / (ADC_res - 1)))
        
        # # FLOAT:
        #voltaje = ((valor) * (Vref / (ADC_res - 1)))
        valores_voltaje.append(voltaje)

    return valores_voltaje


# --- Configuraciones del puerto serial y ADC ---
PORT = '/dev/ttyUSB0'
BAUD_RATE = 2000000
ADC_RESOLUTION = 1024
ADC_REFERENCE_VOLTAGE_RANGE = 2.5
SIGNAL_FREQUENCY = 50
CLEAN_SAMPLE_FREQUENCY = 6800
SAMPLES = int((5) * CLEAN_SAMPLE_FREQUENCY / SIGNAL_FREQUENCY)


# --- Configuración del estilo de Matplotlib ---
plt.style.use('seaborn-v0_8-darkgrid')

# --- Proceso principal: Lectura, procesamiento y graficación ---
try:
    ser = serial.Serial(
        port = PORT,  # Puerto serial a utilizar
        baudrate = BAUD_RATE,  # Velocidad de baudios
        bytesize = serial.EIGHTBITS,  # Tamaño de los bytes
        parity = serial.PARITY_NONE,  # Paridad
        stopbits = serial.STOPBITS_ONE,  # Bits de parada
        timeout = 5,  # Tiempo de espera para leer datos
    )
    vector_muestras = []
    # Buffer para acumular los bytes leídos
    # Usamos una deque para un buffer eficiente si la lectura es continua
    # En este caso, como leemos 150 veces de 5 bytes, una lista simple también funcionaría.
    # Pero si la lectura fuera byte a byte, deque sería mejor.
    buffer_bytes_leidos = bytearray()

    print(f"Abriendo puerto serial {PORT} a {BAUD_RATE} baudios...")
    # Lectura de datos
    for i in range(25):
        # Leer 5 bytes del puerto serial (0xFF + 4 datos)
        dato_leido = ser.read(20)
        vector_muestras.append(dato_leido)  # Almacenar el dato en la secuencia
        if not dato_leido:
            print(f"Advertencia: No se leyeron 5 bytes en la iteración {i+1}. Se leyó: {dato_leido}")
            break # Salir si no se leen datos
        buffer_bytes_leidos.extend(dato_leido)  # Añadir los bytes leídos al buffer

    ser.close()  # Cerrar el puerto serial después de la lectura
    print("Puerto serial cerrado.")



    # Convertir el buffer a un bytearray para las funciones de procesamiento
    secuencia_bytes_bruta = bytearray(buffer_bytes_leidos)

    # Paso 1: Limpiar y validar la secuencia de bytes (obteniendo solo los datos válidos)
    secuencia_solo_datos = limpiar_y_validar_secuencia_bytes(secuencia_bytes_bruta)
    #print(f"Secuencia de datos limpia (sin 0xFF): {secuencia_solo_datos.hex()}")

    vector_muestras = list(secuencia_solo_datos)  # Convertir a lista para iterar fácilmente
    i = 0
    print(vector_muestras)
    print(secuencia_bytes_bruta)
    #print(vector_muestras)
    #print(len(vector_muestras))
    '''
    while i < len(vector_muestras):
        print(vector_muestras[i])
        if vector_muestras[i] == 0xFF:
            print("If externo")
            # Encontramos un 0xFF. Ahora esperamos 4 bytes de datos.
            if i + 5 <= len(vector_muestras):
                # Verificamos si el 5to byte es otro 0xFF (o si estamos al final de la secuencia)
                if i + 5 == len(vector_muestras) or vector_muestras[i + 5] == '\xFF':
                    # El patrón es válido: 0xFF DATO DATO DATO DATO 0xFF (o fin de secuencia)
                    for j in range(1, 5):
                        print(vector_muestras[i + j])
                    i += 6
                else:
                    while i < len(vector_muestras) and vector_muestras[i] != '\xFF':
                        print(vector_muestras[i])
                        i += 1
            else:
                print("Else externo")
                print(vector_muestras[i])
                i += 1
'''
    # Paso 2: Convertir los bytes de datos a una lista de enteros de 32 bits
    valores_adc = bytes_a_enteros_32_bits(secuencia_solo_datos)
    #print(f"Valores enteros del ADC: {valores_adc}")

    # Paso 3: Convertir los valores enteros del ADC a voltajes
    voltajes = conversionADC(valores_adc, ADC_REFERENCE_VOLTAGE_RANGE, ADC_RESOLUTION)
    print(f"Valores de voltaje: {voltajes}")

    # Generar el índice para las muestras (eje X)
    muestras = range(len(voltajes))

    # --- Graficar muestras en el eje X y voltajes en el eje Y ---
    plt.figure(figsize=(12, 6)) # Tamaño de la figura un poco más grande para mejor visualización

    # Graficar los voltajes como una línea continua (sin marcadores)
    plt.plot(muestras, voltajes, linestyle='-', color='b', label='Voltaje del ADC')

    plt.xlabel("Número de Muestra")
    plt.ylabel("Voltaje (V)")
    plt.title("Datos del ADC recibidos por UART")

    # Ajustar los límites del eje Y para que se ajusten mejor a tu rango de voltaje
    # Puedes ajustar estos límites según los valores esperados de tu ADC.
    # Por ejemplo, si Vref es 2.5V, los valores deberían estar entre 0 y 2.5.
    plt.ylim(-1, 3) # Un poco por encima del Vref para ver el rango completo

    plt.grid(True) # Añade una cuadrícula
    plt.legend() # Muestra la leyenda
    plt.tight_layout() # Ajusta automáticamente los parámetros de la subtrama para un diseño ajustado
    plt.show() # Muestra el gráfico

except serial.SerialException as e:
    print(f"Error al abrir o leer del puerto serial: {e}")
    print("Asegúrate de que el puerto serial esté disponible y no esté siendo utilizado por otra aplicación.")
    print("Verifica que el nombre del puerto ({PORT}) sea correcto para tu sistema.")
except Exception as e:
    print(f"Ha ocurrido un error inesperado: {e}")

"""

# Librerias para trabajar con un puerto serial, numeros y plotear
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
from collections import deque


# Funciones auxiliares
def limpiar_y_validar_secuencia_bytes(secuencia_bytes):
    secuencia_limpia = bytearray()
    i = 0
    n = len(secuencia_bytes)

    # 1. Descartar datos hasta el primer 0xFF
    while i < n and secuencia_bytes[i] != 0xFF:
        i += 1

    # 2. Procesar la secuencia, validando el patrón
    while i < n:
        if secuencia_bytes[i] == 0xFF:
            # Encontramos un 0xFF. Ahora esperamos 4 bytes de datos.
            # Y después de esos 4 datos, esperamos el siguiente 0xFF.
            if i + 5 <= n:  # Asegurarse de que hay al menos 0xFF + 4 datos
                # Verificamos si los 4 bytes siguientes son realmente datos y si el 5to es 0xFF
                # O si estamos al final de la secuencia y este es el último patrón posible
                if i + 5 == n or secuencia_bytes[i + 5] == 0xFF:
                    # El patrón es válido: 0xFF DATO DATO DATO DATO 0xFF (o fin de secuencia)
                    for j in range(1, 5):
                        secuencia_limpia.append(secuencia_bytes[i + j])
                    i += 5  # Mover el índice al siguiente byte después de los 4 datos
                else:
                    # El patrón está roto: 0xFF DATO DATO DATO DATO <OTRO_BYTE_QUE_NO_ES_FF>
                    # 4 datos válidos
                    for j in range(1, 5):
                        secuencia_limpia.append(secuencia_bytes[i + j])
                    i += 5  # Avanzamos para después de los 4 datos válidos
                    # Ahora, descartar hasta el próximo 0xFF
                    while i < n and secuencia_bytes[i] != 0xFF:
                        i += 1
                    # El bucle principal se encargará de procesar el 0xFF encontrado
            else:
                # No hay suficientes bytes para un patrón completo después de 0xFF (menos de 4 datos),
                # descartamos lo que queda y terminamos.
                break
        else:
            # Esto NO debería ocurrir si la lógica de descarte inicial y la de patrones rotos funcionan.
            # Si llegamos aquí, significa que el 'i' no está en un 0xFF, por lo que avanzamos hasta encontrar uno.
            i += 1
            while i < n and secuencia_bytes[i] != 0xFF:
                i += 1
            # El bucle principal se encargará de procesar el 0xFF encontrado
    return secuencia_limpia

def bytes_a_enteros_32_bits(secuencia):
    valores_enteros = []

    # Iteramos la secuencia de 4 en 4 bytes
    for i in range(0, len(secuencia), 4):
        # Tomamos el bloque de 4 bytes
        bloque_bytes = secuencia[i:i+4]

        # Solo si tenemos un bloque completo de 4 bytes, lo convertimos
        if len(bloque_bytes) == 4:
            # Convertimos el bloque de bytes a un entero usando big-endian
            valor_entero = int.from_bytes(bloque_bytes, "big")
            valores_enteros.append(valor_entero)
        else:
            # Si el último bloque no es de 4 bytes, significa que está incompleto
            # y no lo procesamos como un entero de 32 bits válido.
            pass # o podrías loggear un error/advertencia
            
    return valores_enteros

def conversionADC(valores_enteros, Vref, ADC_res):
    valores = []
    
    for valor in valores_enteros:
        # Convertimos el valor del ADC a voltaje
        voltaje = (valor / (ADC_res - 1)) * Vref
        valores.append(voltaje)
    
    return valores


# Configuraciones
PORT = '/dev/ttyACM1'
BAUD_RATE = 115200
ADC_RESOLUTION = 1024  # Resolución del ADC (10 bits)
ADC_REFERENCE_VOLTAGE_RANGE = 2.5  # Rango de voltaje de referencia del ADC

ser = serial.Serial(
    port = PORT,  # Puerto serial a utilizar
    baudrate = BAUD_RATE,  # Velocidad de baudios
    bytesize = serial.EIGHTBITS,  # Tamaño de los bytes
    parity = serial.PARITY_NONE,  # Paridad
    stopbits = serial.STOPBITS_ONE,  # Bits de parada
    timeout = 1,  # Tiempo de espera para leer datos
)


# Lectura de datos
secuencia = []
for i in range(150):
    dato = ser.read(5) # Leer 5 bytes del puerto serial
    secuencia.append(dato)  # Almacenar el dato en la secuencia

ser.close()  # Cerrar el puerto serial después de la lectura

secuencia_filtrada = limpiar_y_validar_secuencia_bytes(secuencia)
valores_adc = bytes_a_enteros_32_bits(secuencia_filtrada)
voltajes = conversionADC(valores_adc, ADC_REFERENCE_VOLTAGE_RANGE, ADC_RESOLUTION)


# Genero el indice para las muestras
muestras = range(len(voltajes))  # Genera un rango de muestras basado en la longitud de los voltajes

print(muestras)

#Grafico muestras en el eje X y voltajes en el eje Y
plt.style.use('seaborn-v0_8-darkgrid')

plt.figure(figsize=(10, 5))
plt.plot(muestras, voltajes, marker='o', linestyle='-', color='b')
plt.xlabel("Número de Muestra")
plt.ylabel("Voltaje (V)")
plt.title("Datos del ADC10 recibidos por UART")
plt.ylim(-1, 3)
plt.show()
"""

"""
# Configuracion general
BUFFER_SIZE = 100  # Tamaño del buffer para almacenar muestras
PLOT_WINDOW_SIZE = 200

# ax.set_xlim(0, PLOT_WINDOW_SIZE)
plt.style.use('seaborn-v0_8-darkgrid')
plt.ion()  # Activa el modo interactivo para actualizar la gráfica en tiempo real
fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-')
ax.set_xlabel("Número de Muestra")
ax.set_ylabel("Voltaje (V)")
ax.set_title("Datos del ADC10 recibidos por UART")
ax.set_ylim(-1, 3)
# ax.set_xlim(0, PLOT_WINDOW_SIZE) # Podemos establecer un límite inicial en X, o dejar que se ajuste automáticamente

# Leer los datos del puerto serial en un bucle continuo y actualizarlos en la grafica
samples = deque(maxlen=PLOT_WINDOW_SIZE)

print(f"Intentando abrir puerto serial {PORT} a {BAUD_RATE} baudios...")
try:
    # Abre el puerto serial. El timeout=1 es útil para que la lectura no bloquee indefinidamente. [24]
   # ser = serial.Serial(PORT, BAUD_RATE, timeout=0.1)
    print(f"Puerto serial {PORT} abierto con éxito.")
    print("Esperando datos del microcontrolador...")

    byte_buffer = [] # Buffer temporal para almacenar bytes recibidos hasta tener un paquete completo

    while True:
        # Lee todos los bytes disponibles en el buffer de recepción del puerto serial
        if ser.in_waiting > 0:
            bytes_received = ser.read(ser.in_waiting)
            byte_buffer.extend(bytes_received)
            print(bytes_received)

            # Intentamos procesar pares de bytes del buffer
            while len(byte_buffer) >= 4:
                # Asumimos que el microcontrolador envía 2 bytes por muestra (LSB primero, luego MSB)
                # DEBES VERIFICAR EL ORDEN DE BYTES EN TU CÓDIGO DEL MSP430
                #mmsb = byte_buffer.pop(0)
                #msb = byte_buffer.pop(0)
                #mlsb = byte_buffer.pop(0)
                #lsb = byte_buffer.pop(0)

                # Reconstruye el valor de 16 bits.
                # Si envías LSB primero, luego MSB:
                #raw_adc_value = (msb << 8) | lsb
                # Si envías MSB primero, luego LSB:
                raw_adc_value = int.from_bytes(byte_buffer, "big")#(mmsb << 24) | (msb << 16) | (mlsb << 8) | lsb

                byte_buffer = byte_buffer[4:]  # Elimina los 4 bytes procesados del buffer

                # El ADC10 da valores de 0 a 1023. Asegurarse de que el valor esté en este rango si se usaron 16 bits para enviarlo
                # Dependiendo de cómo dividiste el valor de 16 bits en el MSP430, podrías necesitar enmascarar:
                # raw_adc_value = raw_adc_value & 0x03FF # Para asegurar que solo usamos los 10 bits bajos si necesario

                # Convierte el valor digital del ADC a voltaje. [2, 26]
                # Fórmula: Voltaje = (Valor_ADC / Max_Valor_ADC) * Rango_Voltaje_Referencia
                voltage = (raw_adc_value / (ADC_RESOLUTION - 1)) * ADC_REFERENCE_VOLTAGE_RANGE # Usar (ADC_RESOLUTION - 1) para el máximo valor (1023)

                samples.append(voltage) # Añade la muestra al buffer/deque

                # Si tenemos suficientes muestras, actualizamos el gráfico [Query]
                if len(samples) >= BUFFER_SIZE:
                    # Actualizar los datos de la línea
                    # Usamos range(len(samples)) para el eje X, que representa el índice de las muestras en la ventana
                    line.set_data(range(len(samples)), samples)

                    # Ajustar los límites del eje X dinámicamente
                    ax.set_xlim(0, len(samples))

                    # Re-dibujar el lienzo
                    fig.canvas.draw()
                    # Procesar eventos pendientes de la GUI
                    fig.canvas.flush_events()

        # Pequeña pausa para no sobrecargar la CPU mientras espera datos (INFORMACIÓN EXTERNA A LAS FUENTES)
        #time.sleep(0.001)

except serial.SerialException as e:
    print(f"Error de puerto serial: {e}")
except KeyboardInterrupt:
    print("Programa terminado por el usuario (Ctrl+C)")
except Exception as e:
    print(f"Ocurrió un error: {e}")
finally:
    # Asegúrate de cerrar el puerto serial al finalizar [21, 23]
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Puerto serial cerrado.")
    # Desactiva el modo interactivo y muestra el gráfico final si aún no está cerrado
    plt.ioff()
    # plt.show() # Descomentar si quieres que la ventana del gráfico permanezca abierta al finalizar
"""
