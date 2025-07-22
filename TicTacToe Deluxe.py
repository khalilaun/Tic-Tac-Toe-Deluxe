import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe Deluxe")
        self.root.configure(bg="#0b1a2d")  # Dark space blue background

        self.current_player = "X"
        self.board = [[""]*3 for _ in range(3)]
        self.game_over = False
        self.vs_ai = False
        self.ai_difficulty = "Easy"
        self.score = {"X": 0, "O": 0, "Ties": 0}
        self.move_history = []

        self.title_color = "#00d2ff"
        self.label_fg = "#b3e0ff"
        self.button_bg = "#112f5a"
        self.button_active_bg = "#1a4d8f"
        self.button_fg = "#a1d0ff"
        self.button_active_fg = "#e0f7ff"

        # Containers
        self.main_menu_frame = None
        self.game_frame = None

        self.create_main_menu()

    # ---- Main Menu ----
    def create_main_menu(self):
        if self.game_frame:
            self.game_frame.destroy()

        if self.main_menu_frame:
            self.main_menu_frame.destroy()

        self.main_menu_frame = tk.Frame(self.root, bg="#0b1a2d")
        self.main_menu_frame.pack(expand=True, fill="both")

        # Title canvas for glowing text
        self.title_canvas = tk.Canvas(self.main_menu_frame, bg="#0b1a2d", highlightthickness=0, height=100)
        self.title_canvas.pack(pady=(30, 20), fill="x")
        self.draw_glowing_text(self.title_canvas, "Tic-Tac-Toe Deluxe", 250, 50)

        # Buttons for modes
        btn_font = ("Comic Sans MS", 18, "bold")

        self.btn_vs_human = tk.Button(
            self.main_menu_frame, text="Play vs Friend",
            font=btn_font,
            bg=self.button_bg, fg=self.button_fg,
            activebackground=self.button_active_bg,
            activeforeground=self.button_active_fg,
            width=20, height=2,
            bd=0,
            cursor="hand2",
        )
        self.btn_vs_human.pack(pady=10)
        self.btn_vs_human.bind("<Enter>", lambda e: e.widget.config(bg=self.button_active_bg, fg=self.button_active_fg))
        self.btn_vs_human.bind("<Leave>", lambda e: e.widget.config(bg=self.button_bg, fg=self.button_fg))
        self.btn_vs_human.config(command=lambda: self.start_game(mode="Human"))

        self.btn_vs_ai_easy = tk.Button(
            self.main_menu_frame, text="Play vs Easy AI",
            font=btn_font,
            bg=self.button_bg, fg=self.button_fg,
            activebackground=self.button_active_bg,
            activeforeground=self.button_active_fg,
            width=20, height=2,
            bd=0,
            cursor="hand2",
        )
        self.btn_vs_ai_easy.pack(pady=10)
        self.btn_vs_ai_easy.bind("<Enter>", lambda e: e.widget.config(bg=self.button_active_bg, fg=self.button_active_fg))
        self.btn_vs_ai_easy.bind("<Leave>", lambda e: e.widget.config(bg=self.button_bg, fg=self.button_fg))
        self.btn_vs_ai_easy.config(command=lambda: self.start_game(mode="AI Easy"))

        self.btn_vs_ai_hard = tk.Button(
            self.main_menu_frame, text="Play vs Hard AI",
            font=btn_font,
            bg=self.button_bg, fg=self.button_fg,
            activebackground=self.button_active_bg,
            activeforeground=self.button_active_fg,
            width=20, height=2,
            bd=0,
            cursor="hand2",
        )
        self.btn_vs_ai_hard.pack(pady=10)
        self.btn_vs_ai_hard.bind("<Enter>", lambda e: e.widget.config(bg=self.button_active_bg, fg=self.button_active_fg))
        self.btn_vs_ai_hard.bind("<Leave>", lambda e: e.widget.config(bg=self.button_bg, fg=self.button_fg))
        self.btn_vs_ai_hard.config(command=lambda: self.start_game(mode="AI Hard"))

        # Footer text
        footer = tk.Label(self.main_menu_frame, text="A fun, space-themed Tic-Tac-Toe game!", fg="#5599cc", bg="#0b1a2d",
                          font=("Comic Sans MS", 12, "italic"))
        footer.pack(side="bottom", pady=15)

        # Make sure window resizes nicely
        self.root.update()
        self.center_title_text()

        # Bind resize event to keep title centered
        self.root.bind("<Configure>", lambda e: self.center_title_text())

    def center_title_text(self):
        self.title_canvas.delete("all")
        width = self.title_canvas.winfo_width()
        if width == 1:  # Not yet properly rendered
            width = 500
        self.draw_glowing_text(self.title_canvas, "Tic-Tac-Toe Deluxe", width//2, 50)

    def draw_glowing_text(self, canvas, text, x, y):
        glow_color = self.title_color
        # Draw multiple shadow layers for glow
        offsets = [(-2,-2), (-2,2), (2,-2), (2,2), (0,-3), (0,3), (-3,0), (3,0)]
        for ox, oy in offsets:
            canvas.create_text(
                x + ox, y + oy, text=text, fill=glow_color,
                font=("Comic Sans MS", 40, "bold")
            )
        # Main text on top
        canvas.create_text(
            x, y, text=text, fill=self.label_fg,
            font=("Comic Sans MS", 40, "bold")
        )

    # ---- Game Setup ----
    def start_game(self, mode):
        if self.main_menu_frame:
            self.main_menu_frame.destroy()

        self.vs_ai = (mode != "Human")
        self.ai_difficulty = "Easy" if mode == "AI Easy" else "Hard" if mode == "AI Hard" else None

        self.current_player = "X"
        self.board = [[""]*3 for _ in range(3)]
        self.game_over = False
        self.move_history.clear()

        self.create_game_frame()

        # If AI starts first (O), make AI move after short delay
        if self.vs_ai and self.current_player == "O":
            self.root.after(500, self.ai_move)

    def create_game_frame(self):
        if self.game_frame:
            self.game_frame.destroy()

        self.game_frame = tk.Frame(self.root, bg="#0b1a2d")
        self.game_frame.pack(expand=True, fill="both")

        # Turn Label
        self.turn_label = tk.Label(
            self.game_frame,
            text=f"Player {self.current_player}'s turn",
            font=("Comic Sans MS", 24, "bold"),
            fg=self.label_fg, bg="#0b1a2d"
        )
        self.turn_label.pack(pady=(20, 10))

        # Board Frame
        self.board_frame = tk.Frame(self.game_frame, bg="#0b1a2d")
        self.board_frame.pack(pady=10)

        self.buttons = [[None]*3 for _ in range(3)]
        btn_style = {
            "font": ("Comic Sans MS", 36, "bold"),
            "width": 4,
            "height": 2,
            "bg": self.button_bg,
            "fg": self.button_fg,
            "activebackground": self.button_active_bg,
            "activeforeground": self.button_active_fg,
            "bd": 4,
            "relief": "ridge",
            "cursor": "hand2"
        }
        for r in range(3):
            for c in range(3):
                btn = tk.Button(
                    self.board_frame,
                    command=lambda row=r, col=c: self.on_click(row, col),
                    **btn_style
                )
                btn.grid(row=r, column=c, padx=6, pady=6)
                self.buttons[r][c] = btn

        # Scoreboard
        self.score_frame = tk.Frame(self.game_frame, bg="#112f5a", bd=3, relief="ridge")
        self.score_frame.pack(pady=15, ipadx=15, ipady=10)

        self.score_label = tk.Label(
            self.score_frame,
            text=self.get_score_text(),
            font=("Comic Sans MS", 16, "bold"),
            fg="#99ccff",
            bg="#112f5a"
        )
        self.score_label.pack()

        # Controls Frame
        self.controls_frame = tk.Frame(self.game_frame, bg="#0b1a2d")
        self.controls_frame.pack(pady=10)

        self.restart_button = tk.Button(
            self.controls_frame, text="Restart",
            font=("Comic Sans MS", 14, "bold"),
            bg=self.button_bg, fg="#00aaff",
            activebackground=self.button_active_bg,
            activeforeground="#66ddff",
            bd=0,
            padx=20, pady=8,
            cursor="hand2",
            command=self.start_game_restart
        )
        self.restart_button.grid(row=0, column=0, padx=20)
        self.restart_button.bind("<Enter>", lambda e: e.widget.config(fg="#66ddff"))
        self.restart_button.bind("<Leave>", lambda e: e.widget.config(fg="#00aaff"))

        self.back_button = tk.Button(
            self.controls_frame, text="Back to Menu",
            font=("Comic Sans MS", 14, "bold"),
            bg=self.button_bg, fg="#00aaff",
            activebackground=self.button_active_bg,
            activeforeground="#66ddff",
            bd=0,
            padx=20, pady=8,
            cursor="hand2",
            command=self.create_main_menu
        )
        self.back_button.grid(row=0, column=1, padx=20)
        self.back_button.bind("<Enter>", lambda e: e.widget.config(fg="#66ddff"))
        self.back_button.bind("<Leave>", lambda e: e.widget.config(fg="#00aaff"))

    def start_game_restart(self):
        # Restart with same mode
        mode = "Human" if not self.vs_ai else ("AI Easy" if self.ai_difficulty == "Easy" else "AI Hard")
        self.start_game(mode)

    def get_score_text(self):
        return f"Score - X: {self.score['X']}   O: {self.score['O']}   Ties: {self.score['Ties']}"

    # ---- Gameplay ----
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

        # Color difference for X and O
        self.buttons[row][col]["fg"] = "#00ccff" if self.current_player == "X" else "#ff6666"

        self.move_history.append((row, col, self.current_player))

        if self.check_winner(self.current_player):
            self.game_over = True
            self.turn_label.config(text=f"Player {self.current_player} wins!")
            self.highlight_winner(self.current_player)
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.disable_all_buttons()
            self.score[self.current_player] += 1
            self.score_label.config(text=self.get_score_text())
        elif self.is_board_full():
            self.game_over = True
            self.turn_label.config(text="It's a tie!")
            messagebox.showinfo("Game Over", "It's a tie!")
            self.disable_all_buttons()
            self.score["Ties"] += 1
            self.score_label.config(text=self.get_score_text())
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            self.turn_label.config(text=f"Player {self.current_player}'s turn")

    def disable_all_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn["state"] = tk.DISABLED

    def highlight_winner(self, player):
        b = self.board
        winning_color = "#00ffff" if player == "X" else "#ff6666"

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

    # ---- AI Logic ----
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

    # ---- Helpers ----
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
    root.geometry("600x700")
    root.minsize(520, 600)
    game = TicTacToeGame(root)
    root.mainloop()




