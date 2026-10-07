import tkinter as tk
import numpy as np

from barcos import d_barcos, com_colocacion, col_barco, com_barco, com_hundido
from ai import ia_colocar_barcos, ia_dis_barcos


def limpiar_ventana(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()


def iniciar_interfaz():
    ventana = tk.Tk()

    ventana.title("Hundir la Flota")
    ventana.geometry("1200x800")
    ventana.resizable(False, False)

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
        command=lambda: seleccionar_jugadores(ventana, 1)
    )
    boton_1.pack(pady=10)

    boton_2 = tk.Button(
        ventana,
        text="2 Jugadores",
        command=lambda: seleccionar_jugadores(ventana, 2)
    )
    boton_2.pack(pady=10)

    ventana.mainloop()


def seleccionar_jugadores(ventana, numero):
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
        command=lambda: seleccionar_dificultad(ventana, numero, 8, 1)
    )
    facil.pack(pady=10)

    normal = tk.Button(
        ventana,
        text="Normal - 10x10",
        command=lambda: seleccionar_dificultad(ventana, numero, 10, 1)
    )
    normal.pack(pady=10)

    dificil = tk.Button(
        ventana,
        text="Difícil - 12x12",
        command=lambda: seleccionar_dificultad(ventana, numero, 12, 1)
    )
    dificil.pack(pady=10)


def seleccionar_dificultad(ventana, numero_jugadores, tamaño, jugador):
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
    botones = {}
    botones_barcos = {}
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

    barcos_posicion = {
        "Destructor": [],
        "Submarino": [],
        "Crucero": [],
        "Acorazado": [],
        "Portaaviones": []
    }

    jugadores[jugador]["tablero"] = tablero
    jugadores[jugador]["barcos_posicion"] = barcos_posicion

    mostrar_colocacion(
        ventana,
        tablero,
        barcos_disponibles,
        barcos_posicion,
        tamaño,
        barco_seleccionado,
        direccion_seleccionada,
        botones,
        botones_barcos,
        botones_direccion,
        numero_jugadores,
        jugador,
        jugadores
    )


def mostrar_colocacion(
    ventana,
    tablero,
    barcos_disponibles,
    barcos_posicion,
    tamaño,
    barco_seleccionado,
    direccion_seleccionada,
    botones,
    botones_barcos,
    botones_direccion,
    numero_jugadores,
    jugador,
    jugadores
):

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
                botones_barcos
            )
        )

        botones_barcos[barco] = boton

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
        barcos_posicion,
        tamaño,
        barco_seleccionado,
        direccion_seleccionada,
        botones,
        botones_barcos,
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


def seleccionar_barco(
    barco,
    barco_seleccionado,
    barcos_disponibles,
    botones_barcos
):

    for boton in botones_barcos.values():
        boton.config(relief="raised")

    botones_barcos[barco].config(
        relief="sunken"
    )

    barco_seleccionado[0] = barco

    print("Barco seleccionado:", barco)


def seleccionar_direccion(
    direccion,
    direccion_seleccionada,
    botones_direccion
):

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
    barcos_posicion,
    tamaño,
    barco_seleccionado,
    direccion_seleccionada,
    botones,
    botones_barcos,
    numero_jugadores,
    jugador,
    jugadores
):

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
                barcos_posicion,
                tamaño,
                barco_seleccionado,
                direccion_seleccionada,
                botones,
                botones_barcos,
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
    barcos_posicion,
    tamaño,
    barco_seleccionado,
    direccion_seleccionada,
    botones,
    botones_barcos,
    numero_jugadores,
    jugador,
    jugadores
):

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
            barcos_posicion,
            tamaño,
            barco_seleccionado,
            direccion_seleccionada,
            botones,
            botones_barcos,
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
    barcos_posicion,
    tamaño,
    barco_seleccionado,
    direccion_seleccionada,
    botones,
    botones_barcos,
    numero_jugadores,
    jugador,
    jugadores
):

    if barco_seleccionado[0] is None:
        print("Selecciona un barco.")
        return

    if direccion_seleccionada[0] is None:
        print("Selecciona una dirección.")
        return

    barco = barco_seleccionado[0]

    longitud = d_barcos[barco]

    posiciones_antiguas = barcos_posicion[barco]

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

    barcos_posicion[barco] = posiciones

    botones_barcos[barco].config(
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

        barcos_posicion_ia = {
            "Destructor": [],
            "Submarino": [],
            "Crucero": [],
            "Acorazado": [],
            "Portaaviones": []
        }

        ia_colocar_barcos(
            tablero_ia,
            barcos_disponibles_ia,
            barcos_posicion_ia,
            tamaño
        )

        jugadores[2]["tablero"] = tablero_ia

        jugadores[2]["barcos_posicion"] = barcos_posicion_ia

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

    siguiente_jugador = 2 if jugador_actual == 1 else 1

    # PARTIDA CONTRA IA
    if numero_jugadores == 1 and siguiente_jugador == 2:

        impacto = ia_dis_barcos(
            jugadores[1]["tablero"],
            jugadores[1]["barcos_posicion"],
            tamaño
        )

        print("La IA ha disparado.")

        # Comprobar si la IA ha ganado
        if comprobar_victoria(
            jugadores[1]["tablero"],
            jugadores[1]["barcos_posicion"]
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
        jugadores[jugador_actual]["barcos_posicion"],
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
        jugadores[enemigo]["barcos_posicion"],
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
    barcos_posicion,
    jugador_actual,
    ventana,
    jugadores,
    numero_jugadores
):

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
                            barcos_posicion,
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
    barcos_posicion,
    botones,
    jugador_actual,
    ventana,
    jugadores,
    tamaño,
    numero_jugadores
):

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
            barcos_posicion
        )

        print("Has alcanzado:", barco)

        if com_hundido(
            tablero,
            barco,
            barcos_posicion
        ):

            print("Has hundido:", barco)

            for fil, col in barcos_posicion[barco]:

                tablero[fil][col] = 4

                botones[(fil, col)].config(
                    text="☠",
                    state="disabled",
                    bg="white",
                    fg="red"
                )

            if comprobar_victoria(
                tablero,
                barcos_posicion
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


def comprobar_victoria(
    tablero,
    barcos_posicion
):

    for posiciones in barcos_posicion.values():

        for fila, columna in posiciones:

            if tablero[fila][columna] != 4:
                return False

    return True


def mostrar_victoria(
    ventana,
    jugador
):

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
