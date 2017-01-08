import pygame,os, sys
from pygame.locals import *
import yahtzee.model.game as model
import yahtzee.view as view
import yahtzee.utils as utils

def main_loop():

    HOLD_KEYS = (K_1, K_2, K_3, K_4, K_5, K_6)
    UNHOLD_KEYS = (K_F1, K_F2, K_F3, K_F4, K_F5, K_F6)

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    game = model.Game()
    game.add_player(model.Player("Rosie"))
    game.add_player(model.Player("Jack"))
    #game.add_player(model.Player("Keith"))

    frame = view.MainFrame("yahtzee", 600, 700)
    frame.initialise(game)

    score_picker = view.ScorePickerView(300)
    score_picker.initialise(game)

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

                elif event.key == K_q:
                    try:
                        game.quit()
                    except Exception as err:
                        print(str(err))

                elif event.key == K_r:
                    try:
                        game.roll()
                    except Exception as err:
                        print(str(err))

                elif event.key == K_e:
                    try:
                        game.stop_rolling()
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

        if game.state != model.Game.GAME_READY and game.current_turn.state == model.Turn.LAST_ROLL_DONE:
            try:
                pane_rect = frame.surface.get_rect()
                available_scores = sorted(game.available_scores())
                choice = int(select_score_number(frame.surface, x = pane_rect.centerx, y = pane_rect.bottom - 30))
                print("You chose {0}. {1}".format(choice, available_scores[choice-1]))
                game.score_turn(available_scores[choice-1])
                game.next_player()
            except Exception as err:
                print(str(err))

        if game.state == model.Game.GAME_OVER:
            try:
                game.end()
            except Exception as err:
                print(str(err))


def select_score_number(surface, x, y):

    txtbx = utils.eztext.Input(maxlength=2, color=utils.Colours.WHITE, font=pygame.font.Font(None, 24),
                         x=x,
                         y=y,
                         prompt='Choice? ',
                         restricted = "0123456789")

    choice = None

    # create the pygame clock
    clock = pygame.time.Clock()
    # main loop!
    loop = True
    while loop:
        # make sure the program is running at 30 fps
        clock.tick(30)

        # events for txtbx
        events = pygame.event.get()
        # process other events
        for event in events:
            # close it x button is pressed
            if event.type == QUIT:
                loop = False
                break
            elif event.type == KEYDOWN and event.key == K_RETURN:
                print("Finished. Value={0}".format(txtbx.value))
                choice = txtbx.value
                loop = False
                break

        # update txtbx
        txtbx.update(events)
        # blit txtbx on the sceen
        txtbx.draw(surface)
        # refresh the display
        pygame.display.flip()

    return choice



if __name__ == "__main__":
    main_loop()
