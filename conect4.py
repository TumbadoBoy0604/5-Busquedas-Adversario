
"""
Juego de conecta 4

El estado se va a representar como una lista de 42 elementos, tal que


0  1  2  3  4  5  6
7  8  9 10 11 12 13
14 15 16 17 18 19 20
21 22 23 24 25 26 27
28 29 30 31 32 33 34
35 36 37 38 39 40 41

y cada elemento puede ser 0, 1 o -1, donde 0 es vacío, 1 es una ficha del
jugador 1 y -1 es una ficha del jugador 2.

Las acciones son poner una ficha en una columna, que se representa como un
número de 0 a 6.

Un estado terminal es aquel en el que un jugador ha conectado 4 fichas
horizontales, verticales o diagonales, o ya no hay espacios para colocar
fichas.

La ganancia es 1 si gana el jugador 1, -1 si gana el jugador 2 y 0 si es un
empate.

"""

from juegos_simplificado import ModeloJuegoZT2
from juegos_simplificado import juega_dos_jugadores
from minimax import jugador_negamax
from minimax import minimax_iterativo

class Conecta4(ModeloJuegoZT2):
    def inicializa(self):
        return (tuple([0 for _ in range(6 * 7)]), 1)
        
    def jugadas_legales(self, s, j):
        return (columna for columna in range(7) if s[columna] == 0)
    
    def transicion(self, s, a, j):
        s = list(s[:])
        for i in range(5, -1, -1):
            if s[a + 7 * i] == 0:
                s[a + 7 * i] = j
                break
        return tuple(s)
    
    def ganancia(self, s):
        #Verticales
        for i in range(7):
            for j in range(3):
                if (s[i + 7 * j] == s[i + 7 * (j + 1)] 
                    == s[i + 7 * (j + 2)] == s[i + 7 * (j + 3)] 
                    != 0):
                    return s[i + 7 * j]
        #Horizontales
        for i in range(6):
            for j in range(4):
                if (s[7 * i + j] == s[7 * i + j + 1] 
                    == s[7 * i + j + 2] == s[7 * i + j + 3] 
                    != 0):
                    return s[7 * i + j]
        #Diagonales
        for i in range(4):
            for j in range(3):
                if (s[i + 7 * j] == s[i + 7 * j + 8] 
                    == s[i + 7 * j + 16] == s[i + 7 * j + 24] 
                    != 0):
                    return s[i + 7 * j]
                if (s[i + 7 * j + 3] == s[i + 7 * j + 9] 
                    == s[i + 7 * j + 15] == s[i + 7 * j + 21] 
                    != 0):
                    return s[i + 7 * j + 3]
        return 0
    
    def terminal(self, s):
        if 0 not in s:
            return True
        return self.ganancia(s) != 0
    
def pprint_conecta4(s):
    a = [' X ' if x == 1 else ' O ' if x == -1 else '   ' 
         for x in s]
    print('\n 0 | 1 | 2 | 3 | 4 | 5 | 6')
    for i in range(6):
        print('|'.join(a[7 * i:7 * (i + 1)]))
        print('---+---+---+---+---+---+---')
    print('|'.join(a[42:49]))
    
def jugador_manual_conecta4(juego, s, j):
    pprint_conecta4(s)
    print("Jugador", " XO"[j])
    jugadas = list(juego.jugadas_legales(s, j))
    print("Jugadas legales:", jugadas)
    jugada = None
    while jugada not in jugadas:
        jugada = int(input("Jugada: "))
    return jugada



def ordena_centro(jugadas, jugador):
    """
    Ordena las jugadas de acuerdo a la distancia al centro
    """
    return sorted(jugadas, key=lambda x: abs(x - 4))

def evalua_3con(s):
    """
    Evalua el estado s para el jugador 1
    """
    conect3 = sum(
        1 for i in range(7) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * (j + 1)] 
            == s[i + 7 * (j + 2)] == 1)
    ) - sum(
        1 for i in range(7) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * (j + 1)] 
            == s[i + 7 * (j + 2)] == -1)
    ) + sum(
        1 for i in range(6) for j in range(5) 
        if (s[7 * i + j] == s[7 * i + j + 1] 
            == s[7 * i + j + 2] == 1)
    ) - sum(
        1 for i in range(6) for j in range(5) 
        if (s[7 * i + j] == s[7 * i + j + 1] 
            == s[7 * i + j + 2] == -1)
    ) + sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * j + 8] 
            == s[i + 7 * j + 16] == 1)
    ) - sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * j + 8] 
            == s[i + 7 * j + 16] == -1)
    ) + sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j + 3] == s[i + 7 * j + 9] 
            == s[i + 7 * j + 15] == 1)
    ) - sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j + 3] == s[i + 7 * j + 9] 
            == s[i + 7 * j + 15] == -1)
    )
    promedio = conect3 / (7 * 4 + 6 * 5 + 5 * 4 + 5 * 4)
    if abs(promedio) >= 1:
        print("ERROR, evaluación fuera de rango --> ", promedio)
    return promedio

def evalua3_avanzada(s):
    """
    Evaluación avanzada del tablero para el jugador 1.
    
    Considera múltiples factores estratégicos:
    1. Control del centro (posiciones centrales más valiosas)
    2. Amenazas (líneas con potencial de victoria)
    3. Patrones defensivos/ofensivos
    4. Piezas conectadas con espacio para ganar
    5. Bloqueos y estructuras defensivas
    """
    if not s:
        return 0
        
    # Si es un estado terminal, retornar el valor exacto
    juego = Conecta4()
    if juego.terminal(s):
        return juego.ganancia(s)
    
    # Factores de peso para diferentes componentes de evaluación
    PESO_CENTRO = 0.3
    PESO_CONECTADOS = 0.4
    PESO_AMENAZAS = 0.7
    PESO_DEFENSAS = 0.5
    
    # 1. Valorar control del centro
    valor_centro = 0
    # El centro de cada fila es más valioso (columnas 2,3,4)
    cols_centrales = [2, 3, 4]
    for fila in range(6):
        for col in cols_centrales:
            pos = fila * 7 + col
            if s[pos] == 1:  # Ficha del jugador 1
                # La columna central (3) tiene mayor valor
                valor_centro += 3 if col == 3 else 2
            elif s[pos] == -1:  # Ficha del jugador 2
                valor_centro -= 3 if col == 3 else 2
    
    # Normalizar valor del centro
    valor_centro = valor_centro / (6 * 3 * 3)  # max teórico: 6 filas * 3 columnas * valor máximo
    
    # 2. Evaluar piezas conectadas de diferentes longitudes
    conectados = {
        'j1_2': contar_conectados(s, 1, 2),
        'j1_3': contar_conectados(s, 1, 3),
        'j2_2': contar_conectados(s, -1, 2),
        'j2_3': contar_conectados(s, -1, 3)
    }
    
    # Valoramos más las conexiones de 3 que las de 2
    valor_conectados = (conectados['j1_2'] * 0.1 + conectados['j1_3'] * 0.4) - \
                       (conectados['j2_2'] * 0.1 + conectados['j2_3'] * 0.4)
    
    # Normalizar valor de conexiones (estimación de máximo)
    max_conectados = 20  # Número estimado máximo de conexiones posibles
    valor_conectados = valor_conectados / max_conectados
    
    # 3. Evaluar amenazas directas (jugadas que permiten ganar en el siguiente turno)
    amenazas_j1 = contar_amenazas_directas(s, 1)
    amenazas_j2 = contar_amenazas_directas(s, -1)
    
    valor_amenazas = (amenazas_j1 * 0.5) - (amenazas_j2 * 0.5)
    # Normalizar (máximo estimado de amenazas posibles)
    valor_amenazas = valor_amenazas / 7  # Máximo teórico: una amenaza por columna
    
    # 4. Evaluar estructuras defensivas y control de espacio
    valor_defensivo = evaluar_estructuras_defensivas(s)
    # Ya normalizado internamente
    
    # 5. Evaluación de movilidad (cuántos movimientos útiles tiene cada jugador)
    valor_movilidad = evaluar_movilidad(s)
    # Ya normalizado internamente
    
    # Combinar todos los factores con sus pesos
    evaluacion_total = (
        PESO_CENTRO * valor_centro +
        PESO_CONECTADOS * valor_conectados +
        PESO_AMENAZAS * valor_amenazas +
        PESO_DEFENSAS * valor_defensivo +
        0.2 * valor_movilidad  # Peso menor para movilidad
    )
    
    # Asegurar que está en el rango [-1, 1]
    evaluacion_total = max(min(evaluacion_total, 0.99), -0.99)
    
    return evaluacion_total

def contar_amenazas_directas(estado, jugador):
    """
    Cuenta cuántas amenazas directas tiene un jugador.
    Una amenaza directa es una posición donde al colocar una ficha se gana inmediatamente.
    """
    juego = Conecta4()
    amenazas = 0
    
    # Verificar cada columna
    for col in range(7):
        if estado[col] == 0:  # Si la columna no está llena
            # Simular colocar una ficha
            nuevo_estado = juego.transicion(estado, col, jugador)
            # Verificar si es un estado ganador
            if juego.terminal(nuevo_estado) and juego.ganancia(nuevo_estado) == jugador:
                amenazas += 1
    
    return amenazas

def evaluar_estructuras_defensivas(estado):
    """
    Evalúa estructuras defensivas como bloqueos y formaciones protectoras.
    Retorna un valor normalizado entre -1 y 1.
    """
    # Identificar bloqueos defensivos (fichas que bloquean victorias del oponente)
    bloqueos_j1 = 0
    bloqueos_j2 = 0
    
    # Revisar horizontales, verticales y diagonales para posibles bloqueos
    
    # Ejemplo: Buscar patrones del tipo "X O X" donde O bloquea a X
    for fila in range(6):
        for col in range(1, 6):  # Dejamos espacio para el patrón
            # Horizontal: revisar si hay un bloqueo en el centro
            if col > 0 and col < 6:
                # Patrón -1,1,-1 (O bloquea a X)
                if estado[fila*7 + col-1] == -1 and estado[fila*7 + col] == 1 and estado[fila*7 + col+1] == -1:
                    bloqueos_j1 += 1
                # Patrón 1,-1,1 (X bloquea a O)
                if estado[fila*7 + col-1] == 1 and estado[fila*7 + col] == -1 and estado[fila*7 + col+1] == 1:
                    bloqueos_j2 += 1
    
    # Patrones similares para verticales y diagonales (simplificado por brevedad)
    
    # Normalizar los bloqueos
    max_bloqueos = 20  # Estimación del máximo posible
    valor_bloqueos = (bloqueos_j1 - bloqueos_j2) / max_bloqueos
    
    # Considerar estructuras defensivas como "fortalezas" (configuraciones difíciles de atacar)
    # Simplificado por brevedad
    
    return max(min(valor_bloqueos, 1), -1)  # Normalizar entre -1 y 1

def evaluar_movilidad(estado):
    """
    Evalúa la movilidad de cada jugador (cuántos movimientos efectivos tiene disponibles).
    Retorna un valor normalizado entre -1 y 1.
    """
    # Contar columnas disponibles para cada jugador que no llevan a una pérdida inmediata
    juego = Conecta4()
    
    movilidad_j1 = 0
    movilidad_j2 = 0
    
    # Para el jugador 1
    for col in range(7):
        if estado[col] == 0:  # Columna disponible
            # Verificar que no lleva a una pérdida inmediata
            nuevo_estado = juego.transicion(estado, col, 1)
            if not juego.terminal(nuevo_estado) or juego.ganancia(nuevo_estado) != -1:
                movilidad_j1 += 1
    
    # Para el jugador 2
    for col in range(7):
        if estado[col] == 0:  # Columna disponible
            # Verificar que no lleva a una pérdida inmediata
            nuevo_estado = juego.transicion(estado, col, -1)
            if not juego.terminal(nuevo_estado) or juego.ganancia(nuevo_estado) != 1:
                movilidad_j2 += 1
    
    # Normalizar la diferencia de movilidad
    max_movilidad = 7  # Máximo posible (7 columnas)
    valor_movilidad = (movilidad_j1 - movilidad_j2) / max_movilidad
    
    return valor_movilidad



# Variable global para almacenar el estado actual del juego
_estado_actual = None

def set_estado_actual(estado):
    """Función auxiliar para establecer el estado actual"""
    global _estado_actual
    _estado_actual = estado

def contar_conectados(estado, jugador, n):
    """
    Cuenta cuántas líneas de 'n' fichas conectadas tiene el jugador
    con espacios para completar una línea de 4.
    """
    count = 0
    
    # Buscar horizontales
    for fila in range(6):
        for col in range(7-n+1):
            if all(estado[fila*7 + col+i] == jugador for i in range(n)):
                # Verificar si hay espacio para completar 4
                if n < 4:
                    espacios_libres = False
                    # Verificar espacios a la izquierda
                    if col > 0 and estado[fila*7 + col-1] == 0:
                        espacios_libres = True
                    # Verificar espacios a la derecha
                    if col+n < 7 and estado[fila*7 + col+n] == 0:
                        espacios_libres = True
                    
                    if espacios_libres:
                        count += 1
                else:
                    count += 1
    
    # Buscar verticales
    for col in range(7):
        for fila in range(6-n+1):
            if all(estado[(fila+i)*7 + col] == jugador for i in range(n)):
                # Para verticales, solo verificamos si hay espacio arriba
                if n < 4 and fila > 0 and estado[(fila-1)*7 + col] == 0:
                    count += 1
                elif n == 4:
                    count += 1
    
    # Buscar diagonales ascendentes
    for fila in range(n-1, 6):
        for col in range(7-n+1):
            if all(estado[(fila-i)*7 + col+i] == jugador for i in range(n)):
                if n < 4:
                    espacios_libres = False
                    # Verificar espacio abajo-izquierda
                    if col > 0 and fila < 5 and estado[(fila+1)*7 + col-1] == 0:
                        espacios_libres = True
                    # Verificar espacio arriba-derecha
                    if col+n < 7 and fila-(n) >= 0 and estado[(fila-(n))*7 + col+n] == 0:
                        espacios_libres = True
                    
                    if espacios_libres:
                        count += 1
                else:
                    count += 1
    
    # Buscar diagonales descendentes
    for fila in range(6-n+1):
        for col in range(7-n+1):
            if all(estado[(fila+i)*7 + col+i] == jugador for i in range(n)):
                if n < 4:
                    espacios_libres = False
                    # Verificar espacio arriba-izquierda
                    if col > 0 and fila > 0 and estado[(fila-1)*7 + col-1] == 0:
                        espacios_libres = True
                    # Verificar espacio abajo-derecha
                    if col+n < 7 and fila+n < 6 and estado[(fila+n)*7 + col+n] == 0:
                        espacios_libres = True
                    
                    if espacios_libres:
                        count += 1
                else:
                    count += 1
    
    return count

def ordena_avanzado(jugadas, jugador):
    """
    Función adaptada para usar con la API de ordenamiento del negamax.
    Usa el estado global establecido previamente.
    """
    global _estado_actual
    
    if _estado_actual is None:
        # Si no hay estado disponible, volvemos al ordenamiento básico
        valor_estrategico = {
            3: 100,  # Columna central
            2: 80,   # Adyacentes al centro
            4: 80,
            1: 60,   # Intermedias
            5: 60,
            0: 40,   # Extremos
            6: 40
        }
        return sorted(jugadas, key=lambda x: -valor_estrategico[x])
    
    estado = _estado_actual
    juego = Conecta4()
    puntuaciones = {}
    
    for jugada in jugadas:
        # Valor base según posición (priorizar centro)
        valor_posicion = 50 - 10 * abs(jugada - 3)
        
        # Simular la jugada
        nuevo_estado = juego.transicion(estado, jugada, jugador)
        
        # Verificar victoria inmediata (máxima prioridad)
        if juego.terminal(nuevo_estado) and juego.ganancia(nuevo_estado) == jugador:
            puntuaciones[jugada] = 10000
            continue
            
        # Comprobar si bloquea victoria del oponente
        bloqueo = False
        for col in range(7):
            if col in jugadas and col != jugada:
                estado_oponente = juego.transicion(estado, col, -jugador)
                if juego.terminal(estado_oponente) and juego.ganancia(estado_oponente) == -jugador:
                    bloqueo = True
                    break
        
        if bloqueo:
            puntuaciones[jugada] = 5000
            continue
            
        # Evitar jugadas que permiten al oponente ganar en el siguiente turno
        crea_amenaza = False
        for col in range(7):
            # Solo verificamos columnas que estarían disponibles
            if nuevo_estado[col] == 0:
                estado_siguiente = juego.transicion(nuevo_estado, col, -jugador)
                if juego.terminal(estado_siguiente) and juego.ganancia(estado_siguiente) == -jugador:
                    crea_amenaza = True
                    break
        
        puntuacion = valor_posicion
        
        if crea_amenaza:
            puntuacion -= 2000
            
        # Contar líneas de 2 y 3 propias
        lineas_2 = contar_conectados(nuevo_estado, jugador, 2)
        lineas_3 = contar_conectados(nuevo_estado, jugador, 3)
        
        puntuacion += lineas_2 * 10 + lineas_3 * 100
        
        # Penalizar si creamos oportunidades para el oponente
        lineas_2_oponente = contar_conectados(nuevo_estado, -jugador, 2)
        lineas_3_oponente = contar_conectados(nuevo_estado, -jugador, 3)
        
        puntuacion -= lineas_2_oponente * 5 + lineas_3_oponente * 50
        
        puntuaciones[jugada] = puntuacion
    
    # Ordenar jugadas por puntuación (mayor primero)
    return sorted(jugadas, key=lambda j: -puntuaciones.get(j, 0))

def negamax_con_estado_actual(juego, s, j, d):
    """Wrapper para jugador_negamax que incluye el estado actual"""
    set_estado_actual(s)  # Establecer el estado global
    return jugador_negamax(juego, s, j, ordena=ordena_avanzado, evalua=evalua3_avanzada, d=d)

def minimax_iter_con_estado_actual(juego, s, j, tiempo):
    """Wrapper para minimax_iterativo que incluye el estado actual"""
    set_estado_actual(s)  # Establecer el estado global
    return minimax_iterativo(juego, s, j, ordena=ordena_avanzado, evalua=evalua3_avanzada, tiempo=tiempo)

if __name__ == '__main__':

    modelo = Conecta4()
    print("="*40 + "\n" + "EL JUEGO DE CONECTA 4".center(40) + "\n" + "="*40)
    
    jugs = []
    for j in [1, -1]:
        print(f"Selección de jugadores para las {' XO'[j]}:")
        sel = 0
        print("   1. Jugador manual")
        print("   2. Jugador negamax limitado en profundidad")
        print("   3. Jugador negamax limitado en tiempo")
        print("   4. Jugador negamax avanzado limitado en profundidad")
        print("   5. Jugador negamax avanzado limitado en tiempo")
        while sel not in [1, 2, 3, 4, 5]:
            sel = int(input(f"Jugador para las {' XO'[j]}: "))
    
        if sel == 1:
            jugs.append(jugador_manual_conecta4)
        elif sel == 2:
            d = None
            while type(d) != int or d < 1:
                d = int(input("Profundidad: "))
            jugs.append(lambda juego, s, j: jugador_negamax(
                juego, s, j, ordena=ordena_centro, evalua=evalua_3con, d=d)
            )
        elif sel == 3:
            t = None
            while type(t) != int or t < 1:
                t = int(input("Tiempo: "))
            jugs.append(lambda juego, s, j: minimax_iterativo(
                juego, s, j, ordena=ordena_centro, evalua=evalua_3con, tiempo=t)
            )
        elif sel == 4:
            d = None
            while type(d) != int or d < 1:
                d = int(input("Profundidad: "))
            jugs.append(lambda juego, s, j: negamax_con_estado_actual(juego, s, j, d))
        else:  # sel == 5
            t = None
            while type(t) != int or t < 1:
                t = int(input("Tiempo: "))
            jugs.append(lambda juego, s, j: minimax_iter_con_estado_actual(juego, s, j, t))
        
    g, s_final = juega_dos_jugadores(modelo, jugs[0], jugs[1])
    print("\nSE ACABO EL JUEGO\n")
    pprint_conecta4(s_final)
    if g != 0:
        print("Gana el jugador " + " XO"[g])
    else:
        print("Empate")
