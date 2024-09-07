PRECIO_BASE = 50000

def es_bisiesto(anio):
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

def es_numero_valido(cadena):
    return cadena.isdigit()

def es_fecha_valida(fecha_str):
    partes = fecha_str.split("/")
    if len(partes) != 3:
        return False
    
    dia_str, mes_str, anio_str = partes
    if not (es_numero_valido(dia_str) and es_numero_valido(mes_str) and es_numero_valido(anio_str)):
        return False
    
    dia, mes, anio = int(dia_str), int(mes_str), int(anio_str)
    
    if mes < 1 or mes > 12:
        return False
    
    dias_por_mes = [31, 29 if es_bisiesto(anio) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    if dia < 1 or dia > dias_por_mes[mes - 1]:
        return False
    
    return True

def solicitar_fecha_valida():
    fecha = input("Introduce la fecha del espectáculo (DD/MM/AAAA): ")
    while not es_fecha_valida(fecha):
        print("Fecha no válida. Por favor, ingrese una fecha válida.")
        fecha = input("Introduce la fecha del espectáculo (DD/MM/AAAA): ")
    return fecha

def cargar_espectaculos():
    nombres = []
    fechas = []
    asientos_list = []
    
    n = int(input("Introduce la cantidad de espectáculos: "))
    for i in range(n):
        nombre = input(f"Introduce el nombre del espectáculo {i + 1}: ")
        fecha = solicitar_fecha_valida()
        filas = int(input("Introduce el número de filas de asientos: "))
        columnas = int(input("Introduce el número de asientos por fila: "))
        asientos = [[0] * columnas for _ in range(filas)]  # 0 = libre, 1 = ocupado
        
        nombres.append(nombre)
        fechas.append(fecha)
        asientos_list.append(asientos)
    
    return nombres, fechas, asientos_list

def mostrar_asientos(asientos, nombre, fecha):
    print(f"Asientos para el espectáculo '{nombre}' en la fecha {fecha}:")
    for fila in asientos:
        linea = ""
        for asiento in fila:
            linea += str(asiento) + " "
        print(linea.strip())

def calcular_precio(fila):
    if fila < 3:  # Si la fila está entre las primeras 3
        return PRECIO_BASE * 1.4  # 40% más caro
    else:
        return PRECIO_BASE

def reservar_entrada(asientos, nombre, fecha):
    while True:
        mostrar_asientos(asientos, nombre, fecha)  # Mostrar la sala antes de la reserva con nombre y fecha
        fila = int(input("Introduce el número de fila: "))
        columna = int(input("Introduce el número de asiento: "))
        
        if fila >= 0 and fila < len(asientos) and columna >= 0 and columna < len(asientos[0]):
            if asientos[fila][columna] == 0:  # Si el asiento está libre
                precio = calcular_precio(fila)
                print(f"El precio de la butaca es de: {precio} pesos.")
                confirmar = input("¿Desea confirmar la reserva? (si/no): ")
                if confirmar.lower() == 'si':
                    asientos[fila][columna] = 1  # Reservar el asiento
                    print("Reserva exitosa.")
                    break
                else:
                    print("Reserva cancelada.")
            else:
                print("El asiento ya está ocupado. Elige otro asiento.")
        else:
            print("Número de fila o columna inválido. Inténtalo de nuevo.")

def consultar_disponibilidad(asientos):
    libres = sum(fila.count(0) for fila in asientos)
    ocupados = sum(fila.count(1) for fila in asientos)
    print(f"Asientos libres: {libres}, Asientos ocupados: {ocupados}")

def cancelar_reserva(asientos, fila, columna):
    if asientos[fila][columna] == 1:  # Si el asiento está ocupado
        asientos[fila][columna] = 0  # Liberar el asiento
        print("Reserva cancelada.")
    else:
        print("El asiento ya estaba libre.")

def main():
    nombres, fechas, asientos_list = cargar_espectaculos()
    
    while True:
        print("\n--- Gestión de Entradas ---")
        print("1. Mostrar asientos disponibles")
        print("2. Reservar entrada")
        print("3. Consultar disponibilidad")
        print("4. Cancelar reserva")
        print("5. Salir")
        opcion = int(input("Selecciona una opción: "))
        
        if opcion == 5:
            break
        
        for i, nombre in enumerate(nombres):
            print(f"{i + 1}. {nombre} - {fechas[i]}")
        
        espectaculo_index = int(input("Selecciona el número del espectáculo: ")) - 1
        
        if 0 <= espectaculo_index < len(nombres):
            nombre = nombres[espectaculo_index]
            fecha = fechas[espectaculo_index]
            asientos = asientos_list[espectaculo_index]
            
            if opcion == 1:
                mostrar_asientos(asientos, nombre, fecha)
            elif opcion == 2:
                reservar_entrada(asientos, nombre, fecha)
            elif opcion == 3:
                consultar_disponibilidad(asientos)
            elif opcion == 4:
                fila = int(input("Introduce el número de fila: "))
                columna = int(input("Introduce el número de asiento: "))
                cancelar_reserva(asientos, fila, columna)
        else:
            print("Espectáculo no encontrado.")

if __name__ == "__main__":
    main()

