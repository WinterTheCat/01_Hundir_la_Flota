d_barcos = {
    "Destructor": 2,
    "Submarino": 3,
    "Crucero": 3,
    "Acorazado": 4,
    "Portaaviones": 5
}

def sel_barco(boat_able):
    '''Función original que nos permitia colocar los barcos usando la consola:
    - Usa numeros y cadenas de texto para ser elegido'''
    while True:
        try:
            boat = input("¿Qué barco quieres colocar? ")

            if boat.isdigit():
                boat = list(d_barcos)[int(boat) - 1]

            boat = boat.capitalize()

            if boat in d_barcos:
                if boat_able[boat] > 0:
                    return boat, d_barcos[boat]
                else:
                    print("Ya no quedan barcos de ese tipo.")
            else:
                print("Barco no disponible.")

        except (ValueError, IndexError):
            print("Barco no disponible.")

def sel_direccion():
    '''Función original para seleccionar mediante consola la dirección del barco'''
    while True:
        direccion = input("¿Dirección? 1- Horizontal, 2- Vertical: ")

        if direccion == "1":
            return "H"
        elif direccion == "2":
            return "V"
        elif direccion.upper() in ["H", "V"]:
            return direccion.upper()
        else:
            print("Dirección no válida.")

def com_colocacion(t_tablero, fil, col, long, dircc, t_matriz):
    '''Función que comprueba si el barco cabe en las coordenadas elegidas y lo coloca de izquiera a derecha o arriba abajo según el espacio disponible.'''
    if dircc == "H":
        if col + long - 1 < t_matriz:
            for i in range(long):
                if t_tablero[fil][col+i] !=0:
                    break
            else:
                return "D"
        if col - long + 1 >= 0:
            for i in range(long):
                if t_tablero[fil][col-i] !=0:
                    break
            else:
                    return "I"
    elif dircc == "V":
        if fil + long - 1 < t_matriz:
            for i in range(long):
                if t_tablero[fil + i][col] != 0:
                    break
            else:
                return "A"

        if fil - long + 1 >= 0:
            for i in range(long):
                if t_tablero[fil - i][col] != 0:
                    break
            else:
                return "B"

    return False

def col_barco(fil, col, long, pos, tablero):
    '''Si todo esta bien, coloca el barco en su sitio'''
    posiciones = []
    
    if pos == "D":
        for i in range(long):
            tablero[fil][col +i] = 1
            posiciones.append((fil, col + i))

    elif pos == "I":
            for i in range(long):
                tablero[fil][col -i] = 1
                posiciones.append((fil, col - i))

    elif pos == "A":
            for i in range(long):
                tablero[fil+i][col] = 1
                posiciones.append((fil + i, col))

    elif pos == "B":
            for i in range(long):
                tablero[fil-i][col] = 1
                posiciones.append((fil - i, col))
    
    return posiciones

def com_barco(fil, col, d_boat_pos):
    '''Comprueba si hay un barco en esa posición'''

    for boat, pos in d_boat_pos.items():

        if (fil, col) in pos:
            return boat

    return False

def com_hundido(tablero, barco, d_boat_pos):
    '''Comprueba si el barco se ha hundido'''
    for fil, col in d_boat_pos[barco]:
        if tablero[fil][col] not in [3, 4]:
            return False

    return True

