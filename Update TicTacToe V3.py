import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe Kids Edition")
        self.root.configure(bg="#FFF8E7")  # Calm yellow beige background

        self.current_player = "X"
        self.board = [[""]*3 for _ in range(3)]
        self.game_over = False
        self.vs_ai = False
        self.ai_difficulty = "Easy"
        self.score = {"X": 0, "O": 0, "Ties": 0}
        self.move_history = []

        # Colors and styles
        self.bg_color = "#FFF8E7"
        self.button_bg = "#FFF4C1"  # pastel yellow
        self.button_hover_bg = "#FFF9DB"
        self.button_outline = "#FFD966"  # warm yellow outline
        self.button_outline_hover = "#FFC107"  # stronger yellow on hover
        self.x_color = "#4A90E2"  # pastel blue for X
        self.o_color = "#FF6F61"  # pastel coral for O
        self.text_color = "#5D4636"  # warm brownish for text

        # Fonts - use Poppins if available or fallback to Segoe UI or Arial
        self.title_font = ("Poppins", 36, "bold")
        self.btn_font = ("Poppins", 18, "bold")
        self.label_font = ("Poppins", 20, "bold")

        self.main_menu_frame = None
        self.game_frame = None

        self.create_main_menu()

    # --- Main Menu ---
    def create_main_menu(self):
        if self.game_frame:
            self.game_frame.destroy()
        if self.main_menu_frame:
            self.main_menu_frame.destroy()

        self.main_menu_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_menu_frame.pack(expand=True, fill="both")

        # Big playful title
        title_label = tk.Label(
            self.main_menu_frame,
            text="Tic-Tac-Toe Kids!",
            font=self.title_font,
            fg=self.text_color,
            bg=self.bg_color,
            pady=60
        )
        title_label.pack()

        # Create colorful buttons with outlines and hover effects
        def make_button(text, command):
            btn = tk.Button(
                self.main_menu_frame,
                text=text,
                font=self.btn_font,
                bg=self.button_bg,
                fg=self.text_color,
                activebackground=self.button_hover_bg,
                activeforeground=self.text_color,
                bd=3,
                relief="solid",
                highlightthickness=3,
                highlightbackground=self.button_outline,
                highlightcolor=self.button_outline,
                padx=20, pady=12,
                cursor="hand2",
                command=command
            )
            btn.pack(pady=18, ipadx=20, fill='x', padx=150)

            # Hover effects
            def on_enter(e):
                e.widget.config(
                    bg=self.button_hover_bg,
                    highlightbackground=self.button_outline_hover,
                    highlightcolor=self.button_outline_hover,
                    bd=4
                )
            def on_leave(e):
                e.widget.config(
                    bg=self.button_bg,
                    highlightbackground=self.button_outline,
                    highlightcolor=self.button_outline,
                    bd=3
                )
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            return btn

        self.btn_vs_human = make_button("Play with a Friend", lambda: self.start_game("Human"))
        self.btn_vs_ai_easy = make_button("Play vs Easy AI", lambda: self.start_game("AI Easy"))
        self.btn_vs_ai_hard = make_button("Play vs Hard AI", lambda: self.start_game("AI Hard"))

        footer = tk.Label(
            self.main_menu_frame,
            text="Have fun and learn while playing!",
            font=("Poppins", 14, "italic"),
            fg="#A98467",
            bg=self.bg_color,
            pady=40
        )
        footer.pack(side="bottom")

    # --- Game Setup ---
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

        if self.vs_ai and self.current_player == "O":
            self.root.after(500, self.ai_move)

    def create_game_frame(self):
        if self.game_frame:
            self.game_frame.destroy()

        self.game_frame = tk.Frame(self.root, bg=self.bg_color)
        self.game_frame.pack(expand=True, fill="both")

        self.turn_label = tk.Label(
            self.game_frame,
            text=f"Player {self.current_player}'s turn",
            font=self.label_font,
            fg=self.text_color,
            bg=self.bg_color,
            pady=20
        )
        self.turn_label.pack()

        self.board_frame = tk.Frame(self.game_frame, bg=self.bg_color)
        self.board_frame.pack()

        self.buttons = [[None]*3 for _ in range(3)]

        for r in range(3):
            for c in range(3):
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    font=("Poppins", 40, "bold"),
                    width=4,
                    height=2,
                    bg=self.button_bg,
                    fg=self.text_color,
                    relief="raised",
                    bd=5,
                    cursor="hand2",
                    command=lambda row=r, col=c: self.on_click(row, col)
                )
                btn.grid(row=r, column=c, padx=15, pady=15)
                btn.config(
                    highlightbackground=self.button_outline,
                    highlightthickness=3,
                    bd=5,
                    relief="raised"
                )
                # Rounded corners are tricky in Tkinter; simulate by padding and border colors
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.button_hover_bg, bd=7))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.button_bg, bd=5))

                self.buttons[r][c] = btn

        # Scoreboard
        self.score_frame = tk.Frame(self.game_frame, bg="#FFF4C1", bd=3, relief="ridge")
        self.score_frame.pack(pady=25, ipadx=40, ipady=15)

        self.score_label = tk.Label(
            self.score_frame,
            text=self.get_score_text(),
            font=self.label_font,
            fg=self.text_color,
            bg="#FFF4C1"
        )
        self.score_label.pack()

        # Controls
        self.controls_frame = tk.Frame(self.game_frame, bg=self.bg_color)
        self.controls_frame.pack(pady=15)

        self.restart_button = tk.Button(
            self.controls_frame, text="Restart",
            font=self.btn_font,
            bg=self.button_bg, fg=self.text_color,
            activebackground=self.button_hover_bg,
            activeforeground=self.text_color,
            bd=3, relief="solid",
            highlightbackground=self.button_outline,
            highlightthickness=3,
            padx=30, pady=10,
            cursor="hand2",
            command=self.start_game_restart
        )
        self.restart_button.grid(row=0, column=0, padx=20)
        self.restart_button.bind("<Enter>", lambda e: e.widget.config(bg=self.button_hover_bg, bd=5))
        self.restart_button.bind("<Leave>", lambda e: e.widget.config(bg=self.button_bg, bd=3))

        self.back_button = tk.Button(
            self.controls_frame, text="Back to Menu",
            font=self.btn_font,
            bg=self.button_bg, fg=self.text_color,
            activebackground=self.button_hover_bg,
            activeforeground=self.text_color,
            bd=3, relief="solid",
            highlightbackground=self.button_outline,
            highlightthickness=3,
            padx=30, pady=10,
            cursor="hand2",
            command=self.create_main_menu
        )
        self.back_button.grid(row=0, column=1, padx=20)
        self.back_button.bind("<Enter>", lambda e: e.widget.config(bg=self.button_hover_bg, bd=5))
        self.back_button.bind("<Leave>", lambda e: e.widget.config(bg=self.button_bg, bd=3))

    def start_game_restart(self):
        mode = "Human" if not self.vs_ai else ("AI Easy" if self.ai_difficulty == "Easy" else "AI Hard")
        self.start_game(mode)

    def get_score_text(self):
        return f"Score - X: {self.score['X']}   O: {self.score['O']}   Ties: {self.score['Ties']}"

    # --- Gameplay ---
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
        self.buttons[row][col]["fg"] = self.x_color if self.current_player == "X" else self.o_color

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
        highlight_bg = "#C9E4C5" if player == "X" else "#F7B7A3"  # soft green or soft coral

        # Rows
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] == player:
                for j in range(3):
                    self.buttons[i][j]["bg"] = highlight_bg
                return
        # Columns
        for i in range(3):
            if b[0][i] == b[1][i] == b[2][i] == player:
                for j in range(3):
                    self.buttons[j][i]["bg"] = highlight_bg
                return
        # Diagonals
        if b[0][0] == b[1][1] == b[2][2] == player:
            for i in range(3):
                self.buttons[i][i]["bg"] = highlight_bg
            return
        if b[0][2] == b[1][1] == b[2][0] == player:
            for i in range(3):
                self.buttons[i][2 - i]["bg"] = highlight_bg
            return

    # --- AI Logic ---
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

    # --- Helpers ---
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


