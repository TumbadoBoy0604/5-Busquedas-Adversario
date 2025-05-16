import tkinter as tk
from tkinter import messagebox
from ultimate_tictaetoe import *


class UltimateTicTacToeGUI:
    def __init__(self, juego, agente_X=None, agente_O=None):
        self.juego = juego
        self.agente_X = agente_X
        self.agente_O = agente_O
        self.estado, self.jugador_actual = juego.inicializa()
        self.jugada_usuario = None
        self.esperando_jugada = False
        self.callback_jugada = None
        self.root = tk.Tk()
        self.root.title("Ultimate TicTacToe")
        
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        
        self.botones = []
        
        for tablero_idx in range(9):
            frame_tablero = tk.Frame(self.frame, relief=tk.RIDGE, borderwidth=2)
            frame_tablero.grid(row=tablero_idx//3, column=tablero_idx%3, padx=2, pady=2)
            tablero_botones = []
            for pos in range(9):
                btn = tk.Button(frame_tablero, text=" ", width=3, height=1,
                                font=("Arial", 16, "bold"),
                                command=lambda tb=tablero_idx, p=pos: self.jugar(tb, p))
                btn.grid(row=pos//3, column=pos%3)
                tablero_botones.append(btn)
            self.botones.append(tablero_botones)
        
        self.info = tk.Label(self.root, text=f"Turno: {'X' if self.jugador_actual == 1 else 'O'}")
        self.info.pack(pady=10)
        
        self.actualiza_gui()

    def actualiza_gui(self):
        tableros, tablero_actual, ultimo_movimiento = self.estado
        simbolos = {0: " ", 1: "X", -1: "O"}
        
        for tb_idx, tablero_botones in enumerate(self.botones):
            tablero = tableros[tb_idx]
            activo = (tablero_actual == -1 or tablero_actual == tb_idx) and not self.juego._hay_ganador(tablero) and not self.juego._tablero_lleno(tablero)
            
            for pos, btn in enumerate(tablero_botones):
                btn.config(text=simbolos[tablero[pos]])
                if tablero[pos] == 0 and activo:
                    btn.config(state=tk.NORMAL)
                else:
                    btn.config(state=tk.DISABLED)
                
                if tb_idx == tablero_actual:
                    btn.config(bg="#d1ffd1")
                else:
                    btn.config(bg="lightgray")
                
                if ultimo_movimiento == (tb_idx, pos):
                    btn.config(bg="#ffff99")
        
        self.info.config(text=f"Turno: {'X' if self.jugador_actual == 1 else 'O'}")

   
    def jugar(self, tablero, pos):
        jugada = (tablero, pos)

        if self.esperando_jugada:
            if jugada not in self.juego.jugadas_legales(self.estado, self.jugador_actual):
                return  # Clic inválido mientras espera jugada
            self.jugada_usuario = jugada
            if self.callback_jugada:
                self.callback_jugada(jugada)
            return

        if (self.jugador_actual == 1 and self.agente_X) or (self.jugador_actual == -1 and self.agente_O):
            return  # Ignora clics si es IA

        if jugada not in self.juego.jugadas_legales(self.estado, self.jugador_actual):
            return
        
        self.estado = self.juego.transicion(self.estado, jugada, self.jugador_actual)

        if self.juego.terminal(self.estado):
            self.actualiza_gui()
            self.mostrar_resultado()
            return

        self.jugador_actual = -self.jugador_actual
        self.actualiza_gui()
        self.root.after(200, self.turno_ia_si_es)

    def turno_ia_si_es(self):
        agente = self.agente_X if self.jugador_actual == 1 else self.agente_O
        if agente is not None:
            self.root.after(100, lambda: self.jugar_ia(agente))

    def jugar_ia(self, agente):
        jugada = agente(self.juego, self.estado, self.jugador_actual)
        self.estado = self.juego.transicion(self.estado, jugada, self.jugador_actual)
        
        if self.juego.terminal(self.estado):
            self.actualiza_gui()
            self.mostrar_resultado()
            return
        
        self.jugador_actual = -self.jugador_actual
        self.actualiza_gui()
        self.root.after(200, self.turno_ia_si_es)

    def mostrar_resultado(self):
        ganancia = self.juego.ganancia(self.estado)
        if ganancia == 0:
            messagebox.showinfo("Juego terminado", "Empate!")
        else:
            ganador = "X" if ganancia == 1 else "O"
            messagebox.showinfo("Juego terminado", f"Ganador: {ganador}")
        self.root.destroy()

def selecciona_agente(nombre):
    print(f"Selecciona agente para {nombre}")
    print("1. Humano")
    print("2. IA simple (profundidad limitada)")
    print("3. IA simple (tiempo limitado)")
    print("4. IA avanzada (profundidad limitada)")
    print("5. IA avanzada (tiempo limitado)")

    while True:
        try:
            sel = int(input(f"Agente para {nombre}: "))
            
            if sel == 1:
                return jugador_manual_gui  # <-- pasamos la GUI luego
            elif sel in [2, 4]:
                d = int(input("Profundidad (recomendado 2-4): "))
                if sel == 2:
                    return lambda juego, s, j: jugador_negamax(
                        juego, s, j, ordena=ordena_centro_ultimate, evalua=evalua_simple_ultimate, d=d)
                else:
                    return lambda juego, s, j: negamax_con_estado_actual(juego, s, j, d)
            elif sel in [3, 5]:
                t = int(input("Tiempo en segundos: "))
                if sel == 3:
                    return lambda juego, s, j: minimax_iterativo(
                        juego, s, j, ordena=ordena_centro_ultimate, evalua=evalua_simple_ultimate, tiempo=t)
                else:
                    return lambda juego, s, j: minimax_iter_con_estado_actual(juego, s, j, t)
            else:
                print("Opción inválida.")
        except ValueError:
            print("Entrada inválida.")

if __name__ == '__main__':

    print("="*40)
    print("ULTIMATE TIC-TAC-TOE".center(40))
    print("="*40)
    
    modelo = UltimateTicTacToe()

    print("\nSeleccione quién juega como X:")
    agente_X = selecciona_agente("X")

    print("\nSeleccione quién juega como O:")
    agente_O = selecciona_agente("O")

    # Crea la GUI
    gui = UltimateTicTacToeGUI(modelo)

    # Asigna agentes correctamente
    gui.agente_X = agente_X(gui) if agente_X == jugador_manual_gui else agente_X
    gui.agente_O = agente_O(gui) if agente_O == jugador_manual_gui else agente_O

    # Inicia el juego
    gui.turno_ia_si_es()
    gui.root.mainloop()
