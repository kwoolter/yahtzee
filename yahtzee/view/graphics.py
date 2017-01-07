import pygame,os, sys


class MainFrame:

    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"

    def __init__(self, name : str, width : int = 800, height : int = 600):
        self.name = name
        self.surface = pygame.display.set_mode((width, height))

    def initialise(self):
        pygame.init()
        pygame.display.set_caption(self.name)
        filename = MainFrame.RESOURCES_DIR + self.name + ".jpg"
        image = pygame.image.load(filename)
        image = pygame.transform.scale(image, (32, 32))
        pygame.display.set_icon(image)



    def draw(self):
        pass
