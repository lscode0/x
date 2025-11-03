import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kółko i Krzyżyk")
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_over = False

        # Etykieta statusu informująca o turze gracza
        self.status_label = tk.Label(root, text=f"Tura gracza: {self.current_player}", font=('Arial', 14))
        self.status_label.pack(pady=10)

        # Ramka na planszę gry
        board_frame = tk.Frame(self.root)
        board_frame.pack()

        # Tworzenie przycisków planszy
        for row in range(3):
            for col in range(3):
                self.buttons[row][col] = tk.Button(board_frame, text="", font=('Arial', 40, 'bold'),
                                                   width=4, height=2,
                                                   command=lambda r=row, c=col: self.handle_click(r, c))
                self.buttons[row][col].grid(row=row, column=col)

        # Przycisk restartu
        restart_button = tk.Button(self.root, text="Restart", font=('Arial', 12), command=self.restart_game)
        restart_button.pack(pady=10)

    def handle_click(self, row, col):
        """Obsługuje kliknięcie w pole na planszy."""
        if self.board[row][col] == "" and not self.game_over:
            # Ustaw symbol gracza na planszy i w przycisku
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, state=tk.DISABLED)

            # Sprawdź, czy jest zwycięzca lub remis
            if self.check_winner(self.current_player):
                self.game_over = True
                self.status_label.config(text=f"Wygrywa gracz {self.current_player}!")
                messagebox.showinfo("Koniec gry", f"Wygrywa gracz {self.current_player}!")
            elif self.is_draw():
                self.game_over = True
                self.status_label.config(text="Remis!")
                messagebox.showinfo("Koniec gry", "Remis!")
            else:
                # Zmień gracza
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status_label.config(text=f"Tura gracza: {self.current_player}")

    def check_winner(self, player):
        """Sprawdza, czy dany gracz wygrał."""
        # Sprawdzenie wierszy i kolumn
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)): return True
            if all(self.board[j][i] == player for j in range(3)): return True
        # Sprawdzenie przekątnych
        if all(self.board[i][i] == player for i in range(3)): return True
        if all(self.board[i][2 - i] == player for i in range(3)): return True
        return False

    def is_draw(self):
        """Sprawdza, czy nastąpił remis."""
        return all(self.board[row][col] != "" for row in range(3) for col in range(3))

    def restart_game(self):
        """Resetuje grę do stanu początkowego."""
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.status_label.config(text=f"Tura gracza: {self.current_player}")
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
