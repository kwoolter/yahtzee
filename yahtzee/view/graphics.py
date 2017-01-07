import pygame,os, sys
from pygame.locals import *
import yahtzee.utils.colours as colours


class MainFrame:

    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"

    def __init__(self, name : str, width : int = 800, height : int = 600):
        self.name = name
        self.surface = pygame.display.set_mode((width, height))

    def initialise(self):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.display.set_caption(self.name)
        filename = MainFrame.RESOURCES_DIR + self.name + ".jpg"
        image = pygame.image.load(filename)
        image = pygame.transform.scale(image, (32, 32))
        pygame.display.set_icon(image)

    def draw(self):
        self.surface.fill(colours.Colours.BLUE)

    def update(self):
        pygame.display.update()



if __name__ == "__main__":

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    frame = MainFrame("yahtzee", 400, 600)
    frame.initialise()

    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        frame.draw()
        frame.update()
