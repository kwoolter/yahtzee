import pygame,os, sys
from pygame.locals import *
import yahtzee.model.game as model
import yahtzee.view as view

def main_loop():

    HOLD_KEYS = (K_1, K_2, K_3, K_4, K_5, K_6)
    UNHOLD_KEYS = (K_F1, K_F2, K_F3, K_F4, K_F5, K_F6)

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    game = model.Game()
    game.add_player(model.Player("Rosie"))
    game.add_player(model.Player("Jack"))
    game.add_player(model.Player("Keith"))

    frame = view.MainFrame("yahtzee", 600, 700)
    frame.initialise(game)

    FPSCLOCK = pygame.time.Clock()

    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    try:
                        game.start()
                    except Exception as err:
                        print(str(err))

                elif event.key == K_r:
                    try:
                        game.roll()
                    except Exception as err:
                        print(str(err))

                elif event.key == K_e:
                    try:
                        game.end_turn()
                    except Exception as err:
                        print(str(err))

                elif event.key == K_s:
                    try:
                        game.score_turn("1's")
                    except Exception as err:
                        print(str(err))

                elif event.key in HOLD_KEYS:
                    dice_number = HOLD_KEYS.index(event.key) + 1
                    try:
                        game.hold(dice_number)
                    except Exception as err:
                        print(str(err))

                elif event.key in UNHOLD_KEYS:
                    dice_number = UNHOLD_KEYS.index(event.key) + 1
                    try:
                        game.unhold(dice_number)
                    except Exception as err:
                        print(str(err))

        FPSCLOCK.tick(30)
        frame.draw()
        frame.update()


if __name__ == "__main__":
    main_loop()