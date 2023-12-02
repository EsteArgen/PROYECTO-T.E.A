from pygame.locals import *
import pygame
from random import randrange
import os
import time
import pygameMenu
from pygameMenu.locals import *
from const import *
from square import *
from point import *
from board import *
from hardAI import *
from easyAI import *

# -----------------------------------------------------------------------------

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Create pygame screen and objects
surface = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('¡The game of amazons!')
clock = pygame.time.Clock()
dt = 1 / FPS
DIFFICULTY = ['EASY']
MOVE_FIRST = ['YES']

# -----------------------------------------------------------------------------

def change_difficulty(d):
    """
    Change difficulty of the game.

    :return: 
    """
    DIFFICULTY[0] = d

def change_moveFirst(d):
    """
    choose your turn is first or second

    :return: 
    """
    MOVE_FIRST[0] = d


def random_color():
    """
    Return random color.

    :return: Color tuple
    """
    return randrange(0, 255), randrange(0, 255), randrange(0, 255)


def personModePlay(difficulty, font):
    """
    person mode play function

    :param difficulty: Difficulty of the game
    :param font: Pygame font
    :return: None
    """
    difficulty = difficulty[0]
    assert isinstance(difficulty, str)

    turnPlayer1 = True
    nboard = board()
    
    main_menu.disable()
    main_menu.reset(1)

    while True:

        clock.tick(60)

        playevents = pygame.event.get()
        for e in playevents:
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE and main_menu.is_disabled():
                    main_menu.enable()

                    return
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if turnPlayer1:
                    turnPlayer1 = nboard.select(
                        pygame.mouse.get_pos(), 'w', turnPlayer1)
                else:
                    turnPlayer1 = nboard.select(
                        pygame.mouse.get_pos(), 'b', turnPlayer1)

        main_menu.mainloop(playevents)

       
        nboard.update(surface)

       
        pygame.display.flip()


def AImodePlay(difficulty, font):
    """
    AI mode play function

    :param difficulty: Difficulty of the game
    :param font: Pygame font
    :return: None
    """
    difficulty = difficulty[0]
    assert isinstance(difficulty, str)

    bot = None
    personTurn = True
    nboard = board()

    if difficulty == 'EASY':
        f = font.render('easy', 1, COLOR_WHITE)
        bot = easyAI('b')
    elif difficulty == 'HARD':
        f = font.render('hard', 1, COLOR_WHITE)
        bot = hardAI('b')
    else:
        raise Exception('Unknown difficulty {0}'.format(difficulty))

    f_width = f.get_size()[0]

    main_menu.disable()
    main_menu.reset(1)
    
    while True:

        clock.tick(60)

        playevents = pygame.event.get()
        for e in playevents:
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE and main_menu.is_disabled():
                    main_menu.enable()

                    return

        if personTurn:
    
            for e in playevents:
                if e.type == pygame.MOUSEBUTTONDOWN:                  
                    personTurn = nboard.select(
                        pygame.mouse.get_pos(), 'w', personTurn)
        else:
            tempState = nboard.convert2matrix()
            move = bot.nextMove(tempState)
         
            if not move:
                f = font.render('you win!!!', 1, COLOR_WHITE)
            else:
                for i in range(3):
                    pos = (move[i][1] * (SQUARE_SIZE + 5), move[i][0] * (SQUARE_SIZE + 5))
                    personTurn = nboard.select(pos,'b', personTurn)
        
            
                    nboard.update(surface)

                    surface.blit(f, ((WINDOW_SIZE[0] - f_width) / 2, WINDOW_SIZE[1] / 2))
                    pygame.display.flip()
                    time.sleep(1)
        
        main_menu.mainloop(playevents)

      
        nboard.update(surface)

    
        surface.blit(f, ((WINDOW_SIZE[0] - f_width) / 2, WINDOW_SIZE[1] / 2))
        pygame.display.flip()


def main_background():
    """
    Function used by menus, draw on background while menu is active.

    :return: None
    """
    surface.fill(COLOR_BACKGROUND)


# -----------------------------------------------------------------------------

play_menu = pygameMenu.Menu(surface,
                            bgfun=main_background,
                            color_selected=COLOR_WHITE,
                            font=pygameMenu.fonts.FONT_BEBAS,
                            font_color=COLOR_BLACK,
                            font_size=30,
                            menu_alpha=100,
                            menu_color=MENU_BACKGROUND_COLOR,
                            menu_height=int(WINDOW_SIZE[1] * 0.6),
                            menu_width=int(WINDOW_SIZE[0] * 0.6),
                            onclose=PYGAME_MENU_DISABLE_CLOSE,
                            option_shadow=False,
                            title='Play menu',
                            window_height=WINDOW_SIZE[1],
                            window_width=WINDOW_SIZE[0]
                            )
# When pressing return -> play(DIFFICULTY[0], font)
play_menu.add_option('Start', AImodePlay, DIFFICULTY,
                     pygame.font.Font(pygameMenu.fonts.FONT_FRANCHISE, 30))
play_menu.add_selector('Select difficulty', [('Easy', 'EASY'),
                                             ('Hard', 'HARD')],
                       onreturn=None,
                       onchange=change_difficulty)
play_menu.add_option('Return to main menu', PYGAME_MENU_BACK)


main_menu = pygameMenu.Menu(surface,
                            bgfun=main_background,
                            color_selected=COLOR_WHITE,
                            font=pygameMenu.fonts.FONT_BEBAS,
                            font_color=COLOR_BLACK,
                            font_size=30,
                            menu_alpha=100,
                            menu_color=MENU_BACKGROUND_COLOR,
                            menu_height=int(WINDOW_SIZE[1] * 0.6),
                            menu_width=int(WINDOW_SIZE[0] * 0.6),
                            onclose=PYGAME_MENU_DISABLE_CLOSE,
                            option_shadow=False,
                            title='Main menu',
                            window_height=WINDOW_SIZE[1],
                            window_width=WINDOW_SIZE[0]
                            )
main_menu.add_option('Human - Machine', play_menu)
main_menu.add_option('Human - Human', personModePlay, DIFFICULTY,
                     pygame.font.Font(pygameMenu.fonts.FONT_FRANCHISE, 30))
main_menu.add_option('About', PYGAME_MENU_EXIT)

# -----------------------------------------------------------------------------

while True:

    clock.tick(60)

    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            exit()

    main_menu.mainloop(events)

    pygame.display.flip()
