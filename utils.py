import constants as c
import numpy as np
import pandas as pd

class Tablero:
    barcos = c.BARCOS
    tamanyo = c.T_TABLERO

    def __init__(self):
        pass
    
    def iniciar_tableros(self):
        # Creamos los tableros de los jugadores
        jugador_1 = np.full((self.tamanyo,self.tamanyo), '()')
        jugador_2 = np.full((self.tamanyo,self.tamanyo), '()')
        jugadores = [jugador_1,jugador_2]
        tableros = []

        # Por cada jugador
        for x in jugadores:
            #Por cada barco
            for v in self.barcos.values():
                # Por la cantidad de cada tipo de barcos
                for _ in range(v.get('cantidad')):

                    while True:
                        # posicion inicial del barco
                        pos_inicial_x = int(np.random.randint(10, size=1, dtype=np.int64))
                        pos_inicial_y = int(np.random.randint(10, size=1, dtype=np.int64))

                        # generar de forma aleatoria la orientacion
                        lista_dir = np.array(['N','S','E','O'])
                        orientacion = np.random.choice(lista_dir)

                        # Calculamos las posiciones hasta de los barcos
                        pos_hasta_n = int(np.subtract(pos_inicial_x, v.get('espacios')))
                        pos_hasta_s = int(np.sum([pos_inicial_x, v.get('espacios')]))
                        pos_hasta_e = int(np.sum([pos_inicial_y, v.get('espacios')]))
                        pos_hasta_o = int(np.subtract(pos_inicial_y, v.get('espacios')))

                        # comprobamos la orientacion
                        if orientacion == 'N':
                            # comprobamos que no supera los limites del tablero
                            if pos_hasta_n > 0:
                                pos_final = x[pos_hasta_n:pos_inicial_x,pos_inicial_y]
                                # comprobamos si esa posicion ya esta ocupada por un barco
                                if 'O' not in pos_final:
                                    x[pos_hasta_n:pos_inicial_x,pos_inicial_y] = 'O'
                                    break

                        elif orientacion == 'S':
                            if not(pos_hasta_s > 9):
                                pos_final = x[pos_inicial_x:pos_hasta_s,pos_inicial_y]
                            
                                if 'O' not in pos_final:
                                    x[pos_inicial_x:pos_hasta_s,pos_inicial_y] = 'O'
                                    break

                        elif orientacion == 'E':
                            if not(pos_hasta_e > 9):
                                pos_final = x[pos_inicial_x,pos_inicial_y:pos_hasta_e]

                                if 'O' not in pos_final:
                                    x[pos_inicial_x,pos_inicial_y:pos_hasta_e] = 'O'
                                    break

                        else:
                            if not(pos_hasta_o < 0):
                                pos_final = x[pos_inicial_x,pos_hasta_o:pos_inicial_y]
                                
                                if 'O' not in pos_final:
                                    x[pos_inicial_x,pos_hasta_o:pos_inicial_y] = 'O'
                                    break
            tableros.append(x)

        # Devolvemos los tableros con los barcos
        return tableros

    def comprobar_coordenadas(self,t_jugador,t_maquina,t_impactos_jugador,t_impactos_maquina,t):
        barco = 'O'
        disparo = 'X'
        agua = '-'

        # turno maquina
        if t == 1:
            coordenada_x = int(np.random.randint(10, size=1, dtype=np.int64))
            coordenada_y = int(np.random.randint(10, size=1, dtype=np.int64))

            # Si es una coordenada en la que ya ha disparado
            if all(i != 'X' or i != '-' for i in [t_impactos_maquina[coordenada_x,coordenada_y]]):
                
                # Si es un disparo
                if t_jugador[coordenada_x,coordenada_y] == barco:
                    t_jugador[coordenada_x,coordenada_y] = disparo
                    t_impactos_maquina[coordenada_x,coordenada_y] = disparo
                    
                    # Si es game over
                    if self.check_gameover(t_jugador) == 0:
                        self.imprimir_tableros(t_jugador,t_impactos_jugador)
                        self.comprobar_coordenadas(t_jugador,t_maquina,t_impactos_jugador,t_impactos_maquina,1)
                    else:
                        return 1
                # Si es agua
                else:
                    t_jugador[coordenada_x,coordenada_y] = agua
                    t_impactos_maquina[coordenada_x,coordenada_y] = agua
                    self.imprimir_tableros(t_jugador,t_impactos_jugador)
            else:
                self.comprobar_coordenadas(t_jugador,t_maquina,t_impactos_jugador,t_impactos_maquina,1)

        # turno jugador
        else:
            coordenada_x = input("Introduce la coordenada X")
            coordenada_y = input("Introduce la coordenada Y")

            try:
                # Intentamos pasar las coordenadadas a entero
                coordenada_x = int(coordenada_x)
                coordenada_y = int(coordenada_y)

                # Si esta entre 1 y 10
                if all(i > 0 and i < 11 for i in [coordenada_x,coordenada_y]):
                    coordenada_x -= 1
                    coordenada_y -= 1

                    # Si es un disparo
                    if t_maquina[coordenada_x,coordenada_y] == barco:
                        t_maquina[coordenada_x,coordenada_y] = disparo
                        t_impactos_jugador[coordenada_x,coordenada_y] = disparo

                        # Imprimos los tableros
                        self.imprimir_tableros(t_jugador,t_impactos_jugador)

                        #Comprobamos game over
                        if self.check_gameover(t_maquina) == 0:
                            self.comprobar_coordenadas(t_jugador,t_maquina,t_impactos_jugador,t_impactos_maquina,0)
                        else:
                            return 1

                    # Si es agua
                    else:
                        t_maquina[coordenada_x,coordenada_y] = agua
                        t_impactos_jugador[coordenada_x,coordenada_y] = agua
                        self.imprimir_tableros(t_jugador,t_impactos_jugador)
                else:
                    print("Debes introducir numeros entre el 1 y el 9")
                    self.comprobar_coordenadas(t_jugador,t_maquina,t_impactos_jugador,t_impactos_maquina,0)
            except:
                print("Debes introducir numeros")
                self.comprobar_coordenadas(t_jugador,t_maquina,t_impactos_jugador,t_impactos_maquina,0)
    
    # Imprimir tablero del jugador
    def imprimir_tableros(self,tablero_jugador,tablero_impactos):
        tablero_jugador = pd.DataFrame(tablero_jugador)
        tablero_impactos = pd.DataFrame(tablero_impactos)

        print("tablero jugador")
        print(tablero_jugador)
        print("tablero jugador impactos")
        print(tablero_impactos)

    # Comprobar game over
    def check_gameover(self,tablero):
        if 'O' in tablero:
            return 0
        else:
            return 1