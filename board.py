from square import *
import pygame
import sys

# ======================================================================
Initial_Board = [
    ['.', '.', '.', 'w', '.', '.', 'w', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['w', '.', '.', '.', '.', '.', '.', '.', '.', 'w'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['b', '.', '.', '.', '.', '.', '.', '.', '.', 'b'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', 'b', '.', '.', 'b', '.', '.', '.'],
]

# Correspondencia entre las coordenadas del tablero y la representación en la lista.
# 9 : . . . b . . b . . .
# 8 : . . . . . . . . . .
# 7 : . . . . . . . . . .
# 6 : b . . . . . . . . b
# 5 : . . . . . . . . . .
# 4 : . . . . . . . . . .
# 3 : w . . . . . . . . w
# 2 : . . . . . . . . . .
# 1 : . . . . . . . . . .
# 0 : . . . w . . w . . .
#     0 1 2 3 4 5 6 7 8 9
# ======================================================================


class board():
    def __init__(self):
        self.square_gr = pygame.sprite.Group()
        a = square(point(0, 0), '.') # Instanciar para tener una referencia del cuadro 

        self.matrix = [
            [a, a, a, a, a, a, a, a, a, a],
            [a, a, a, a, a, a, a, a, a, a],
            [a, a, a, a, a, a, a, a, a, a],
            [a, a, a, a, a, a, a, a, a, a],
            [a, a, a, a, a, a, a, a, a, a],
            [a, a, a, a, a, a, a, a, a, a],
            [a, a, a, a, a, a, a, a, a, a],
            [a, a, a, a, a, a, a, a, a, a],
            [a, a, a, a, a, a, a, a, a, a],
            [a, a, a, a, a, a, a, a, a, a]
        ]

        for y in range(10):
            for x in range(10):
                temp = square(point(x, y), Initial_Board[y][x]) # Actualiza el valor de cada cuadro segun los elementos de la posicion inicial
                self.square_gr.add(temp)
                self.matrix[y][x] = temp

        self.state = 0 #  Esta variable almacena el estado actual del juego, que puede ser 0 (selección de Amazona), 1 (selección de destino) o 2 (selección de flecha)

        self.prePos = (-1, -1) # Guarda la posición previa seleccionada por el jugador. Inicialmente se establece en (-1, -1) para indicar que no se ha seleccionado nada.
        self.move = [(-1, -1), (-1, -1), (-1, -1)] # s una lista que almacena información sobre los movimientos realizados por el jugador. Cada elemento de la lista es una tupla que contiene información sobre las posiciones de la Amazona, el destino y la flecha seleccionados.

    def update(self, surface):
        self.square_gr.update()
        self.square_gr.draw(surface)

    def changeBoard(self, move):
        self.moveQueen(move[0], move[1])
        self.matrix[move[2][0]][move[2][1]].arrow()

    def toggleBoolValue(self, turnplayer):
        '''
        toggle bool value:
        +turnplayer param: bool value
        return: toggle value
        '''
        if turnplayer:
            return False
        else:
            return True

    def select(self, pos, player_str: str, turnplayer):
        # print(pos)
        for y in range(10):
            for x in range(10):
                # find square is checked by pointer
                if self.matrix[y][x].rect.collidepoint(pos[0], pos[1]):


                    # choose a queen to move
                    if self.matrix[y][x].state == player_str and self.state == 0:
                        self.recommendMove((y, x))
                        self.move[0] = (y, x)
                        self.state = (self.state + 1) % 3
                        return turnplayer

                    # choose queen destination to go
                    elif self.matrix[y][x].state == 'r' and self.state == 1:
                        self.clearRecommendMove()
                        self.moveQueen(self.move[0], (y, x))
                        self.recommendMove((y, x))
                        self.move[1] = (y, x)
                        # self.printMatrix()
                        self.state = (self.state + 1) % 3
                        return turnplayer

                    # choose arrow destination shoot
                    elif self.matrix[y][x].state == 'r' and self.state == 2:
                        self.clearRecommendMove()
                        self.matrix[y][x].arrow()
                        self.state = (self.state + 1) % 3
                        turnplayer = self.toggleBoolValue(turnplayer)
                        self.move[2] = (y, x)
                        # print(turnplayer)
                        # print(self.move)
                        return turnplayer

                    else:
                        return turnplayer

    def moveQueen(self, pos, des):
        self.matrix[des[0]][des[1]].setQueen(self.matrix[pos[0]][pos[1]].state)
        self.matrix[pos[0]][pos[1]].clearQueen()

    def clearRecommendMove(self):
        for y in range(10):
            for x in range(10):
                if self.matrix[y][x].state == 'r':
                    self.matrix[y][x].clearRecommend()

    def printMatrix(self):
        for y in range(10):
            for x in range(10):
                sys.stdout.write(self.matrix[y][x].state)
            print(" ")

    def convert2matrix(self): # Actualizaciòn del estado del tablero 
        '''
        convert to matrix of string: like initial_board format
        '''
        m = [
            ['.', '.', '.', 'w', '.', '.', 'w', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['w', '.', '.', '.', '.', '.', '.', '.', '.', 'w'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['b', '.', '.', '.', '.', '.', '.', '.', '.', 'b'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', 'b', '.', '.', 'b', '.', '.', '.'],
        ]

        for y in range(10):
            for x in range(10):
                m[y][x] = self.matrix[y][x].state

        return m

    def recommendMove(self, pos):
        (x, y) = pos

        # right
        for i in range(1, 10):
            if y + i > 9:
                break
            elif self.matrix[x][y+i].state == '.':
                self.matrix[x][y+i].recommended()
            else:
                break

        # left
        for i in range(1, 10):
            if y - i < 0:
                break
            elif self.matrix[x][y-i].state == '.':
                self.matrix[x][y-i].recommended()
            else:
                break

        # down
        for i in range(1, 10):
            if x + i > 9:
                break
            elif self.matrix[x+i][y].state == '.':
                self.matrix[x+i][y].recommended()
            else:
                break

        # top
        for i in range(1, 10):
            if x - i < 0:
                break
            elif self.matrix[x-i][y].state == '.':
                self.matrix[x-i][y].recommended()
            else:
                break

        # topleft
        for i in range(1, 10):
            if x - i < 0 or y - i < 0:
                break
            elif self.matrix[x-i][y-i].state == '.':
                self.matrix[x-i][y-i].recommended()
            else:
                break

        # downleft
        for i in range(1, 10):
            if x + i > 9 or y - i < 0:
                break
            elif self.matrix[x+i][y-i].state == '.':
                self.matrix[x+i][y-i].recommended()
            else:
                break

        # topright
        for i in range(1, 10):
            if x - i < 0 or y + i > 9:
                break
            elif self.matrix[x-i][y+i].state == '.':
                self.matrix[x-i][y+i].recommended()
            else:
                break

        # downright
        for i in range(1, 10):
            if x + i > 9 or y + i > 9:
                break
            elif self.matrix[x+i][y+i].state == '.':
                self.matrix[x+i][y+i].recommended()
            else:
                break
