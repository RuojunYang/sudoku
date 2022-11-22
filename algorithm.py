import os
import numpy as np
import pandas as pd


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
        if not check(game):
            continue

        recursion(game, next_ind, res)


if __name__ == '__main__':
    # https://www.kaggle.com/datasets/rohanrao/sudoku
    df = pd.read_csv('sudoku.csv')

    #070000043040009610800634900094052000358460020000800530080070091902100005007040802
    #679518243543729618821634957794352186358461729216897534485276391962183475137945862
    for i in range(5):
        l = []
        ori = df['puzzle'][i]
        recursion(ori, -1, l)
        print(l[0] == df['solution'][i])
