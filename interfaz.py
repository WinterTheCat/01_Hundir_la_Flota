import tkinter as tk
import numpy as np

from barcos import d_barcos, com_colocacion, col_barco, com_barco, com_hundido
from ia import ia_colocar_barcos, ia_dis_barcos


def limpiar_ventana(ventana):
    '''
    Función que nos limpia la pantalla visible para cuando hacemos cambios de jugador o de escena
    '''
    for widget in ventana.winfo_children():
        widget.destroy()


def mostrar_menu(ventana):
    '''
    Función que enseña el menu de juego, cada vez que empieza la partida.
    Usa la libreria TKinter para crear labels y botones que usaremos en el juego.
    '''
    limpiar_ventana(ventana)

    titulo = tk.Label(
        ventana,
        text="HUNDIR LA FLOTA",
        font=("Arial", 24)
    )
    titulo.pack(pady=20)

    texto_jugadores = tk.Label(
        ventana,
        text="¿Cuántos jugadores?",
        font=("Arial", 16)
    )
    texto_jugadores.pack(pady=20)

    boton_1 = tk.Button(
        ventana,
        text="1 Jugador",
        command=lambda: mos_seleccion_dificultad(ventana, 1)
    )
    boton_1.pack(pady=10)

    boton_2 = tk.Button(
        ventana,
        text="2 Jugadores",
        command=lambda: mos_seleccion_dificultad(ventana, 2)
    )
    boton_2.pack(pady=10)


def iniciar_interfaz():
    '''
    Función que crea la ventana de juego e invoca mostrar_menu() para poblarla.
    Usa la libreria TKinter para crear una interfaz grafica.
    '''
    ventana = tk.Tk()

    ventana.title("Hundir la Flota")
    ventana.geometry("1200x800")
    ventana.resizable(False, False)

    mostrar_menu(ventana)

    ventana.mainloop()


def mos_seleccion_dificultad(ventana, numero):
    '''
    Función que devuelve el tamaño de la matriz que usaremos en base a la dificultad seleccionada
    '''
    limpiar_ventana(ventana)

    texto_dificultad = tk.Label(
        ventana,
        text="Selecciona la dificultad",
        font=("Arial", 20)
    )
    texto_dificultad.pack(pady=30)

    facil = tk.Button(
        ventana,
        text="Fácil - 8x8",
        command=lambda: mos_seleccion_jugadores(ventana, numero, 8, 1)
    )
    facil.pack(pady=10)

    normal = tk.Button(
        ventana,
        text="Normal - 10x10",
        command=lambda: mos_seleccion_jugadores(ventana, numero, 10, 1)
    )
    normal.pack(pady=10)

    dificil = tk.Button(
        ventana,
        text="Difícil - 12x12",
        command=lambda: mos_seleccion_jugadores(ventana, numero, 12, 1)
    )
    dificil.pack(pady=10)


def mos_seleccion_jugadores(ventana, numero_jugadores, tamaño, jugador):
    '''
    Función que marca el numero de jugadores:
    - Si son 2, se juega PvP
    - Si es 1, se juega PvE
    '''
    jugadores = {
        1: {},
        2: {}
    }

    preparar_jugador(
        ventana,
        numero_jugadores,
        tamaño,
        jugador,
        jugadores
    )


def preparar_jugador(ventana, numero_jugadores, tamaño, jugador, jugadores):
    '''
    Función que utiliza todos los datos dados por la selección de partida para comenzar la partida en PvP o PvE
    '''
    botones = {}
    botones_sel_barco = {}
    botones_direccion = {}

    barco_seleccionado = [None]
    direccion_seleccionada = [None]

    tablero = np.zeros(
        (tamaño, tamaño),
        dtype=int
    )

    barcos_disponibles = {
        "Destructor": 1,
        "Submarino": 1,
        "Crucero": 1,
        "Acorazado": 1,
        "Portaaviones": 1
    }

    posiciones_barcos = {
        "Destructor": [],
        "Submarino": [],
        "Crucero": [],
        "Acorazado": [],
        "Portaaviones": []
    }

    jugadores[jugador]["tablero"] = tablero
    jugadores[jugador]["posiciones_barcos"] = posiciones_barcos

    mostrar_colocacion(
        ventana,
        tablero,
        barcos_disponibles,
        posiciones_barcos,
        tamaño,
        barco_seleccionado,
        direccion_seleccionada,
        botones,
        botones_sel_barco,
        botones_direccion,
        numero_jugadores,
        jugador,
        jugadores
    )


def mostrar_colocacion(
    ventana,
    tablero,
    barcos_disponibles,
    posiciones_barcos,
    tamaño,
    barco_seleccionado,
    direccion_seleccionada,
    botones,
    botones_sel_barco,
    botones_direccion,
    numero_jugadores,
    jugador,
    jugadores
):
    """Construye la interfaz de colocación de barcos del jugador actual.

    Limpia la ventana, muestra los controles para seleccionar barcos y
    direcciones, dibuja el tablero y añade el botón para confirmar
    la colocación.
    """
    limpiar_ventana(ventana)

    titulo = tk.Label(
        ventana,
        text=f"Coloca tus barcos - Jugador {jugador}",
        font=("Arial", 20)
    )
    titulo.pack(pady=10)

    frame_controles = tk.Frame(ventana)
    frame_controles.pack(pady=10)

    texto_barcos = tk.Label(
        frame_controles,
        text="Selecciona un barco",
        font=("Arial", 14)
    )
    texto_barcos.grid(
        row=0,
        column=0,
        columnspan=5
    )

    for i, barco in enumerate(barcos_disponibles):

        boton = tk.Button(
            frame_controles,
            text=barco,
            width=12,
            command=lambda b=barco: seleccionar_barco(
                b,
                barco_seleccionado,
                barcos_disponibles,
                botones_sel_barco
            )
        )

        botones_sel_barco[barco] = boton

        boton.grid(
            row=1,
            column=i,
            padx=0,
            pady=0
        )

    texto_direccion = tk.Label(
        frame_controles,
        text="Dirección",
        font=("Arial", 12)
    )

    texto_direccion.grid(
        row=2,
        column=0,
        columnspan=5,
        pady=(5, 0)
    )

    boton_horizontal = tk.Button(
        frame_controles,
        text="Horizontal",
        command=lambda: seleccionar_direccion(
            "H",
            direccion_seleccionada,
            botones_direccion
        )
    )

    botones_direccion["H"] = boton_horizontal

    boton_horizontal.grid(
        row=3,
        column=0,
        columnspan=2,
        padx=2,
        pady=5
    )

    boton_vertical = tk.Button(
        frame_controles,
        text="Vertical",
        command=lambda: seleccionar_direccion(
            "V",
            direccion_seleccionada,
            botones_direccion
        )
    )

    botones_direccion["V"] = boton_vertical

    boton_vertical.grid(
        row=3,
        column=2,
        columnspan=2,
        padx=2,
        pady=5
    )

    frame_tablero = tk.Frame(ventana)
    frame_tablero.pack(pady=10)

    mostrar_tablero_colocacion(
        ventana,
        frame_tablero,
        tablero,
        barcos_disponibles,
        posiciones_barcos,
        tamaño,
        barco_seleccionado,
        direccion_seleccionada,
        botones,
        botones_sel_barco,
        numero_jugadores,
        jugador,
        jugadores
    )

    boton_confirmar = tk.Button(
        ventana,
        text="Confirmar colocación",
        command=lambda: confirmar_colocacion(
            ventana,
            barcos_disponibles,
            numero_jugadores,
            jugador,
            jugadores,
            tamaño
        )
    )

    boton_confirmar.pack(pady=15)


def seleccionar_barco(barco, barco_seleccionado, botones_sel_barco):
    '''Función que usa el boton de seleccionar el barco para indicar cual se va a colocar en el tablero'''

    for boton in botones_sel_barco.values():
        boton.config(relief="raised")

    botones_sel_barco[barco].config(
        relief="sunken"
    )

    barco_seleccionado[0] = barco

    print("Barco seleccionado:", barco)


def seleccionar_direccion(direccion, direccion_seleccionada, botones_direccion):
    '''Función que usa el boton de seleccionar la dirrección para indicar cual se va a colocar en el tablero'''

    for boton in botones_direccion.values():
        boton.config(relief="raised")

    botones_direccion[direccion].config(
        relief="sunken"
    )

    direccion_seleccionada[0] = direccion

    print("Dirección seleccionada:", direccion)


def mostrar_tablero_colocacion(
    ventana,
    frame_tablero,
    tablero,
    barcos_disponibles,
    posiciones_barcos,
    tamaño,
    barco_seleccionado,
    direccion_seleccionada,
    botones,
    botones_sel_barco,
    numero_jugadores,
    jugador,
    jugadores
):
    """Dibuja las coordenadas y las casillas del tablero de colocación.

    Muestra las letras de las columnas y los números de las filas.
    Crea un botón interactivo para cada casilla mediante
    crear_boton_colocacion().
    """
    for columna in range(tamaño):

        letra = chr(65 + columna)

        etiqueta = tk.Label(
            frame_tablero,
            text=letra,
            font=("Arial", 12, "bold"),
            width=3
        )

        etiqueta.grid(
            row=5,
            column=columna + 1
        )

    for fila in range(tamaño):

        etiqueta = tk.Label(
            frame_tablero,
            text=fila + 1,
            font=("Arial", 12, "bold"),
            width=3
        )

        etiqueta.grid(
            row=fila + 6,
            column=0
        )

        for columna in range(tamaño):

            crear_boton_colocacion(
                ventana,
                frame_tablero,
                tablero,
                fila,
                columna,
                barcos_disponibles,
                posiciones_barcos,
                tamaño,
                barco_seleccionado,
                direccion_seleccionada,
                botones,
                botones_sel_barco,
                numero_jugadores,
                jugador,
                jugadores
            )


def crear_boton_colocacion(
    ventana,
    frame_tablero,
    tablero,
    fila,
    columna,
    barcos_disponibles,
    posiciones_barcos,
    tamaño,
    barco_seleccionado,
    direccion_seleccionada,
    botones,
    botones_sel_barco,
    numero_jugadores,
    jugador,
    jugadores
):
    """Crea y configura el botón correspondiente a una casilla del tablero.

    Guarda el botón en el diccionario de botones, establece la acción
    que se ejecutará al pulsarlo y lo coloca en la cuadrícula visual.
    """
    boton = tk.Button(
        frame_tablero,
        text="≈",
        width=2,
        height=1,
        bg="white",
        fg="blue"
    )

    botones[(fila, columna)] = boton

    boton.config(
        command=lambda: colocar_barco_gui(
            ventana,
            tablero,
            fila,
            columna,
            boton,
            barcos_disponibles,
            posiciones_barcos,
            tamaño,
            barco_seleccionado,
            direccion_seleccionada,
            botones,
            botones_sel_barco,
            numero_jugadores,
            jugador,
            jugadores
        )
    )

    boton.grid(
        row=fila + 6,
        column=columna + 1,
        padx=0,
        pady=0
    )


def colocar_barco_gui(
    ventana,
    tablero,
    fila,
    columna,
    boton,
    barcos_disponibles,
    posiciones_barcos,
    tamaño,
    barco_seleccionado,
    direccion_seleccionada,
    botones,
    botones_sel_barco,
    numero_jugadores,
    jugador,
    jugadores
):
    '''Gestiona la colocación o recolocación de un barco cuando se pulsa una casilla.'''

    if barco_seleccionado[0] is None:
        print("Selecciona un barco.")
        return

    if direccion_seleccionada[0] is None:
        print("Selecciona una dirección.")
        return

    barco = barco_seleccionado[0]

    longitud = d_barcos[barco]

    posiciones_antiguas = posiciones_barcos[barco]

    if posiciones_antiguas:

        for fil, col in posiciones_antiguas:

            tablero[fil][col] = 0

            botones[(fil, col)].config(
                text="≈",
                bg="white",
                fg="blue"
            )

    posicion = com_colocacion(
        tablero,
        fila,
        columna,
        longitud,
        direccion_seleccionada[0],
        tamaño
    )

    if not posicion:

        print("No se puede colocar el barco aquí.")

        for fil, col in posiciones_antiguas:

            tablero[fil][col] = 1

            botones[(fil, col)].config(
                text="■",
                bg="white",
                fg="black"
            )

        return

    posiciones = col_barco(
        fila,
        columna,
        longitud,
        posicion,
        tablero
    )

    barcos_disponibles[barco] = 0

    posiciones_barcos[barco] = posiciones

    botones_sel_barco[barco].config(
        relief="raised",
        bg="gray",
        fg="white"
    )

    for fil, col in posiciones:

        botones[(fil, col)].config(
            text="■",
            bg="white",
            fg="black"
        )

    print("Barco colocado:")
    print(barco)
    print(posiciones)


def confirmar_colocacion(
    ventana,
    barcos_disponibles,
    numero_jugadores,
    jugador,
    jugadores,
    tamaño
):
    '''Comprueba si la colocación de todos los barcos está completa y avanza a la siguiente fase de la partida.'''
    if any(
        cantidad > 0
        for cantidad in barcos_disponibles.values()
    ):

        print("Debes colocar todos los barcos.")
        return

    if numero_jugadores == 2 and jugador == 1:

        preparar_jugador(
            ventana,
            numero_jugadores,
            tamaño,
            2,
            jugadores
        )

    elif numero_jugadores == 2 and jugador == 2:

        iniciar_combate(
            ventana,
            jugadores,
            tamaño,
            numero_jugadores
            )

    elif numero_jugadores == 1:

        tablero_ia = np.zeros(
            (tamaño, tamaño),
            dtype=int
        )

        barcos_disponibles_ia = {
            "Destructor": 1,
            "Submarino": 1,
            "Crucero": 1,
            "Acorazado": 1,
            "Portaaviones": 1
        }

        posiciones_barcos_ia = {
            "Destructor": [],
            "Submarino": [],
            "Crucero": [],
            "Acorazado": [],
            "Portaaviones": []
        }

        ia_colocar_barcos(
            tablero_ia,
            barcos_disponibles_ia,
            posiciones_barcos_ia,
            tamaño
        )

        jugadores[2]["tablero"] = tablero_ia

        jugadores[2]["posiciones_barcos"] = posiciones_barcos_ia

        print("Tablero de la IA:")
        print(tablero_ia)

        iniciar_combate(
            ventana,
            jugadores,
            tamaño,
            numero_jugadores
        )


def iniciar_combate(
    ventana,
    jugadores,
    tamaño,
    numero_jugadores
):
    '''Inicia el combate despues de colocar los barcos'''

    mostrar_turno(
        ventana,
        jugadores,
        tamaño,
        1,
        numero_jugadores
    )


def cambiar_turno(
    ventana,
    jugadores,
    tamaño,
    jugador_actual,
    numero_jugadores
):
    '''Cambia el jugador activo y gestiona las acciones correspondientes al siguiente turno'''
    siguiente_jugador = 2 if jugador_actual == 1 else 1

    # PARTIDA CONTRA IA
    if numero_jugadores == 1 and siguiente_jugador == 2:

        impacto = ia_dis_barcos(
            jugadores[1]["tablero"],
            jugadores[1]["posiciones_barcos"],
            tamaño
        )

        print("La IA ha disparado.")

        # Comprobar si la IA ha ganado
        if comprobar_victoria(
            jugadores[1]["tablero"],
            jugadores[1]["posiciones_barcos"]
        ):

            print("¡La IA ha ganado!")

            mostrar_victoria(
                ventana,
                2
            )

            return

        # Si impacta, la IA vuelve a disparar
        if impacto:

            cambiar_turno(
                ventana,
                jugadores,
                tamaño,
                1,
                numero_jugadores
            )

        # Si falla, vuelve el jugador
        else:

            mostrar_turno(
                ventana,
                jugadores,
                tamaño,
                1,
                numero_jugadores
            )

    # PARTIDA DE 2 JUGADORES
    else:

        limpiar_ventana(ventana)

        titulo = tk.Label(
            ventana,
            text=f"Turno del Jugador {siguiente_jugador}",
            font=("Arial", 24)
        )

        titulo.pack(pady=50)

        aviso = tk.Label(
            ventana,
            text="Pasa el ordenador al siguiente jugador",
            font=("Arial", 16)
        )

        aviso.pack(pady=20)

        boton = tk.Button(
            ventana,
            text="Comenzar Turno",
            font=("Arial", 14),
            command=lambda: mostrar_turno(
                ventana,
                jugadores,
                tamaño,
                siguiente_jugador,
                numero_jugadores
            )
        )

        boton.pack(pady=20)


def mostrar_turno(
    ventana,
    jugadores,
    tamaño,
    jugador_actual,
    numero_jugadores
):
    '''Construye la interfaz de combate del jugador activo, usando mostrar_tablero_combate():
    - Enseña su tablero, con sus posiciones y los disparos del rival y sus consecuencias.
    - Enseña el tablero enemigo, con los disparos previos marcados, y enseñando sus consecuencias, pero no los barcos enemigos no encontrados.'''
    limpiar_ventana(ventana)

    titulo = tk.Label(
        ventana,
        text=f"Turno del Jugador {jugador_actual}",
        font=("Arial", 20)
    )

    titulo.pack(pady=10)

    frame_juego = tk.Frame(ventana)
    frame_juego.pack(pady=10)

    frame_propio = tk.Frame(frame_juego)
    frame_propio.grid(
        row=0,
        column=0,
        padx=30
    )

    frame_enemigo = tk.Frame(frame_juego)
    frame_enemigo.grid(
        row=0,
        column=1,
        padx=30
    )

    tk.Label(
        frame_propio,
        text="Tu tablero",
        font=("Arial", 16)
    ).grid(
        row=0,
        column=0,
        columnspan=tamaño + 1,
        pady=10
    )

    tk.Label(
        frame_enemigo,
        text="Tablero enemigo",
        font=("Arial", 16)
    ).grid(
        row=0,
        column=0,
        columnspan=tamaño + 1,
        pady=10
    )

    enemigo = 2 if jugador_actual == 1 else 1

    mostrar_tablero_combate(
        frame_propio,
        jugadores[jugador_actual]["tablero"],
        tamaño,
        False,
        jugadores[jugador_actual]["posiciones_barcos"],
        jugador_actual,
        ventana,
        jugadores,
        numero_jugadores
    )

    mostrar_tablero_combate(
        frame_enemigo,
        jugadores[enemigo]["tablero"],
        tamaño,
        True,
        jugadores[enemigo]["posiciones_barcos"],
        jugador_actual,
        ventana,
        jugadores,
        numero_jugadores
    )


def mostrar_tablero_combate(
    frame,
    tablero,
    tamaño,
    enemigo,
    posiciones_barcos,
    jugador_actual,
    ventana,
    jugadores,
    numero_jugadores
):
    '''Dibuja el tablero durante el combate y muestra la información permitida según sea propio o enemigo.'''
    botones = {}

    for columna in range(tamaño):

        letra = chr(65 + columna)

        tk.Label(
            frame,
            text=letra,
            font=("Arial", 12, "bold"),
            width=3
        ).grid(
            row=1,
            column=columna + 1
        )

    for fila in range(tamaño):

        tk.Label(
            frame,
            text=fila + 1,
            font=("Arial", 12, "bold"),
            width=3
        ).grid(
            row=fila + 2,
            column=0
        )

        for columna in range(tamaño):

            boton = tk.Button(
                frame,
                text="≈",
                width=2,
                height=1,
                bg="white",
                fg="blue"
            )

            botones[(fila, columna)] = boton

            if enemigo:

                if tablero[fila][columna] == 2:

                    boton.config(
                        text="·",
                        state="disabled",
                        bg="white",
                        disabledforeground="black"
                    )

                elif tablero[fila][columna] == 3:

                    boton.config(
                        text="X",
                        state="disabled",
                        bg="white",
                        disabledforeground="red"
                    )

                elif tablero[fila][columna] == 4:

                    boton.config(
                        text="☠",
                        state="disabled",
                        bg="white",
                        disabledforeground="red"
                    )

                else:

                    boton.config(
                        command=lambda f=fila, c=columna, b=boton:
                        disparar_gui(
                            f,
                            c,
                            tablero,
                            b,
                            posiciones_barcos,
                            botones,
                            jugador_actual,
                            ventana,
                            jugadores,
                            tamaño,
                            numero_jugadores
                        )
                    )

            else:

                if tablero[fila][columna] == 1:

                    boton.config(
                        text="■",
                        bg="white",
                        fg="black"
                    )

                elif tablero[fila][columna] == 3:

                    boton.config(
                        text="X",
                        bg="white",
                        fg="red"
                    )

                elif tablero[fila][columna] == 4:

                    boton.config(
                        text="☠",
                        bg="white",
                        fg="red"
                    )

                elif tablero[fila][columna] == 2:

                    boton.config(
                        text="·",
                        bg="white",
                        fg="red"
                    )

            boton.grid(
                row=fila + 2,
                column=columna + 1,
                padx=0,
                pady=0
            )


def disparar_gui(
    fila,
    columna,
    tablero,
    boton,
    posiciones_barcos,
    botones,
    jugador_actual,
    ventana,
    jugadores,
    tamaño,
    numero_jugadores
):
    '''Gestiona el disparo y sus consecuencias'''
    print("Disparo en:", fila, columna)

    if tablero[fila][columna] == 1:

        print("¡Impacto!")

        tablero[fila][columna] = 3

        boton.config(
            text="X",
            state="disabled",
            bg="white",
            fg="red"
        )

        barco = com_barco(
            fila,
            columna,
            posiciones_barcos
        )

        print("Has alcanzado:", barco)

        if com_hundido(
            tablero,
            barco,
            posiciones_barcos
        ):

            print("Has hundido:", barco)

            for fil, col in posiciones_barcos[barco]:

                tablero[fil][col] = 4

                botones[(fil, col)].config(
                    text="☠",
                    state="disabled",
                    bg="white",
                    fg="red"
                )

            if comprobar_victoria(
                tablero,
                posiciones_barcos
            ):

                print(
                    "¡El jugador",
                    jugador_actual,
                    "ha ganado!"
                )

                mostrar_victoria(
                    ventana,
                    jugador_actual
                )

                return

        # Si impacta, mantiene el turno.
        return

    else:

        print("¡Agua!")

        tablero[fila][columna] = 2

        boton.config(
            text="·",
            state="disabled"
        )

        cambiar_turno(
            ventana,
            jugadores,
            tamaño,
            jugador_actual,
            numero_jugadores
        )


def comprobar_victoria(tablero, posiciones_barcos):
    '''Compueba si al hundir un barco, el jugador gana o no'''
    for posiciones in posiciones_barcos.values():

        for fila, columna in posiciones:

            if tablero[fila][columna] != 4:
                return False

    return True


def mostrar_victoria(ventana,jugador):
    '''Si el jugador Gana, enseña la ventana de victoria:
    - Permite al jugador elegir si quiere volver a jugar y cómo.'''
    limpiar_ventana(ventana)

    if jugador == 2:

        titulo = tk.Label(
            ventana,
            text="¡La IA ha ganado!",
            font=("Arial", 28)
        )

    else:

        titulo = tk.Label(
            ventana,
            text=f"¡Jugador {jugador} ha ganado!",
            font=("Arial", 28)
        )

    titulo.pack(pady=80)

    texto = tk.Label(
        ventana,
        text="¡Enhorabuena!",
        font=("Arial", 18)
    )

    texto.pack(pady=20)

    boton_rejugar = tk.Button(
        ventana,
        text="Volver a jugar",
        font=("Arial", 16),
        command=lambda: mostrar_menu(ventana)
    )
    boton_rejugar.pack(pady=20)


