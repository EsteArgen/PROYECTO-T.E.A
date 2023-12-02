
import threading
import time
from collections import deque
import sys
import random
from easyAI import *

class hardAI(easyAI):
    def __init__(self, str_name):
        super().__init__(str_name)

    def nextMove(self, state):
        start_time = time.time()
        move_list = self.generate_move(state)

        if not move_list:  
            return []

        resultMove = self.valuation_func(state, move_list, True, start_time)

        return [resultMove[0], resultMove[1], resultMove[2]]

    def valuation_func(self, state, move_list, AI_turn, start_time):
        '''
        function calculate valuation function of a state

        +param-state: state
        +move-list: all posible movement of this state
        +AI_turn: true if turn of AI
        +start_time: to count time

        return: a movement have format: [[0,3],[5,3],[8,6],0]
        '''

        resultMove = []
        while move_list:

            move = move_list.popleft()
            new_board = self.board_copy(state)
            (x, y) = move[0]
            new_board[x][y] = '.'
            (x, y) = move[1]
            new_board[x][y] = self.str

        
            value_func = self.t1Func(new_board, AI_turn)

            if not resultMove:
                resultMove = [[move[0][0], move[0][1]], [
                    move[1][0], move[1][1]], [move[2][0], move[2][1]], value_func]

            if value_func > resultMove[3]:
                resultMove[0][0] = move[0][0]
                resultMove[0][1] = move[0][1]
                resultMove[1][0] = move[1][0]
                resultMove[1][1] = move[1][1]
                resultMove[2][0] = move[2][0]
                resultMove[2][1] = move[2][1]
                resultMove[3] = value_func

            elapse = time.time() - start_time
            
            if elapse > 2.9:
                return resultMove

        return resultMove

    def t1Func(self, state, AI_turn):  # for queen terrority
        value_t1 = 0

        if self.str == 'w':
            AI_state = self.queen_move(state, "w")
            opposite_state = self.queen_move(state, 'b')
        else:
            AI_state = self.queen_move(state, "b")
            opposite_state = self.queen_move(state, 'w')

        for i in range(10):
            for j in range(10):
                if state[i][j] == '.':
                    if AI_state[i][j] == opposite_state[i][j] and AI_state[i][j] == 100:
                        value_t1 += 0
                    elif AI_state[i][j] == opposite_state[i][j] and AI_turn:
                        value_t1 += 0.2
                    elif AI_state[i][j] == opposite_state[i][j] and not AI_turn:
                        value_t1 -= 0.2
                    elif AI_state[i][j] < opposite_state[i][j]:
                        value_t1 += 1
                    elif AI_state[i][j] > opposite_state[i][j]:
                        value_t1 -= 1
                    else:
                        value_t1 += 0  # do nothing

        return value_t1

    def t2Func(self, state, AI_turn):  # for king terrority
        value_t2 = 0

        if self.str == 'w':
            AI_state = self.king_move(state, "w")
            opposite_state = self.king_move(state, 'b')
        else:
            AI_state = self.king_move(state, "b")
            opposite_state = self.king_move(state, 'w')

        for i in range(10):
            for j in range(10):
                if state[i][j] == '.':
                    if AI_state[i][j] == opposite_state[i][j] and AI_state[i][j] == 100:
                        value_t2 += 0
                    elif AI_state[i][j] == opposite_state[i][j] and AI_turn:
                        value_t2 += 0.2
                    elif AI_state[i][j] == opposite_state[i][j] and not AI_turn:
                        value_t2 -= 0.2
                    elif AI_state[i][j] < opposite_state[i][j]:
                        value_t2 += 1
                    elif AI_state[i][j] > opposite_state[i][j]:
                        value_t2 -= 1
                    else:
                        value_t2 += 0  # do nothing


        return value_t2

    def queen_move(self, state, site):
        new_board = self.board_copy(state)
        queue = deque()  # very important structure
        number_interation = 0

        for i in range(10):
            for j in range(10):
                if new_board[i][j] == site:
                    queue.append((i, j, 0))

        while True:
            number_interation += 1

            while queue:
                (i, j, numberMove) = queue.popleft()

                if numberMove != 0:
                    new_board[i][j] = numberMove

                for index in range(1, 10):
                    if i-index < 0:
                        break
                    if new_board[i-index][j] == 'X' or new_board[i-index][j] == 'b' or new_board[i-index][j] == 'w':
                        break
                    if i-index >= 0 and new_board[i-index][j] == '.':
                        new_board[i-index][j] = 't'

                for index in range(1, 10):
                    if i+index > 9:
                        break
                    if new_board[i+index][j] == 'X' or new_board[i+index][j] == 'b' or new_board[i+index][j] == 'w':
                        break
                    if i+index <= 9 and new_board[i+index][j] == '.':
                        new_board[i+index][j] = 't'

                for index in range(1, 10):
                    if j-index < 0:
                        break
                    if new_board[i][j-index] == 'X' or new_board[i][j-index] == 'b' or new_board[i][j-index] == 'w':
                        break
                    if j-index >= 0 and new_board[i][j-index] == '.':
                        new_board[i][j-index] = 't'

                for index in range(1, 10):
                    if j+index > 9:
                        break
                    if new_board[i][j+index] == 'X' or new_board[i][j+index] == 'b' or new_board[i][j+index] == 'w':
                        break
                    if j+index <= 9 and new_board[i][j+index] == '.':
                        new_board[i][j+index] = 't'

                for index in range(1, 10):
                    if i-index < 0 or j-index < 0:
                        break
                    if new_board[i-index][j-index] == 'X' or new_board[i-index][j-index] == 'b' or new_board[i-index][j-index] == 'w':
                        break
                    if i-index >= 0 and j-index >= 0 and new_board[i-index][j-index] == '.':
                        new_board[i-index][j-index] = 't'

                for index in range(1, 10):
                    if i-index < 0 or j+index > 9:
                        break
                    if new_board[i-index][j+index] == 'X' or new_board[i-index][j+index] == 'b' or new_board[i-index][j+index] == 'w':
                        break
                    if i-index >= 0 and j+index <= 9 and new_board[i-index][j+index] == '.':
                        new_board[i-index][j+index] = 't'

                for index in range(1, 10):
                    if i+index > 9 or j-index < 0:
                        break
                    if new_board[i+index][j-index] == 'X' or new_board[i+index][j-index] == 'b' or new_board[i+index][j-index] == 'w':
                        break
                    if i+index <= 9 and j-index >= 0 and new_board[i+index][j-index] == '.':
                        new_board[i+index][j-index] = 't'

                for index in range(1, 10):
                    if i+index > 9 or j+index > 9:
                        break
                    if new_board[i+index][j+index] == 'X' or new_board[i+index][j+index] == 'b' or new_board[i+index][j+index] == 'w':
                        break
                    if i+index <= 9 and j+index <= 9 and new_board[i+index][j+index] == '.':
                        new_board[i+index][j+index] = 't'

            for i in range(10):
                for j in range(10):
                    if new_board[i][j] == 't':
                        queue.append((i, j, number_interation))

            if not queue:
                break

        for i in range(10):
            for j in range(10):
                if new_board[i][j] == '.':
                    # 100 stand for infinity, its mean the queen can't go to this place
                    new_board[i][j] = 100

        return new_board

    def king_move(self, state, site):

        new_board = self.board_copy(state)
        queue = deque()  # very important structure
        number_interation = 0

        for i in range(10):
            for j in range(10):
                if new_board[i][j] == site:
                    queue.append((i, j, 0))

        while True:
            number_interation += 1
            while queue:
                (i, j, numberMove) = queue.popleft()

                if numberMove != 0:
                    new_board[i][j] = numberMove

                if i-1 >= 0 and new_board[i-1][j] == '.':
                    new_board[i-1][j] = 't'
                if i+1 <= 9 and new_board[i+1][j] == '.':
                    new_board[i+1][j] = 't'
                if j-1 >= 0 and new_board[i][j-1] == '.':
                    new_board[i][j-1] = 't'
                if j+1 <= 9 and new_board[i][j+1] == '.':
                    new_board[i][j+1] = 't'
                if i-1 >= 0 and j-1 >= 0 and new_board[i-1][j-1] == '.':
                    new_board[i-1][j-1] = 't'
                if i-1 >= 0 and j+1 <= 9 and new_board[i-1][j+1] == '.':
                    new_board[i-1][j+1] = 't'
                if i+1 <= 9 and j-1 >= 0 and new_board[i+1][j-1] == '.':
                    new_board[i+1][j-1] = 't'
                if i+1 <= 9 and j+1 <= 9 and new_board[i+1][j+1] == '.':
                    new_board[i+1][j+1] = 't'

            for i in range(10):
                for j in range(10):
                    if new_board[i][j] == 't':
                        queue.append((i, j, number_interation))

            if not queue:
                break

        for i in range(10):
            for j in range(10):
                if new_board[i][j] == '.':
                    # 100 stand for infinity, its mean the queen can't go to this place
                    new_board[i][j] = 100
  
        return new_board

    def board_copy(self, board):
        new_board = [[]]*10
        for i in range(10):
            new_board[i] = [] + board[i]
        return new_board

    def board_print(self, board):
        for y in range(10):
            for x in range(10):
                sys.stdout.write(board[y][x])
            print(" ")
