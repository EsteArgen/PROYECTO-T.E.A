
import threading
import time
from collections import deque
import sys
import random

# ======================== AI class =======================================
# state matrix and coordinate space
# ...w..w...
# ..........
# ..........
# w........w
# ..........
# ..........
# b........b
# ..........
# ..........
# ...b..b...
# 0------>y
# |
# |
# |
# x


class easyAI:
    def __init__(self, str_name):
        self.str = str_name

    def __str__(self):
        return self.str

    def isLose(self, state, str_name):
        tempStr = self.str
        self.str = str_name

        move_list = self.generate_move(state)
        self.str = tempStr

        if not move_list:
            return True
        return False

    def nextMove(self, state):
        start = time.time()
        move_list = self.generate_move(state)
        if not move_list:  # lose
            return []

        resultMove = move_list[random.randint(0, len(move_list) - 1)]
        return resultMove


    def generate_move(self, state):

        queen_list = deque()  # list for saving queen position
        move_list = deque()  # movement of queen
        resultList = deque()  # all posible movement

        for x in range(10):
            for y in range(10):
                if state[x][y] == self.str:
                    queen_list.append((x, y))

        while queen_list:
            (x, y) = queen_list.popleft()
            move = [[x, y]]

            for i in range(1, 10):
                if x - i < 0:
                    break
                elif state[x - i][y] == '.':
                    tempMove = list(move)
                    tempMove.append([x - i, y])

                    move_list.append(tempMove)
                else:
                    break

            for i in range(1, 10):
                if x + i > 9:
                    break
                elif state[x + i][y] == '.':
                    tempMove = list(move)
                    tempMove.append([x + i, y])

                    move_list.append(tempMove)
                else:
                    break

            for i in range(1, 10):
                if y - i < 0:
                    break
                elif state[x][y - i] == '.':
                    tempMove = list(move)
                    tempMove.append([x, y - i])

                    move_list.append(tempMove)
                else:
                    break

            for i in range(1, 10):
                if y + i > 9:
                    break
                elif state[x][y + i] == '.':
                    tempMove = list(move)
                    tempMove.append([x, y + i])

                    move_list.append(tempMove)
                else:
                    break


            for i in range(1, 10):
                if x - i < 0 or y - i < 0:
                    break
                elif state[x - i][y - i] == '.':
                    tempMove = list(move)
                    tempMove.append([x - i, y - i])

                    move_list.append(tempMove)
                else:
                    break

            for i in range(1, 10):
                if x - i < 0 or y + i > 9:
                    break
                elif state[x - i][y + i] == '.':
                    tempMove = list(move)
                    tempMove.append([x - i, y + i])

                    move_list.append(tempMove)
                else:
                    break


            for i in range(1, 10):
                if x + i > 9 or y - i < 0:
                    break
                elif state[x + i][y - i] == '.':
                    tempMove = list(move)
                    tempMove.append([x + i, y - i])

                    move_list.append(tempMove)
                else:
                    break


            for i in range(1, 10):
                if x + i > 9 or y + i > 9:
                    break
                elif state[x + i][y + i] == '.':
                    tempMove = list(move)
                    tempMove.append([x + i, y + i])

                    move_list.append(tempMove)
                else:
                    break

        for move in move_list:

            # change state
            new_board = self.board_copy(state)
            new_board[move[0][0]][move[0][1]] = '.'
            new_board[move[1][0]][move[1][1]] = self.str

            # generate arrow
            resultList.extend(self.shoot(move, new_board))
        

        return resultList

    def shoot(self, move, state):

        return_queue = deque()  # list of possible movement
        x = move[1][0]
        y = move[1][1]

        for i in range(1, 10):
            if x - i < 0:
                break
            elif state[x - i][y] == '.':
                tempMove = list(move)
                tempMove.append([x-i, y])
                return_queue.append(tempMove)
             
            else:
                break

        for i in range(1, 10):
            if x + i > 9:
                break
            elif state[x + i][y] == '.':
                tempMove = list(move)
                tempMove.append([x+i, y])
                return_queue.append(tempMove)
                
            else:
                break

        for i in range(1, 10):
            if y - i < 0:
                break
            elif state[x][y-i] == '.':
                tempMove = list(move)
                tempMove.append([x, y-i])
                return_queue.append(tempMove)
                
            else:
                break


        for i in range(1, 10):
            if y + i > 9:
                break
            elif state[x][y+i] == '.':
                tempMove = list(move)
                tempMove.append([x, y+i])
                return_queue.append(tempMove)
              
            else:
                break


        for i in range(1, 10):
            if x - i < 0 or y - i < 0:
                break
            elif state[x - i][y - i] == '.':
                tempMove = list(move)
                tempMove.append([x - i, y - i])
                return_queue.append(tempMove)
               
            else:
                break


        for i in range(1, 10):
            if x - i < 0 or y + i > 9:
                break
            elif state[x - i][y + i] == '.':
                tempMove = list(move)
                tempMove.append([x - i, y + i])
                return_queue.append(tempMove)
              
            else:
                break


        for i in range(1, 10):
            if x + i > 9 or y - i < 0:
                break
            elif state[x + i][y - i] == '.':
                tempMove = list(move)
                tempMove.append([x + i, y - i])
                return_queue.append(tempMove)
                
            else:
                break

        for i in range(1, 10):
            if x + i > 9 or y + i > 9:
                break
            elif state[x + i][y + i] == '.':
                tempMove = list(move)
                tempMove.append([x + i, y + i])
                return_queue.append(tempMove)
            else:
                break

        return return_queue

    def board_copy(self, board):
        new_board = [[]]*10
        for i in range(10):
            new_board[i] = [] + board[i]
        return new_board
