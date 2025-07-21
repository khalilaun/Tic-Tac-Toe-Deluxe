import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe Deluxe")
        self.current_player = "X"
        self.buttons = [[None]*3 for _ in range(3)]
        self.board = [[""]*3 for _ in range(3)]
        self.vs_ai = False
        self.ai_difficulty = "Easy"  # or "Hard"
        self.game_over = False
        self.move_history = []
        self.score = {"X": 0, "O": 0, "Ties": 0}

        self.root.configure(bg="#e6f0ff")  # Light blue background

        # Mode selection frame with blue text
        self.mode_frame = tk.Frame(root, bg="#e6f0ff")
        self.mode_frame.pack(pady=10)

        tk.Label(self.mode_frame, text="Choose Mode:", font=("Arial", 12, "bold"), bg="#e6f0ff", fg="#003366").pack(side=tk.LEFT)

        self.mode_var = tk.StringVar(value="Human")
        modes = ["Human", "AI Easy", "AI Hard"]
        for mode in modes:
            tk.Radiobutton(
                self.mode_frame,
                text=mode,
                variable=self.mode_var,
                value=mode,
                command=self.start_new_game,
                bg="#e6f0ff",
                fg="#003366",
                selectcolor="#99c2ff",
                font=("Arial", 10, "bold"),
                activebackground="#cce0ff"
            ).pack(side=tk.LEFT, padx=5)

        # Turn label
        self.label = tk.Label(root, text=f"Player X's turn", font=("Arial", 16, "bold"), bg="#e6f0ff", fg="#004080")
        self.label.pack(pady=5)

        # Game board frame with padding
        self.frame = tk.Frame(root, bg="#e6f0ff")
        self.frame.pack(pady=5)

        button_style = {
            "font": ("Arial", 26, "bold"),
            "width": 5,
            "height": 2,
            "bg": "#cce0ff",
            "fg": "#003366",
            "activebackground": "#99c2ff",
            "activeforeground": "#002244",
            "bd": 3,
            "relief": "ridge",
            "highlightthickness": 2,
            "highlightbackground": "#3399ff",
            "highlightcolor": "#3399ff",
            "cursor": "hand2",
        }

        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    self.frame,
                    command=lambda row=i, col=j: self.on_click(row, col),
                    **button_style
                )
                btn.grid(row=i, column=j, padx=4, pady=4)
                self.buttons[i][j] = btn

        # Scoreboard frame with border and background
        self.score_frame = tk.Frame(root, bg="#b3c6ff", bd=3, relief="groove")
        self.score_frame.pack(pady=15, ipadx=20, ipady=10)

        self.score_label = tk.Label(self.score_frame, text=self.get_score_text(), font=("Arial", 14, "bold"), bg="#b3c6ff", fg="#002266", justify=tk.LEFT)
        self.score_label.pack()

        # Restart button
        self.restart_button = tk.Button(
            root, text="Restart", font=("Arial", 12, "bold"),
            bg="#3399ff", fg="white", activebackground="#2673cc",
            activeforeground="white", bd=0, padx=15, pady=8,
            command=self.start_new_game,
            cursor="hand2"
        )
        self.restart_button.pack(pady=10)

        self.start_new_game()

    def get_score_text(self):
        return f"Scoreboard:\nPlayer X: {self.score['X']}  Player O: {self.score['O']}  Ties: {self.score['Ties']}"

    def start_new_game(self):
        self.board = [[""]*3 for _ in range(3)]
        self.current_player = "X"
        self.game_over = False
        self.move_history.clear()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = ""
                self.buttons[i][j]["state"] = tk.NORMAL
                # Reset button colors
                self.buttons[i][j]["bg"] = "#cce0ff"
                self.buttons[i][j]["fg"] = "#003366"
        self.label.config(text=f"Player {self.current_player}'s turn")
        self.score_label.config(text=self.get_score_text())

        mode = self.mode_var.get()
        if mode == "Human":
            self.vs_ai = False
        else:
            self.vs_ai = True
            self.ai_difficulty = "Easy" if mode == "AI Easy" else "Hard"

        # AI starts if current player is O
        if self.vs_ai and self.current_player == "O":
            self.root.after(500, self.ai_move)

    def on_click(self, row, col):
        if self.game_over or self.board[row][col] != "":
            return

        self.make_move(row, col)

        if self.vs_ai and not self.game_over and self.current_player == "O":
            self.root.after(500, self.ai_move)

    def make_move(self, row, col):
        self.board[row][col] = self.current_player
        self.buttons[row][col]["text"] = self.current_player
        self.buttons[row][col]["state"] = tk.DISABLED

        # Different color for X and O
        if self.current_player == "X":
            self.buttons[row][col]["fg"] = "#001a66"
        else:
            self.buttons[row][col]["fg"] = "#660000"

        self.move_history.append((row, col, self.current_player))

        if self.check_winner(self.current_player):
            self.game_over = True
            self.label.config(text=f"Player {self.current_player} wins!")
            self.highlight_winner(self.current_player)
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins! 🎉")
            self.disable_all_buttons()
            self.score[self.current_player] += 1
            self.score_label.config(text=self.get_score_text())

        elif self.is_board_full():
            self.game_over = True
            self.label.config(text="It's a tie!")
            messagebox.showinfo("Game Over", "It's a tie! 🤝")
            self.disable_all_buttons()
            self.score["Ties"] += 1
            self.score_label.config(text=self.get_score_text())

        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            self.label.config(text=f"Player {self.current_player}'s turn")

    def disable_all_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["state"] = tk.DISABLED

    def highlight_winner(self, player):
        b = self.board
        # Highlight the winning line in a brighter blue or red
        winning_color = "#3399ff" if player == "X" else "#cc6666"

        # Rows
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] == player:
                for j in range(3):
                    self.buttons[i][j]["bg"] = winning_color
                return
        # Columns
        for i in range(3):
            if b[0][i] == b[1][i] == b[2][i] == player:
                for j in range(3):
                    self.buttons[j][i]["bg"] = winning_color
                return
        # Diagonals
        if b[0][0] == b[1][1] == b[2][2] == player:
            for i in range(3):
                self.buttons[i][i]["bg"] = winning_color
            return
        if b[0][2] == b[1][1] == b[2][0] == player:
            for i in range(3):
                self.buttons[i][2 - i]["bg"] = winning_color
            return

    # --- AI and minimax functions unchanged ---
    def ai_move(self):
        if self.game_over:
            return

        if self.ai_difficulty == "Easy":
            self.ai_random_move()
        else:
            self.ai_hard_move()

    def ai_random_move(self):
        available = [(r,c) for r in range(3) for c in range(3) if self.board[r][c] == ""]
        if available:
            move = random.choice(available)
            self.make_move(*move)

    def ai_hard_move(self):
        best_score = -float('inf')
        best_move = None
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == "":
                    self.board[r][c] = self.current_player
                    score = self.minimax(self.board, False)
                    self.board[r][c] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        if best_move:
            self.make_move(*best_move)

    def minimax(self, board, is_maximizing):
        if self.check_winner_static(board, "O"):
            return 1
        elif self.check_winner_static(board, "X"):
            return -1
        elif all(cell != "" for row in board for cell in row):
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == "":
                        board[r][c] = "O"
                        score = self.minimax(board, False)
                        board[r][c] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == "":
                        board[r][c] = "X"
                        score = self.minimax(board, True)
                        board[r][c] = ""
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        b = self.board
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] == player:
                return True
            if b[0][i] == b[1][i] == b[2][i] == player:
                return True
        if b[0][0] == b[1][1] == b[2][2] == player:
            return True
        if b[0][2] == b[1][1] == b[2][0] == player:
            return True
        return False

    def check_winner_static(self, board, player):
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] == player:
                return True
            if board[0][i] == board[1][i] == board[2][i] == player:
                return True
        if board[0][0] == board[1][1] == board[2][2] == player:
            return True
        if board[0][2] == board[1][1] == board[2][0] == player:
            return True
        return False

    def is_board_full(self):
        return all(cell != "" for row in self.board for cell in row)

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGame(root)
    root.mainloop()

