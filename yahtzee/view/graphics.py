import pygame,os, sys
from pygame.locals import *
import yahtzee.utils.colours as colours


class MainFrame:

    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"

    def __init__(self, name : str, width : int = 800, height : int = 600):
        self.name = name
        self.surface = pygame.display.set_mode((width, height))

        self.turn_view = TurnView(200,100)

    def initialise(self):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.display.set_caption(self.name)
        filename = MainFrame.RESOURCES_DIR + self.name + ".jpg"
        image = pygame.image.load(filename)
        image = pygame.transform.scale(image, (32, 32))
        pygame.display.set_icon(image)

        self.turn_view.initialise()

    def draw(self):
        self.surface.fill(colours.Colours.BLUE)
        self.turn_view.draw()
        self.surface.blit(self.turn_view.surface, (10,10))

    def update(self):
        pygame.display.update()


class TurnView():
    DICE_WIDTH = 40
    DICE_HEIGHT = 40
    DICE_SPACING = 30

    def __init__(self, width : int = 300, height : int = 300):
        self.surface = pygame.Surface((width, height))
        self.rolled_dice = pygame.sprite.Group()
        self.held_dice = pygame.sprite.Group()

    def initialise(self):

        x = 10
        dice_view = SpriteView(x=x, image_file_name = "dice1.png", width=TurnView.DICE_WIDTH, height = TurnView.DICE_HEIGHT)
        self.rolled_dice.add(dice_view)
        x = dice_view.rect.right + TurnView.DICE_SPACING
        dice_view = SpriteView(x=x, image_file_name="dice2.png", width=TurnView.DICE_WIDTH, height=TurnView.DICE_HEIGHT)
        self.rolled_dice.add(dice_view)



    def draw(self):
        self.surface.fill(colours.Colours.RED)
        self.rolled_dice.draw(self.surface)
        self.held_dice.draw(self.surface)


class SpriteView(pygame.sprite.Sprite):

    def __init__(self, x : int = 0, y : int = 0, width : int = None, height : int = None, image_file_name : str = None):

        super(SpriteView, self).__init__()

        self._x=x
        self._y=y

        self.image_file_name = image_file_name

        if self.image_file_name is not None:
            filename = MainFrame.RESOURCES_DIR + self.image_file_name
            image = pygame.image.load(filename)

            if width is None:
                if height is None:
                    width = image.get_rect().width
                else:
                    width = int(image.get_rect().width * height/image.get_rect().height)
            if height is None:
                if width is None:
                    height = image.get_rect().height
                else:
                    height = int(image.get_rect().height * width/image.get_rect().width)

            self.image = pygame.transform.smoothscale(image, (width, height))
            self.original_image = self.image.copy()

        self.rect = self.image.get_rect()
        self.rect.x = int(self._x)
        self.rect.y = int(self._y)



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
