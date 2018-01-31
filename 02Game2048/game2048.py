# -*- coding: utf-8 -*-

import curses
from random import randrange, choice
from collections import defaultdict

letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']#将字母转化成ascii码
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
actions_dict = dict(zip(letter_codes, actions*2)) # 用映射的方式构建字典

def get_user_action(keyboard):
    #获取用户操作
    char = "N"
    while char not in actions_dict:
        char = keyboard.getch()
    return actions_dict[char]

def transponse(field):
    return [list(row) for row in zip(*field)]#zip*，转置

def invert(field):
    return [row[::-1] for row in field]#list[::-1]为数组倒序

class GameField(object):
    def __init__(self, height=4, width=4, win=2048):
        self.height = height
        self.width = width
        self.win_num = win #设定多少为胜利
        self.score = 0 #初始化分数
        self.highscore = 0
        self.reset()

    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score #最高分记录
        self.score = 0
        self.field = [[0 for i in range(self.width)] for j in range(self.height)] #棋盘初始化，最初都是0
        self.spawn()
        self.spawn()# 产生两个随机数

    def move(self, direction):
        def move_row_left(row):
            def tighten(row):
                new_row = [i for i in row if i!=0]#有数字的地方全部过去
                new_row += [0 for i in range(len(row)-len(new_row))]#剩下的地方为空
                return new_row
            def merge(row):
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2*row[i])
                        self.score += 2*row[i]
                        pair = False
                    else:
                        if i+1 < len(row) and row[i]==row[i+1]:#如果需要融合
                            pair = True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row
            return tighten(merge(tighten(row)))#先聚拢，再融合，再聚拢

        moves = {}
        moves['Left'] = lambda field: [move_row_left(row) for row in field]
        moves['Right'] = lambda field: invert(moves['Left'](invert(field)))
        moves['Up'] = lambda field: transponse(moves['Left'](transponse(field)))
        moves['Down'] = lambda field: transponse(moves['Right'](transponse(field)))

        if direction in moves:
            if self.move_is_possible(direction):#先判断这个方向是否可以移动
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False

    def is_win(self):
        return any(any(i >= self.win_num for i in row) for row in self.field)#当有任何一个数字大于win

    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in actions)#当所有方向都满了

    def draw(self, screen):
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '    (R)Restart (Q)Exit'
        gameover_string = '         GAME OVER!'
        win_string = '          YOU WIN!'
        def cast(string):
            screen.addstr(string + '\n')

        def draw_hor_separator():
            line = '+' + ('+------' * self.width + '+')[1:]
            separator = defaultdict(lambda: line)
            if not hasattr(draw_hor_separator, "counter"):
                draw_hor_separator.counter = 0
            cast(separator[draw_hor_separator.counter])
            draw_hor_separator.counter += 1

        def draw_row(row):
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|    ' for num in row) + '|')

        screen.clear()
        cast('SCORE: ' + str(self.score))

        if 0!=self.highscore:
            cast('HIGHSCORE: '+str(self.highscore) )
        for row in self.field:
            draw_hor_separator()
            draw_row(row)
        draw_hor_separator()
        if self.is_win():
            cast(win_string)
        else:
            if self.is_gameover():
                cast(gameover_string)
            else:
                cast(help_string1)
        cast(help_string2)

    def spawn(self):
        new_element = 4 if randrange(100)>89 else 2
        (i, j) = choice([(i,j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    def move_is_possible(self, direction):
        def row_is_left_movable(row):
            def change(i):
                if row[i]==0 and row[i+1] != 0:
                    return True
                if row[i]!=0 and row[i+1]==row[i]:
                    return True
                return False
            return any(change(i) for i in range(len(row)-1))

        check = {}
        check['Left'] = lambda field: any(row_is_left_movable(row) for row in field)
        check['Right'] = lambda field: check['Left'](invert(field))
        check['Up'] = lambda field: check['Left'](transponse(field))
        check['Down'] = lambda field: check['Right'](transponse(field))

        if direction in check:
            return check[direction](self.field)
        else:
            return False

def main(stdscr):
    def init():
        game_field.reset()
        return 'Game'

    def not_game(state):
        game_field.draw(stdscr)
        action = get_user_action(stdscr)
        responses = defaultdict(lambda: state)
        responses['Restart'] = 'Init'
        responses['Exit'] = 'Exit'
        return responses[action]

    def game():
        game_field.draw(stdscr)
        action = get_user_action(stdscr)

        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action):
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game'

    state_actions = {
        'Init': init,
        'Win': lambda: not_game('Win'),
        'Gameover': lambda: not_game('Gameover'),
        'Game': game
    }

    game_field = GameField(win=32)

    state = 'Init'

    while state != 'Exit':
        state = state_actions[state]()

curses.wrapper(main)
