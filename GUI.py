import os.path
import tkinter as tk
import time
import pandas as pd
import random


def GUI():
    def check(game):
        # left-to-right and top-to-bottom
        if len(game) != 81:
            return False
        # row check
        for i in range(9):
            x = []
            for j in range(9):
                if game[i * 9 + j] != '0':
                    x.append(game[i * 9 + j])
            if len(x) != len(set(x)):
                return False
        # column check
        for i in range(9):
            x = []
            for j in range(9):
                if game[i + j * 9] != '0':
                    x.append(game[i + j * 9])
            if len(x) != len(set(x)):
                return False
        # square check
        for i in [0, 3, 6, 27, 30, 33, 54, 57, 60]:
            x = []
            for j in range(3):
                for k in range(3):
                    if game[i + j + k * 9] != '0':
                        x.append(game[i + j + k * 9])
            if len(x) != len(set(x)):
                return False
        return True

    def check_fill(game):
        if '0' in game:
            return False
        return True

    def recursion(game, ind, res):
        next_ind = ind
        if check(game) and check_fill(game):
            res.append(game)
            return

        for i in range(len(game)):
            if next_ind < i and game[i] == '0':
                next_ind = i
                break

        if next_ind == ind:
            return
        for i in range(1, 10):
            game = game[:next_ind] + str(i) + game[next_ind + 1:]
            res.append(game)
            if not check(game):
                continue

            recursion(game, next_ind, res)

    window = tk.Tk()
    window.title('sudoku')
    # window.geometry('1400x800')
    window.configure(bg='white')

    canvas = tk.Canvas(
        window,
        height=800,
        width=800,
        bg="#fff"
    )

    canvas.pack()

    start_i = 120
    start_j = 120
    w = 60
    text_list = []
    rec_list = []

    for i in range(9):
        for j in range(9):
            rec = canvas.create_rectangle(start_j + j * w, start_i + i * w, start_j + j * w + w, start_i + i * w + w, )
            t = canvas.create_text(start_j + j * w + w / 2, start_i + i * w + w / 2, text='', font=25)
            rec_list.append(rec)
            text_list.append(t)

    for i in range(3):
        for j in range(3):
            canvas.create_rectangle(start_j + j * w * 3, start_i + i * w * 3, start_j + j * w * 3 + w * 3,
                                    start_i + i * w * 3 + w * 3, outline='black', width=4)

    def update(s):
        for i in range(81):
            canvas.itemconfig(text_list[i], text=s[i])
        # time.sleep(0.5)

    problem = []
    button = tk.Button(window, text="New Puzzle", command=lambda: new_puzzle(problem))
    button.place(x=0, y=0)

    problem.append('070000043040009610800634900094052000358460020000800530080070091902100005007040802')
    problem.append('679518243543729618821634957794352186358461729216897534485276391962183475137945862')
    global keep
    keep = None


    # Download at https://www.kaggle.com/datasets/rohanrao/sudoku
    if os.path.isfile('./sudoku.csv'):
        df = pd.read_csv('./sudoku.csv')

        def new_puzzle(l):
            if keep:
                window.after_cancel(keep)
            num = random.randint(0, len(df) - 1)
            puzzle = df['puzzle'][num]
            solution = df['solution'][num]
            l[0] = puzzle
            l[1] = solution
            update(puzzle)
            for j in range(81):
                canvas.itemconfig(rec_list[j], fill='')

        new_puzzle(problem)
    else:
        def new_puzzle(l):
            puzzle = l[0]
            solution = l[1]
            update(puzzle)
            for j in range(81):
                canvas.itemconfig(rec_list[j], fill='')

    button = tk.Button(window, text="Solve", command=lambda: sel())
    button.place(x=0, y=40)

    def sel():
        l = []
        ori = problem[0]
        update(ori)
        recursion(ori, -1, l)
        index = 0

        def func(l, ind, pre):
            global keep
            if ind >= len(l):
                return
            update(l[ind])
            for j in range(81):
                if pre[j] == ori[j]:
                    canvas.itemconfig(rec_list[j], fill='')
                else:
                    canvas.itemconfig(rec_list[j], fill='orange')
            pre = l[ind]
            if check(l[ind]) and check_fill(l[ind]):
                return
            keep = window.after(100, lambda: func(l, ind + 1, pre))

        pre = ori
        func(l, 0, pre)

    answer = tk.Button(window, text="Show Answer", command=lambda: show_ans())

    answer.place(x=0, y=80)

    def show_ans():
        update(problem[1])
        if keep:
            window.after_cancel(keep)
        for j in range(81):
            if problem[0][j] == problem[1][j]:
                canvas.itemconfig(rec_list[j], fill='')
            else:
                canvas.itemconfig(rec_list[j], fill='orange')

    window.resizable(False, False)

    window.mainloop()


if __name__ == '__main__':
    GUI()
