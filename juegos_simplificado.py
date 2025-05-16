"""
Modulo para las clases básicas para realizar un juego de forma muy simplificada
    
Vamos a usar una orientación funcional en este modulo

"""

from random import shuffle
    
class ModeloJuegoZT2:
    """
    Clase abstracta para juegos de suma cero, por turnos, dos jugadores.
    
    Se asumen que los jugadores son 1 y -1
    
    """
    def inicializa(self):
        """
        Inicializa el estado inicial del juego y el jugador
        que comienza (típicamente el primero)
        
        devuelve: (s0, j) donde s0 es el estado inicial y j el jugador
        
        """
        raise NotImplementedError("Hay que desarrollar este método, pues")
    
    def jugadas_legales(self, s, j):
        """
        Devuelve una lista con las jugadas legales para el jugador j
        en el estado s
        
        """
        raise NotImplementedError("Hay que desarrollar este método, pues")      
    
    def transicion(self, s, a, j):
        """
        Devuelve el estado que resulta de realizar la jugada a en el estado s
        para el jugador j
        
        """
        raise NotImplementedError("Hay que desarrollar este método, pues")
    
    def terminal(self, s):
        """
        Devuelve True si es terminal el estado actual,
        
        """
        raise NotImplementedError("Hay que desarrollar este método, pues")
    
    def ganancia(self, s):
        """
        Devuelve la ganancia para el jugador 1 en el estado terminal s
        
        """
        raise NotImplementedError("Hay que desarrollar este método, pues")


def juega_dos_jugadores(juego, jugador1, jugador2):
    """
    Juega un juego de dos jugadores
    
    juego: instancia de ModeloJuegoZT
    jugador1: función que recibe el estado y devuelve la jugada
    jugador2: función que recibe el estado y devuelve la jugada
    
    """
    s, j = juego.inicializa()
    while not juego.terminal(s):
        a = jugador1(juego, s, j) if j == 1 else jugador2(juego, s, j)
        s = juego.transicion(s, a, j)
        j = -j
    return juego.ganancia(s), s


def minimax(juego, estado, jugador):
    """
    Devuelve la mejor jugada para el jugador en el estado
    
    """
    j = jugador
    def max_val(estado, jugador):
        if juego.terminal(estado):
            return j * juego.ganancia(estado)
        v = -1e10
        for a in juego.jugadas_legales(estado, jugador):
            v = max(
                v, 
                min_val(
                    juego.transicion(estado, a, jugador), 
                    -jugador
                )
            )
        return v
    
    def min_val(estado, jugador):
        if juego.terminal(estado):
            return j * juego.ganancia(estado)
        v = 1e10
        for a in juego.jugadas_legales(estado, jugador):
            v = min(
                v, 
                max_val(
                    juego.transicion(estado, a, jugador), 
                    -jugador
                )
            )
        return v
    
    return max(
        juego.jugadas_legales(estado, jugador),
        key=lambda a: min_val(
            juego.transicion(estado, a, jugador), 
            -jugador
            )
        )
    

def alpha_beta(juego, estado, jugador, ordena=None):
    """
    Devuelve la mejor jugada para el jugador en el estado
    
    """
    j = jugador
    def max_val(estado, jugador, alpha, beta):
        if juego.terminal(estado):
            return j * juego.ganancia(estado)
        v = -1e10
        jugadas = list(juego.jugadas_legales(estado, jugador))
        if ordena:
            jugadas = ordena(jugadas)
        else:
            shuffle(jugadas)
        for a in jugadas:
            v = max(
                v, 
                min_val(
                    juego.transicion(estado, a, jugador), 
                    -jugador, 
                    alpha, beta
                )
            )
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v
    
    def min_val(estado, jugador, alpha, beta):
        if juego.terminal(estado):
            return j * juego.ganancia(estado)
        v = 1e10
        jugadas = list(juego.jugadas_legales(estado, jugador))
        if ordena:
            jugadas = ordena(jugadas)
        else:
            shuffle(jugadas)
        for a in jugadas:
            v = min(
                v, 
                max_val(
                    juego.transicion(estado, a, jugador), 
                    -jugador, 
                    alpha, beta
                )
            )
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
    
    jugadas = list(juego.jugadas_legales(estado, jugador))
    if ordena:
        jugadas = ordena(jugadas)
    else:
        shuffle(jugadas)
    return max(
        jugadas,
        key=lambda a: min_val(
                juego.transicion(estado, a, jugador), 
                -jugador, 
                -1e10, 1e10
            ))
