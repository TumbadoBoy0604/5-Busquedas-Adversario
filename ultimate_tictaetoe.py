from juegos_simplificado import ModeloJuegoZT2, juega_dos_jugadores
from minimax import jugador_negamax, minimax_iterativo
from random import shuffle
import time

class UltimateTicTacToe(ModeloJuegoZT2):
    """
    Implementación del juego Ultimate TicTacToe.
    
    El estado se representa como:
    (tableros, tablero_actual, ultimo_movimiento)
    
    Donde:
    - tableros: Tupla de 9 tableros pequeños, cada uno representado 
      por una tupla de 9 elementos (0 para vacío, 1 para X, -1 para O)
    - tablero_actual: Índice del tablero en el que se debe jugar (-1 si se puede elegir cualquiera)
    - ultimo_movimiento: Tupla (tablero, posición) del último movimiento realizado
    """
    
    def inicializa(self):
        """Inicializa el juego con tableros vacíos"""
        tableros = tuple(tuple([0] * 9) for _ in range(9))
        tablero_actual = -1  
        ultimo_movimiento = None
        return ((tableros, tablero_actual, ultimo_movimiento), 1)
    
    def jugadas_legales(self, s, j):
        """
        Devuelve las jugadas legales para el jugador j en el estado s.
        Cada jugada es una tupla (tablero, posicion).
        """
        tableros, tablero_actual, _ = s
        
        jugadas = []
        
        # Si hay que jugar en un tablero específico y es válido
        if tablero_actual != -1:
            tablero = tableros[tablero_actual]
            # Si el tablero está completo o ya tiene ganador, se puede jugar en cualquier tablero
            if self._tablero_lleno(tablero) or self._hay_ganador(tablero):
                tablero_actual = -1
            else:
                # Añadir posiciones libres en este tablero
                for pos in range(9):
                    if tablero[pos] == 0:
                        jugadas.append((tablero_actual, pos))
                return jugadas
        
        # Si se puede jugar en cualquier tablero
        if tablero_actual == -1:
            for tb in range(9):
                tablero = tableros[tb]
                # Solo considerar tableros que no están completos y no tienen ganador
                if not self._tablero_lleno(tablero) and not self._hay_ganador(tablero):
                    for pos in range(9):
                        if tablero[pos] == 0:
                            jugadas.append((tb, pos))
        
        return jugadas
    
    def transicion(self, s, a, j):
        """
        Realiza una jugada y devuelve el nuevo estado.
        a es una tupla (tablero, posicion)
        """
        tableros, _, _ = s
        tablero_idx, pos = a
        
        # Crear copia de los tableros
        tableros_nuevos = list(tableros)
        for i in range(9):
            if i == tablero_idx:
                # Actualizar el tablero donde se realizó la jugada
                tablero = list(tableros[i])
                tablero[pos] = j
                tableros_nuevos[i] = tuple(tablero)
            else:
                tableros_nuevos[i] = tableros[i]
        
        # El próximo tablero es el correspondiente a la posición jugada
        proximo_tablero = pos
        if (self._tablero_lleno(tableros_nuevos[proximo_tablero]) or 
            self._hay_ganador(tableros_nuevos[proximo_tablero])):
            proximo_tablero = -1
        
        return (tuple(tableros_nuevos), proximo_tablero, (tablero_idx, pos))
    
    def terminal(self, s):
        """Determina si el estado es terminal"""
        tableros, _, _ = s
        
        # Verificar si hay ganador en el meta-tablero
        if self._hay_ganador_global(tableros):
            return True
        
        # Verificar si todos los tableros están completos o tienen ganador
        tableros_disponibles = 0
        for tablero in tableros:
            if not self._tablero_lleno(tablero) and not self._hay_ganador(tablero):
                tableros_disponibles += 1
        
        return tableros_disponibles == 0
    
    def ganancia(self, s):
        """Determina la ganancia para el jugador 1 en el estado terminal s"""
        tableros, _, _ = s
        
        # Obtener el meta-tablero (resultados de cada tablero pequeño)
        meta_tablero = self._obtener_meta_tablero(tableros)
        
        # Verificar ganador en el meta-tablero
        for linea in self._lineas_ganadoras():
            if (meta_tablero[linea[0]] == meta_tablero[linea[1]] == meta_tablero[linea[2]] != 0):
                return meta_tablero[linea[0]]
        
        return 0  # Empate
    
    def _tablero_lleno(self, tablero):
        """Verifica si un tablero está lleno"""
        return 0 not in tablero
    
    def _hay_ganador(self, tablero):
        """Determina si hay un ganador en un tablero pequeño"""
        for linea in self._lineas_ganadoras():
            if (tablero[linea[0]] == tablero[linea[1]] == tablero[linea[2]] != 0):
                return True
        return False
    
    def _obtener_ganador_tablero(self, tablero):
        """Obtiene el ganador de un tablero pequeño (0 si no hay ganador)"""
        for linea in self._lineas_ganadoras():
            if (tablero[linea[0]] == tablero[linea[1]] == tablero[linea[2]] != 0):
                return tablero[linea[0]]
        return 0
    
    def _obtener_meta_tablero(self, tableros):
        """
        Convierte los 9 tableros pequeños en un meta-tablero 
        donde cada posición indica el ganador de cada tablero pequeño
        """
        meta_tablero = [0] * 9
        for i, tablero in enumerate(tableros):
            meta_tablero[i] = self._obtener_ganador_tablero(tablero)
        return meta_tablero
    
    def _hay_ganador_global(self, tableros):
        """Determina si hay un ganador en el meta-tablero"""
        meta_tablero = self._obtener_meta_tablero(tableros)
        for linea in self._lineas_ganadoras():
            if (meta_tablero[linea[0]] == meta_tablero[linea[1]] == meta_tablero[linea[2]] != 0):
                return True
        return False
    
    def _lineas_ganadoras(self):
        """Devuelve todas las líneas ganadoras posibles (filas, columnas, diagonales)"""
        return [
            # Filas
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            # Columnas
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            # Diagonales
            (0, 4, 8), (2, 4, 6)
        ]


# Funciones para visualizar el tablero

def pprint_ultimate_tictactoe(s):
    """Imprime el estado del juego Ultimate TicTacToe"""
    tableros, tablero_actual, ultimo_movimiento = s
    
    simbolos = {0: ' ', 1: 'X', -1: 'O'}
    
    print("\n" + "="*31)
    
    for fila_tableros in range(3):
        # Imprimir 3 filas de cada tablero en esta fila de tableros
        for fila_celdas in range(3):
            for tb_col in range(3):
                tb_idx = fila_tableros * 3 + tb_col
                
                # Destacar el tablero actual donde se debe jugar
                if tb_idx == tablero_actual:
                    print("!", end="")
                else:
                    print(" ", end="")
                
                # Imprimir celdas de este tablero para esta fila
                for cel_col in range(3):
                    pos = fila_celdas * 3 + cel_col
                    celda = tableros[tb_idx][pos]
                    
                    # Destacar la última jugada
                    if ultimo_movimiento and ultimo_movimiento == (tb_idx, pos):
                        print("[" + simbolos[celda] + "]", end="")
                    else:
                        print(" " + simbolos[celda] + " ", end="")
                
                # Separador entre tableros
                if tb_col < 2:
                    print(" |", end="")
            
            print()  # Nueva línea después de cada fila de celdas
        
        # Separador entre filas de tableros
        if fila_tableros < 2:
            print("-" * 31)
    
    print("="*31)
    
    # Mostrar meta-tablero (estado global del juego)
    meta_tablero = [" "] * 9
    for i, tablero in enumerate(tableros):
        ganador = UltimateTicTacToe()._obtener_ganador_tablero(tablero)
        meta_tablero[i] = simbolos[ganador]
    
    print("\nEstado global:")
    print(" {} | {} | {} ".format(meta_tablero[0], meta_tablero[1], meta_tablero[2]))
    print("---+---+---")
    print(" {} | {} | {} ".format(meta_tablero[3], meta_tablero[4], meta_tablero[5]))
    print("---+---+---")
    print(" {} | {} | {} ".format(meta_tablero[6], meta_tablero[7], meta_tablero[8]))


def jugador_manual_gui(gui):
    """Agente para recibir jugada desde la GUI."""
    def pedir_jugada(juego, estado, jugador):
        jugadas = list(juego.jugadas_legales(estado, jugador))

        gui.jugada_usuario = None
        gui.esperando_jugada = True

        def on_click(jugada):
            gui.esperando_jugada = False
            gui.callback_jugada = None
            gui.root.quit()

        gui.callback_jugada = on_click
        gui.root.mainloop()
        return gui.jugada_usuario

    return pedir_jugada


def jugador_manual_ultimate_tictactoe(juego, s, j):
    """Interfaz para que un humano juegue"""
    pprint_ultimate_tictactoe(s)
    print("\nJugador " + ("X" if j == 1 else "O"))
    
    tableros, tablero_actual, _ = s
    
    # Mostrar tablero donde debe jugar
    if tablero_actual != -1:
        print(f"Debes jugar en el tablero {tablero_actual + 1}")
    else:
        print("Puedes jugar en cualquier tablero")
    
    jugadas = list(juego.jugadas_legales(s, j))
    
    # Mostrar jugadas disponibles numeradas
    print("\nJugadas disponibles:")
    for i, (tablero, pos) in enumerate(jugadas):
        fila, col = pos // 3, pos % 3
        print(f"{i+1}. Tablero {tablero + 1}, posición ({fila + 1},{col + 1})")
    
    # Solicitar jugada
    seleccion = -1
    while seleccion < 0 or seleccion >= len(jugadas):
        try:
            seleccion = int(input("\nElige una jugada (1-{}): ".format(len(jugadas)))) - 1
        except ValueError:
            print("Por favor, introduce un número válido.")
    
    return jugadas[seleccion]


# Funciones de ordenamiento

# Modificar la función ordena_centro_ultimate para aceptar un segundo parámetro (jugador)
def ordena_centro_ultimate(jugadas, jugador=None):
    """
    Ordena las jugadas priorizando:
    1. Las posiciones centrales de los tableros
    2. Los tableros centrales
    
    El parámetro jugador es ignorado pero necesario para compatibilidad.
    """
    def valor_posicion(pos):
        # Valores según posición: centro > esquinas > bordes
        valores = {
            4: 3,  # Centro
            0: 2, 2: 2, 6: 2, 8: 2,  # Esquinas
            1: 1, 3: 1, 5: 1, 7: 1   # Bordes
        }
        return valores.get(pos, 0)
    
    def valor_tablero(tablero):
        # Valores según posición del tablero: centro > esquinas > bordes
        valores = {
            4: 3,  # Centro
            0: 2, 2: 2, 6: 2, 8: 2,  # Esquinas
            1: 1, 3: 1, 5: 1, 7: 1   # Bordes
        }
        return valores.get(tablero, 0)
    
    # Ordenar por valor combinado (posición + tablero)
    return sorted(
        jugadas,
        key=lambda jugada: (valor_posicion(jugada[1]) + valor_tablero(jugada[0])),
        reverse=True
    )
def ordena_estrategico_ultimate(jugadas, juego, s, j):
    """
    Ordenamiento estratégico que prioriza:
    1. Jugadas que llevan a ganar un tablero
    2. Jugadas que bloquean victorias en tableros
    3. Jugadas que envían al oponente a tableros ya ganados/completos
    4. Jugadas en posiciones estratégicas
    """
    if juego is None:

        juego = UltimateTicTacToe()
    if s is None:

        global _estado_actual

        s = _estado_actual
    if j is None:

        j = 1
    if s is None:

        # Si no hay estado, usar ordenamiento básico

        return ordena_centro_ultimate(jugadas)
    tableros, _, _ = s
    valoraciones = []
    
    for jugada in jugadas:
        tablero_idx, pos = jugada
        
        # Hacer una copia del tablero para simular
        tablero_original = tableros[tablero_idx]
        tablero_simulado = list(tablero_original)
        tablero_simulado[pos] = j
        tablero_simulado = tuple(tablero_simulado)
        
        valor = 0
        
        # 1. Valor base según posición dentro del tablero
        if pos == 4:  # Centro
            valor += 3
        elif pos in (0, 2, 6, 8):  # Esquinas
            valor += 2
        else:  # Bordes
            valor += 1
        
        # 2. Valor base según posición del tablero en el meta-tablero
        if tablero_idx == 4:  # Tablero central
            valor += 3
        elif tablero_idx in (0, 2, 6, 8):  # Tableros de esquina
            valor += 2
        else:  # Tableros de borde
            valor += 1
        
        # 3. Verificar si esta jugada gana el tablero
        if not juego._hay_ganador(tablero_original):
            lineas = juego._lineas_ganadoras()
            for linea in lineas:
                if pos in linea:
                    # Comprobar si completamos una línea
                    if (all(tablero_simulado[p] == j for p in linea)):
                        valor += 100  # Alta prioridad para ganar tablero
        
        # 4. Verificar si esta jugada bloquea al oponente
        oponente = -j
        for linea in juego._lineas_ganadoras():
            if pos in linea:
                # Contar fichas del oponente en esta línea
                fichas_oponente = sum(1 for p in linea if tablero_original[p] == oponente)
                # Si el oponente tiene 2 fichas y bloqueamos la tercera
                if fichas_oponente == 2 and all(tablero_original[p] != j for p in linea if p != pos):
                    valor += 50  # Prioridad para bloquear
        
        # 5. Verificar si envía al oponente a un tablero favorable para nosotros
        siguiente_tablero = pos
        if siguiente_tablero < 9:  # Asegurarse que es un tablero válido
            # Si el siguiente tablero ya tiene ganador o está lleno
            if (juego._hay_ganador(tableros[siguiente_tablero]) or 
                juego._tablero_lleno(tableros[siguiente_tablero])):
                valor += 20  # Buena estrategia enviar a un tablero ya resuelto
            elif siguiente_tablero == 4:  # Evitar enviar al centro si está libre
                valor -= 15
        
        valoraciones.append((jugada, valor))
    
    # Ordenar por valor (mayor primero)
    valoraciones.sort(key=lambda x: x[1], reverse=True)
    return [v[0] for v in valoraciones]


# Funciones de evaluación

def evalua_simple_ultimate(s, j=None):
    """
    Evaluación simple basada en tableros ganados.
    Retorna un valor entre -1 y 1.
    
    Si j no se proporciona, asume la perspectiva del jugador 1.
    """
    juego = UltimateTicTacToe()
    tableros, _, _ = s
    
    # Si no se proporciona j, usar 1 (jugador por defecto)
    if j is None:
        j = 1
    
    # Si es un estado terminal, retorna el valor exacto
    if juego.terminal(s):
        return juego.ganancia(s) * j  # Multiplicar por j para perspectiva del jugador actual
    
    # Obtener el meta-tablero
    meta_tablero = juego._obtener_meta_tablero(tableros)
    
    # Contar tableros ganados por cada jugador
    tableros_j = meta_tablero.count(j)
    tableros_oponente = meta_tablero.count(-j)
    
    # Diferencia normalizada entre -1 y 1
    return (tableros_j - tableros_oponente) / 9

def evalua_avanzada_ultimate(s, j=None):
    """
    Evaluación avanzada que considera múltiples factores estratégicos.
    El parámetro j indica la perspectiva del jugador (1 o -1).
    Si j es None, usa el jugador actual del estado.
    """
    juego = UltimateTicTacToe()
    tableros, tablero_actual, _ = s
    
    # Si j es None, determinar el jugador actual
    # Para una llamada desde negamax, siempre evaluamos desde la perspectiva del jugador 1
    if j is None:
        j = 1
    
    # El resto de la implementación continúa igual...
    # Si es un estado terminal, retorna el valor exacto
    if juego.terminal(s):
        ganancia = juego.ganancia(s)
        # Convertir a perspectiva del jugador actual
        return ganancia * j
    
    # Obtener meta-tablero
    meta_tablero = juego._obtener_meta_tablero(tableros)
    
    # 1. Valor base por tableros ganados (mayor peso)
    tableros_j = meta_tablero.count(j)
    tableros_oponente = meta_tablero.count(-j)
    valor_tableros = (tableros_j - tableros_oponente) / 9 * 0.5  # Normalizado * peso
    
    # 2. Valor por líneas potenciales en el meta-tablero
    valor_lineas = 0
    for linea in juego._lineas_ganadoras():
        # Contar fichas propias y del oponente en esta línea del meta-tablero
        fichas_propias = sum(1 for pos in linea if meta_tablero[pos] == j)
        fichas_oponente = sum(1 for pos in linea if meta_tablero[pos] == -j)
        
        # Linea propia con potencial (no bloqueada por oponente)
        if fichas_propias > 0 and fichas_oponente == 0:
            valor_lineas += fichas_propias * 0.1
        
        # Linea del oponente con potencial (restar)
        if fichas_oponente > 0 and fichas_propias == 0:
            valor_lineas -= fichas_oponente * 0.1
    
    # 3. Control de posiciones estratégicas (centro y esquinas)
    valor_estrategico = 0
    posiciones_clave = {
        4: 0.1,       # Centro (mayor valor)
        0: 0.05, 2: 0.05, 6: 0.05, 8: 0.05  # Esquinas
    }
    
    for pos, valor in posiciones_clave.items():
        if meta_tablero[pos] == j:
            valor_estrategico += valor
        elif meta_tablero[pos] == -j:
            valor_estrategico -= valor
    
    # 4. Evaluar tableros individuales para detectar ventajas tácticas
    valor_tactico = 0
    for idx, tablero in enumerate(tableros):
        # Si el tablero no está ganado todavía
        if meta_tablero[idx] == 0 and not juego._tablero_lleno(tablero):
            # Ventaja posicional: piezas propias vs oponente
            piezas_j = tablero.count(j)
            piezas_oponente = tablero.count(-j)
            
            # Más valor a tableros estratégicos
            multiplicador = 1.0
            if idx == 4:  # Centro
                multiplicador = 1.5
            elif idx in (0, 2, 6, 8):  # Esquinas
                multiplicador = 1.2
                
            ventaja_tablero = (piezas_j - piezas_oponente) / 9 * 0.05 * multiplicador
            valor_tactico += ventaja_tablero
            
            # Detectar amenazas de victoria en cada tablero
            for linea in juego._lineas_ganadoras():
                # Contar piezas propias y vacías en esta línea
                propias_linea = sum(1 for pos in linea if tablero[pos] == j)
                vacias_linea = sum(1 for pos in linea if tablero[pos] == 0)
                
                # Amenaza de victoria (2 propias y 1 vacía)
                if propias_linea == 2 and vacias_linea == 1:
                    valor_tactico += 0.1
                
                # Bloqueo potencial de victoria del oponente
                oponente_linea = sum(1 for pos in linea if tablero[pos] == -j)
                if oponente_linea == 2 and vacias_linea == 1:
                    valor_tactico -= 0.08  # Penalizar menos que el beneficio de ganar
    
    # 5. Ventaja de movimiento (si el siguiente tablero nos da ventaja)
    valor_movimiento = 0
    if tablero_actual != -1:
        # Si nos toca jugar en un tablero específico, evaluar si es favorable
        if juego._hay_ganador(tableros[tablero_actual]) or juego._tablero_lleno(tableros[tablero_actual]):
            # Si es un tablero ya resuelto, es ventajoso para el oponente (puede elegir)
            valor_movimiento -= 0.05
        elif tablero_actual == 4:  # Centro
            # Jugar en el centro es generalmente ventajoso
            valor_movimiento += 0.05
    
    # Combinar todos los factores (con diferentes pesos para equilibrar)
    valor_final = (
        valor_tableros * 0.4 +    # Más peso a tableros ganados
        valor_lineas * 0.25 +     
        valor_estrategico * 0.15 +
        valor_tactico * 0.15 +
        valor_movimiento * 0.05   # Menor peso a la ventaja de movimiento
    )
    
    # Asegurar que el valor está en el rango [-1, 1]
    return max(min(valor_final, 0.99), -0.99)


# Variable global para almacenar el estado actual (para función de ordenamiento)
_estado_actual = None

def set_estado_actual(estado):
    """Función auxiliar para establecer el estado global"""
    global _estado_actual
    _estado_actual = estado


def ordena_con_estado_actual(jugadas, j=None):
    """
    Función de ordenamiento que utiliza el estado global actual.
    Compatible con la API de minimax y negamax.
    """
    global _estado_actual
    
    if j is None:
        j = 1
    
    if _estado_actual is None:
        # Si no hay estado actual, usar ordenamiento básico
        return ordena_centro_ultimate(jugadas)
    
    # Usar ordenamiento estratégico con el estado actual
    return ordena_estrategico_ultimate(jugadas, UltimateTicTacToe(), _estado_actual, j)


def negamax_con_estado_actual(juego, s, j, d):
    """Wrapper para jugador_negamax que incluye el estado actual"""
    set_estado_actual(s)  # Establecer el estado global
    return jugador_negamax(juego, s, j, ordena=ordena_con_estado_actual, evalua=evalua_avanzada_ultimate, d=d)


def minimax_iter_con_estado_actual(juego, s, j, tiempo):
    """Wrapper para minimax_iterativo que incluye el estado actual"""
    set_estado_actual(s)  # Establecer el estado global
    return minimax_iterativo(juego, s, j, ordena=ordena_con_estado_actual, evalua=evalua_avanzada_ultimate, tiempo=tiempo)


# Script principal para jugar

if __name__ == '__main__':
    modelo = UltimateTicTacToe()
    print("="*40 + "\n" + "ULTIMATE TIC-TAC-TOE".center(40) + "\n" + "="*40)
    print("\nReglas:")
    print("- El tablero contiene 9 tableros pequeños de Tic-Tac-Toe")
    print("- El movimiento en un tablero pequeño determina en qué tablero jugará el siguiente jugador")
    print("- Para ganar, consigue 3 tableros pequeños en línea")
    print("- Si te envían a un tablero ya ganado o lleno, podrás elegir cualquier tablero")
    print("\nSimbología:")
    print("- X: Jugador 1, O: Jugador 2")
    print("- [X] o [O]: Último movimiento realizado")
    print("- !: Indica el tablero donde toca jugar")
    print("\nVamos a jugar!\n")
    
    jugs = []
    for j in [1, -1]:
        print(f"Selección de jugadores para las {' XO'[j]}:")
        sel = 0
        print("   1. Jugador humano")
        print("   2. IA simple (prioriza centro, profundidad limitada)")
        print("   3. IA simple (prioriza centro, tiempo limitado)")
        print("   4. IA avanzada (estratégica, profundidad limitada)")
        print("   5. IA avanzada (estratégica, tiempo limitado)")
        
        while sel not in [1, 2, 3, 4, 5]:
            try:
                sel = int(input(f"Jugador para las {' XO'[j]}: "))
            except ValueError:
                print("Por favor, introduce un número válido.")
    
        if sel == 1:
            jugs.append(jugador_manual_ultimate_tictactoe)
        elif sel == 2:
            d = None
            while not isinstance(d, int) or d < 1:
                try:
                    d = int(input("Profundidad (recomendado 2-4): "))
                except ValueError:
                    print("Por favor, introduce un número entero positivo.")
            jugs.append(lambda juego, s, j: jugador_negamax(
                juego, s, j, ordena=ordena_centro_ultimate, evalua=evalua_simple_ultimate, d=d)
            )
        elif sel == 3:
            t = None
            while not isinstance(t, int) or t < 1:
                try:
                    t = int(input("Tiempo en segundos: "))
                except ValueError:
                    print("Por favor, introduce un número entero positivo.")
            jugs.append(lambda juego, s, j: minimax_iterativo(
                juego, s, j, ordena=ordena_centro_ultimate, evalua=evalua_simple_ultimate, tiempo=t)
            )
        elif sel == 4:
            d = None
            while not isinstance(d, int) or d < 1:
                try:
                    d = int(input("Profundidad (recomendado 2-4): "))
                except ValueError:
                    print("Por favor, introduce un número entero positivo.")
            jugs.append(lambda juego, s, j: negamax_con_estado_actual(juego, s, j, d))
        else:  # sel == 5
            t = None
            while not isinstance(t, int) or t < 1:
                try:
                    t = int(input("Tiempo en segundos: "))
                except ValueError:
                    print("Por favor, introduce un número entero positivo.")
            jugs.append(lambda juego, s, j: minimax_iter_con_estado_actual(juego, s, j, t))
    
    # Jugar la partida
    print("\n¡Comienza el juego!\n")
    g, s_final = juega_dos_jugadores(modelo, jugs[0], jugs[1])
    
    # Mostrar resultado final
    print("\nFIN DEL JUEGO\n")
    pprint_ultimate_tictactoe(s_final)
    
    if g != 0:
        print("\n¡Gana el jugador " + " XO"[g] + "!")
    else:
        print("\n¡Empate!")
