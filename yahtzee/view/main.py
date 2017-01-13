import logging, os, sys
import pygame
from pygame.locals import *
from yahtzee.utils.colours import *
import yahtzee.model.game as game

RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"
DATA_DIR  = os.path.dirname(__file__) + "\\data\\"

def main():

    logging.basicConfig(level=logging.WARN)
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()

    # Set-up the game window
    pygame.display.set_caption('YAHTZEE')
    filename = RESOURCES_DIR + "yahtzee.jpg"
    image = pygame.image.load(filename)
    image = pygame.transform.scale(image, (32, 32))
    pygame.display.set_icon(image)

    DISPLAYSURF = pygame.display.set_mode((800, 640))

    pygame.time.set_timer(USEREVENT + 1, 500)

    yahtzee = game.Game()

    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == USEREVENT + 1:
                pass
            elif event.type == KEYDOWN:
                pass

        # draw on the surface object
        DISPLAYSURF.fill(Colours.GREY)

        pygame.display.update()

    #The end of main()
    return


if __name__ == "__main__":
    main()