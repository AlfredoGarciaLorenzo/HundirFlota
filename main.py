import utils as u
import constants as c
import numpy as np
import colorama as color

mi_tablero = u.Tablero()
x = mi_tablero.iniciar_tableros()

tablero_jugador = x[0]
tablero_maquina = x[1]

tablero_impactos_jugador = np.full((10,10), '()')
tablero_impactos_maquina = np.full((10,10), '()')

print(c.MENSAJE)

while True:
    turno_jugador = mi_tablero.comprobar_coordenadas(tablero_jugador,tablero_maquina,tablero_impactos_jugador,tablero_impactos_maquina,0)

    # Si en algun momento devuelve un 1 significa que has ganado
    if turno_jugador == 1:
        print("¡Has ganado!")
        break

    turno_maquina = mi_tablero.comprobar_coordenadas(tablero_jugador,tablero_maquina,tablero_impactos_jugador,tablero_impactos_maquina,1)

    # Por el contrario si devuelve un 1 en el turno de la maquina gana la maquina
    if turno_maquina == 1:
        print("¡Has perdido!")
        break