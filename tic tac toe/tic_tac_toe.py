"""
tic_tac_toe_minimax.py
اجرای بازی Tic-Tac-Toe با رابط گرافیکی (tkinter) و هوش مصنوعی Minimax + Alpha-Beta.
"""

import tkinter as tk
from tkinter import messagebox
import copy

# ----- تنظیمات اولیه -----
HUMAN = None   # نماد انسان ('X' یا 'O') — تنظیم می‌شود از UI
AI = None      # نماد هوش مصنوعی
EMPTY = ''
BOARD_SIZE = 3

# ----- منطق بازی -----
def initial_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def available_moves(board):
    moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == EMPTY:
                moves.append((r, c))
    return moves

def is_board_full(board):
    return all(board[r][c] != EMPTY for r in range(BOARD_SIZE) for c in range(BOARD_SIZE))

def check_winner(board):
    """برمی‌گرداند ('X'/'O', [(cells)]) یا (None, None)"""
    # ردیف‌ها
    for r in range(BOARD_SIZE):
        if board[r][0] != EMPTY and all(board[r][c] == board[r][0] for c in range(BOARD_SIZE)):
            return board[r][0], [(r, c) for c in range(BOARD_SIZE)]
    # ستون‌ها
    for c in range(BOARD_SIZE):
        if board[0][c] != EMPTY and all(board[r][c] == board[0][c] for r in range(BOARD_SIZE)):
            return board[0][c], [(r, c) for r in range(BOARD_SIZE)]
    # قطر اصلی
    if board[0][0] != EMPTY and all(board[i][i] == board[0][0] for i in range(BOARD_SIZE)):
        return board[0][0], [(i, i) for i in range(BOARD_SIZE)]
    # قطر فرعی
    if board[0][BOARD_SIZE-1] != EMPTY and all(board[i][BOARD_SIZE-1-i] == board[0][BOARD_SIZE-1] for i in range(BOARD_SIZE)):
        return board[0][BOARD_SIZE-1], [(i, BOARD_SIZE-1-i) for i in range(BOARD_SIZE)]
    return None, None

def game_over(board):
    winner, line = check_winner(board)
    if winner:
        return True, winner, line
    if is_board_full(board):
        return True, None, None
    return False, None, None

# ----- Minimax با Alpha-Beta -----
def minimax(board, depth, maximizing_player, alpha, beta, ai_symbol, human_symbol):
    over, winner, _ = game_over(board)
    if over:
        if winner == ai_symbol:
            return 10 - depth, None  # برد AI
        elif winner == human_symbol:
            return depth - 10, None  # برد انسان (منفی)
        else:
            return 0, None  # تساوی

    if maximizing_player:
        max_eval = -999
        best_move = None
        for (r, c) in available_moves(board):
            board[r][c] = ai_symbol
            eval_score, _ = minimax(board, depth+1, False, alpha, beta, ai_symbol, human_symbol)
            board[r][c] = EMPTY
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (r, c)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = 999
        best_move = None
        for (r, c) in available_moves(board):
            board[r][c] = human_symbol
            eval_score, _ = minimax(board, depth+1, True, alpha, beta, ai_symbol, human_symbol)
            board[r][c] = EMPTY
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (r, c)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

# برای سطح‌های سختی ضعیف‌تر از Minimax کامل استفاده می‌کنیم:
def ai_move_by_difficulty(board, difficulty):
    """difficulty: 'Easy', 'Medium', 'Hard'"""
    # Hard: کامل (minimax)
    # Medium: گاهی (50%) از بهترین حرکت استفاده می‌کند، گاهی حرکت تصادفی
    # Easy: حرکت کاملاً تصادفی بین حرکات خوب/بد
    import random
    if difficulty == 'Easy':
        return random.choice(available_moves(board))
    elif difficulty == 'Medium':
        if random.random() < 0.5:
            _, mv = minimax(board, 0, True, -999, 999, AI, HUMAN)
            return mv
        else:
            return random.choice(available_moves(board))
    else:  # Hard
        _, mv = minimax(board, 0, True, -999, 999, AI, HUMAN)
        return mv

# ----- رابط گرافیکی (Tkinter) -----
class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe — Minimax AI")
        self.board = initial_board()
        self.buttons = [[None]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.turn = 'X'  # نماد کسی که نوبت دارد
        self.line_cells = []
        self.difficulty = tk.StringVar(value='Hard')  # سطح پیش‌فرض
        self.first_player = tk.StringVar(value='Human')  # Human یا Computer
        self.symbol_choice = tk.StringVar(value='X')  # نماد انسان
        self.create_widgets()
        self.reset_game(start_new=True)

    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(padx=10, pady=8)

        # گزینه‌ها
        tk.Label(top_frame, text="سطح سختی:").grid(row=0, column=0, sticky='w')
        tk.OptionMenu(top_frame, self.difficulty, 'Easy', 'Medium', 'Hard').grid(row=0, column=1, sticky='w')

        tk.Label(top_frame, text="شما:").grid(row=0, column=2, sticky='w', padx=(10,0))
        tk.OptionMenu(top_frame, self.symbol_choice, 'X', 'O').grid(row=0, column=3, sticky='w')

        tk.Label(top_frame, text="نوبت اول:").grid(row=0, column=4, sticky='w', padx=(10,0))
        tk.OptionMenu(top_frame, self.first_player, 'Human', 'Computer').grid(row=0, column=5, sticky='w')

        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        # بورد 3x3
        board_frame = tk.Frame(btn_frame)
        board_frame.grid(row=0, column=0, padx=10, pady=10)
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                b = tk.Button(board_frame, text='', font=('Arial', 36), width=4, height=2,
                              command=lambda r=r, c=c: self.human_move(r, c))
                b.grid(row=r, column=c, padx=4, pady=4)
                self.buttons[r][c] = b

        # کنترل‌ها
        control_frame = tk.Frame(btn_frame)
        control_frame.grid(row=0, column=1, sticky='n', padx=(10,0))
        tk.Button(control_frame, text="شروع دوباره", command=self.reset_game).pack(fill='x', pady=4)
        tk.Button(control_frame, text="حالت آموزشی (نمایش Minimax)", command=self.show_minimax_choice).pack(fill='x', pady=4)
        tk.Button(control_frame, text="خروج", command=self.root.quit).pack(fill='x', pady=4)

    def reset_game(self, start_new=False):
        global HUMAN, AI
        # تنظیم نمادها از UI
        HUMAN = self.symbol_choice.get()
        AI = 'O' if HUMAN == 'X' else 'X'
        self.board = initial_board()
        self.turn = 'X'  # X همیشه نماد نوبت‌دهی داخلی است
        self.line_cells = []
        # خالی کردن دکمه‌ها
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.buttons[r][c]['text'] = ''
                self.buttons[r][c]['state'] = 'normal'
                self.buttons[r][c]['bg'] = 'SystemButtonFace'
        # اگر کامپیوتر اول است، و انتخاب شده
        if start_new:
            # اگر کاربر قبلا المان‌ها را تغییر داده باشد هنوز اعمال می‌شود
            pass
        if self.first_player.get() == 'Computer':
            if AI == 'X':
                self.root.after(150, self.ai_turn)
            else:
                # اگر AI نماد O است ولی می‌خواهد اول بزند، AI با X نیست -> باید نقش اول را با نماد X بازی کند.
                # برای سادگی: وقتی "Computer" انتخاب شده و AI نماد O است، اجازه می‌دهیم Human نماد O باشد و Computer با X باشد.
                # اما در این کد AI نماد ثابت است (بر اساس symbol_choice)، بنابراین اگر کاربر انتخاب کند Computer اول و Human=X، 
                # اینجا کامپیوتر باید منتظر باشد تا user تغییر دهد. ساده‌ترین رفتار: اگر کاربر انتخاب کرده Human=X و first_player=Computer،
                # کامپیوتر حرکت می‌کند اما با نماد AI (که ممکن است O باشد). این طبیعی است: "اول بودن" مهم‌تر از نماد.
                self.root.after(150, self.ai_turn)

    def disable_all_buttons(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.buttons[r][c]['state'] = 'disabled'

    def human_move(self, r, c):
        # اگر نوبت انسان است و خانه خالی است
        if self.board[r][c] == EMPTY and self.turn == HUMAN:
            self.board[r][c] = HUMAN
            self.buttons[r][c]['text'] = HUMAN
            self.buttons[r][c]['state'] = 'disabled'
            over, winner, line = game_over(self.board)
            if over:
                self.end_game(winner, line)
                return
            # نوبت AI
            self.turn = AI
            self.root.after(150, self.ai_turn)

    def ai_turn(self):
        # اگر بازی تمام نشده و نوبت AI است
        if game_over(self.board)[0] or self.turn != AI:
            return
        mv = ai_move_by_difficulty(self.board, self.difficulty.get())
        if mv is None:
            # تساوی یا چیزی مشابه
            over, winner, line = game_over(self.board)
            self.end_game(winner, line)
            return
        r, c = mv
        self.board[r][c] = AI
        self.buttons[r][c]['text'] = AI
        self.buttons[r][c]['state'] = 'disabled'
        over, winner, line = game_over(self.board)
        if over:
            self.end_game(winner, line)
            return
        self.turn = HUMAN

    def end_game(self, winner, line):
        if winner:
            # هایلایت خط برنده
            for (r, c) in line:
                self.buttons[r][c]['bg'] = 'lightgreen'
            messagebox.showinfo("پایان بازی", f"برنده: {winner}")
        else:
            messagebox.showinfo("پایان بازی", "بازی مساوی شد.")
        self.disable_all_buttons()

    def show_minimax_choice(self):
        """نمایش حرکتِ پیشنهادی Minimax (برای حالت آموزشی)"""
        # فقط وقتی که بازی تمام نشده و نوبت Human است، حرکت پیشنهادی برای Human پیشنهاد می‌شود.
        # برای حالت آموزنده: نشان می‌دهیم Minimax برای AI چه حرکتی را بهترین می‌داند (اگر AI نوبت داشت).
        board_copy = copy.deepcopy(self.board)
        score, mv = minimax(board_copy, 0, True, -999, 999, AI, HUMAN)
        if mv:
            r, c = mv
            messagebox.showinfo("Minimax پیشنهاد می‌کند",
                                f"Minimax (AI) بهترین حرکت را اینجا می‌داند: ردیف {r+1}, ستون {c+1}\nامتیاز: {score}")
        else:
            messagebox.showinfo("Minimax", "حرکتی برای پیشنهاد وجود ندارد (بازی تمام است یا برابر).")

# ----- اجرای برنامه -----
def main():
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
