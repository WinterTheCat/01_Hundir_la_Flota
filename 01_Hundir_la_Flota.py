import numpy as np

d_barcos = {
    "Destructor": 2,
    "Submarino": 3,
    "Crucero": 3,
    "Acorazado": 4,
    "Portaaviones": 5
}

simbolos = {
    0: "≈",
    1: "■",
    2: "•",
    3: "✕",
    4: "☠"
}

c_letras = "ABCDEFGHIJKL"

# Primero elegimos el numero de jugadores, si es 1, el segundo jugador es una IA, si es 2, son dos jugadores.
def n_jugadores():
    while True:
        n_player = input(
            "Introduce el numero de jugadores: \n"
            "- 1 jugador, PVE.\n"
            "- 2 jugadores, PVP.")
        try:
            n_player = int(n_player)
            if n_player in [1,2]:
                return n_player
        except ValueError: 
            pass

# Aqui empezamos la comprobación de si el segundo jugador sera una IA o no.

# Luego seleccionamos la dificultad, para asi cambiar el tamaño de la matriz donde se jugara
def sel_dificultad():
    tamaños = {
        1:8,
        2:10,
        3:12
    }
    while True:
        n_dificultad = input(
            "Selecciona la dificultad de la partida:\n"
            "1- Facil, tablero 8X8.\n "
            "2- Normal, tablero 10X10.\n "
            "3- Dificil, tablero 12X12.")
        try:
            n_dificultad = int(n_dificultad)
            if n_dificultad in tamaños:
                return tamaños[n_dificultad]
        except ValueError:
            pass

# Ahora hacemos la matriz de juego usando el tamaño dado por la dificultad
def c_tablero(tamaño):
    tablero = np.zeros((tamaño, tamaño), dtype=int)
    return tablero

# Comenzamos el proceso de poner los barcos, pero para eso hacemos una función especializada en coger las coordenadas y comprobar que estan en la matriz, que usaremos constantemente más adelante
def sel_coordenada(t_matriz):
    while True:
        try:
            coord = input("Introduce una coordenada")
            letra = coord[0].upper()
            numero = coord[1:]

            columna = c_letras.index(letra)
            fila = int(numero) - 1
            if 0 <= columna < t_matriz and 0 <= fila < t_matriz:
                return fila, columna
            else:
                print("Coordenada fuera del tablero.")
        except (ValueError, IndexError):
            print("Coordenada no válida.")

# Ahora una función para elegir donde colocar los barcos
def sel_barco(boat_able):
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

# Miramos que en que dirección colocamos el barco.
def sel_direccion():
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

# Ahora si, comprobamos si el barco choca
def com_colocacion(t_tablero, fil, col, long, dircc, t_matriz):
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

def prep_barco(tablero, d_boat_able, d_boat_pos, t_matriz):

    selected_boat, lng_boat = sel_barco(d_boat_able)

    while True:
        fil, col = sel_coordenada(t_matriz)
        drt_barco = sel_direccion()
        
        pos_boat = com_colocacion(
            tablero, 
            fil, 
            col, 
            lng_boat, 
            drt_barco,
            t_matriz
            )

        if pos_boat:
            posiciones = col_barco(fil,col,lng_boat,pos_boat,tablero)
            d_boat_able[selected_boat] -= 1
            d_boat_pos[selected_boat] = posiciones

            mos_tablero(tablero)
            break
        
        else:
            print("Coordenada no valida, introduce otra")

def colocar_barcos(tablero, d_boat_able, d_boat_pos, t_matriz):
    
    print("\nTablero inicial:")
    mos_tablero(tablero)

    while 1 in d_boat_able.values():

        print("\nBarcos disponibles:")

        for i, (barco, cantidad) in enumerate(d_boat_able.items(), 1):
            if cantidad == 1:
                print(f"{i}- {barco}: Disponible")
            else:
                print(f"{i}- {barco}: No disponible")

        prep_barco(tablero, d_boat_able, d_boat_pos, t_matriz)

    print("\nTodos los barcos han sido colocados.")

def ia_colocar_barcos(tablero, d_boat_able, d_boat_pos, t_matriz):
    while 1 in d_boat_able.values():
        boats = [
            boat for boat, i in d_boat_able.items()
            if i == 1
        ]
        sel_boat = np.random.choice(boats)
        lng_boat = d_barcos[sel_boat]

        fil = np.random.randint(0, t_matriz)
        col = np.random.randint(0, t_matriz)
        drt_boat = np.random.choice(["H", "V"])

        pos_boat = com_colocacion(tablero, fil, col, lng_boat, drt_boat, t_matriz)

        if pos_boat:
            positions = col_barco(fil, col, lng_boat, pos_boat, tablero)

            d_boat_able[sel_boat] -=1
            d_boat_pos[sel_boat] = positions

def mos_tablero(tablero, b_ocultar = False):
    print("   ", end="")
    
    for i in range(len(tablero)):
        print(c_letras[i], end=" ")
    
    print()

    print("  " + "-" * (len(tablero) * 2 + 1))

    for i, fil in enumerate(tablero, 1):
        print(f"{i:2}|", end=" ")
        
        for j in fil:
            if b_ocultar and j == 1:
                print(simbolos[0], end=" ")
            else:
                print(simbolos[j], end=" ")
        
        print()

def com_barco(fil, col, d_boat_pos):

    for boat, pos in d_boat_pos.items():

        if (fil, col) in pos:
            return boat

    return False

def com_hundido(tablero, barco, d_boat_pos):

    for fil, col in d_boat_pos[barco]:
        if tablero[fil][col] not in [3, 4]:
            return False

    return True

def dis_barcos(tablero, d_boat_pos, t_matriz):
    fil, col = sel_coordenada(t_matriz)
    if tablero[fil][col] == 0:
        tablero[fil][col] = 2
        print("¡Agua!")
        mos_tablero(tablero, True)
        return False

    elif tablero[fil][col] == 1:
        tablero[fil][col] = 3
        print("¡Impacto!")

        boat = com_barco(fil, col, d_boat_pos)

        if com_hundido(tablero, boat, d_boat_pos):
            print(f"¡Has hundido el {boat}!")

            for fil, col in d_boat_pos[boat]:
                tablero[fil][col] = 4

        mos_tablero(tablero, True)
        return True

    else:
        print("Ya disparaste en esta posición")
        mos_tablero(tablero, True)
        return None

def ia_dis_barcos(tablero, d_boat_pos, t_matriz):
    fil = np.random.randint(0, t_matriz)
    col = np.random.randint(0, t_matriz)

    while tablero[fil][col] in [2, 3, 4]:
        fil = np.random.randint(0, t_matriz)
        col = np.random.randint(0, t_matriz)

    if tablero[fil][col] == 0:
        tablero[fil][col] = 2
        print(f"IA dispara en {c_letras[col]}{fil + 1}")
        print("¡Agua!")
        return False

    elif tablero[fil][col] == 1:
        tablero[fil][col] = 3
        print(f"IA dispara en {c_letras[col]}{fil + 1}")
        print("¡Impacto!")

        boat = com_barco(fil, col, d_boat_pos)

        if com_hundido(tablero, boat, d_boat_pos):
            print(f"¡La IA ha hundido el {boat}!")

            for fil, col in d_boat_pos[boat]:
                tablero[fil][col] = 4
        return True
# Por fin enmezamos a jugar:
def prep_partida():
    jugadores = n_jugadores()
    ia_player = jugadores == 1
    
    t_matriz = sel_dificultad()

    tablero_j1 = c_tablero(t_matriz)
    tablero_j2 = c_tablero(t_matriz)

    # Y cuentos barcos hay disponibles
    barcos_disponibles_j1 = {
        "Destructor": 1,
        "Submarino": 1,
        "Crucero": 1,
        "Acorazado": 1,
        "Portaaviones": 1
    }

    barcos_disponibles_j2 = {
        "Destructor": 1,
        "Submarino": 1,
        "Crucero": 1,
        "Acorazado": 1,
        "Portaaviones": 1
    }
    # Y aqui guardaremos sus posiciones
    barcos_posicion_j1 = {
        "Destructor": [],
        "Submarino": [],
        "Crucero": [],
        "Acorazado": [],
        "Portaaviones": []
    }

    barcos_posicion_j2 = {
        "Destructor": [],
        "Submarino": [],
        "Crucero": [],
        "Acorazado": [],
        "Portaaviones": []
    }

    colocar_barcos(tablero_j1, barcos_disponibles_j1, barcos_posicion_j1, t_matriz)
    if ia_player:
        ia_colocar_barcos(tablero_j2, barcos_disponibles_j2, barcos_posicion_j2, t_matriz)
    else:
        colocar_barcos(tablero_j2, barcos_disponibles_j2, barcos_posicion_j2, t_matriz)
    
    return tablero_j1, tablero_j2, barcos_posicion_j1, barcos_posicion_j2, t_matriz, jugadores, ia_player

tablero_j1, tablero_j2, posiciones_j1, posiciones_j2, t_matriz, jugadores, ia_player = prep_partida()

def com_victoria (tablero, d_boat_pos):
    for boat in d_boat_pos:
        if not com_hundido(tablero, boat, d_boat_pos):
            return False
    return True

def partida(tab_j1, tab_j2, pos_j1, pos_j2, t_matriz, ia_player):

    turn = 1

    while True:

        if turn == 1:
            print("Turno J1:")
            res = dis_barcos(tab_j2, pos_j2, t_matriz)

            if com_victoria(tab_j2, pos_j2):
                print("J1 ha ganado!")
                break

            if res is False:
                turn=2

        else:
            if ia_player:
                print("Turno IA:")
                res= ia_dis_barcos(tab_j1, pos_j1, t_matriz)
            else:
                print("Turno J2:")
                res = dis_barcos(tab_j1, pos_j1, t_matriz)

            if com_victoria(tab_j1, pos_j1):
                if ia_player:
                    print("IA ha ganado")
                else:
                    print("J2 ha ganado")
                break
            if res is False:
                turn=1

partida(tablero_j1, tablero_j2, posiciones_j1, posiciones_j2, t_matriz, ia_player)