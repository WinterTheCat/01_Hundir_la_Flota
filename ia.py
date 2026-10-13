import numpy as np

from barcos import d_barcos, com_colocacion, col_barco, com_barco, com_hundido


def ia_colocar_barcos(tablero, d_boat_able, d_boat_pos, t_matriz):
    '''Función que permite colocar los barcos a la IA'''
    while 1 in d_boat_able.values():

        boats = [
            boat for boat, cantidad in d_boat_able.items()
            if cantidad == 1
        ]

        sel_boat = np.random.choice(boats)
        lng_boat = d_barcos[sel_boat]

        fil = np.random.randint(0, t_matriz)
        col = np.random.randint(0, t_matriz)
        drt_boat = np.random.choice(["H", "V"])

        pos_boat = com_colocacion(
            tablero,
            fil,
            col,
            lng_boat,
            drt_boat,
            t_matriz
        )

        if pos_boat:
            posiciones = col_barco(
                fil,
                col,
                lng_boat,
                pos_boat,
                tablero
            )

            d_boat_able[sel_boat] -= 1
            d_boat_pos[sel_boat] = posiciones


def ia_dis_barcos(tablero, d_boat_pos, t_matriz):
    '''Función que permite disparar a la IA'''
    fil = np.random.randint(0, t_matriz)
    col = np.random.randint(0, t_matriz)

    while tablero[fil][col] in [2, 3, 4]:
        fil = np.random.randint(0, t_matriz)
        col = np.random.randint(0, t_matriz)

    if tablero[fil][col] == 0:

        tablero[fil][col] = 2

        return False

    elif tablero[fil][col] == 1:

        tablero[fil][col] = 3

        barco = com_barco(
            fil,
            col,
            d_boat_pos
        )

        if com_hundido(
            tablero,
            barco,
            d_boat_pos
        ):
            for fil, col in d_boat_pos[barco]:
                tablero[fil][col] = 4

        return True