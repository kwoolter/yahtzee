import pygame,os, sys
from pygame.locals import *
import yahtzee.utils.colours as colours
import yahtzee.model.game as model


class MainFrame:

    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"
    PANE_PACING = 10

    def __init__(self, name : str, width : int = 800, height : int = 800):
        self.name = name
        self.game = None
        self.surface = pygame.display.set_mode((width, height))

        self.turn_view = TurnView(width = width - MainFrame.PANE_PACING*2)
        self.score_view = ScoreView(width = width - MainFrame.PANE_PACING*2)

    def initialise(self, game : model.Game):
        self.game = game

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.display.set_caption(self.name)
        filename = MainFrame.RESOURCES_DIR + self.name + ".jpg"
        image = pygame.image.load(filename)
        image = pygame.transform.scale(image, (32, 32))
        pygame.display.set_icon(image)

        self.turn_view.initialise(self.game)
        self.score_view.initialise(self.game)

    def draw(self):

        self.surface.fill(colours.Colours.GREEN)

        x=MainFrame.PANE_PACING
        y=MainFrame.PANE_PACING

        self.turn_view.draw()
        self.surface.blit(self.turn_view.surface, (x,y))

        y+=self.turn_view.surface.get_rect().height + MainFrame.PANE_PACING

        self.score_view.draw()
        self.surface.blit(self.score_view.surface, (x,y))

    def update(self):
        pygame.display.update()

class ScoreView:

    TITLE_HEIGHT = 50
    HEADER_HEIGHT = 20
    HEADER_WIDTH = 120
    SCORE_HEIGHT = 20
    SCORE_WIDTH = 150
    PADDING = 5
    SCORE_TEXT_HEIGHT = 20

    def __init__(self, width : int = 500, height : int = None):

        self.game = None

        if height is None:
            height = ScoreView.TITLE_HEIGHT + ScoreView.HEADER_HEIGHT + (ScoreView.SCORE_HEIGHT + ScoreView.PADDING) * 16

        self.surface = pygame.Surface((width, height))

    def initialise(self, game : model.Game):
        self.game = game

    def draw(self):
        if self.game is None:
            raise Exception("No game to view!!!")

        self.surface.fill(colours.Colours.BLUE)

        if self.game.state == model.Game.GAME_PLAYING:

            draw_text(self.surface,"  Scores  ({0})  ".format(model.Game.STATE[self.game.state]),
                      self.surface.get_rect().centerx, ScoreView.TITLE_HEIGHT/2)

        # Game to update current leaders
        self.game.calc_leaders()

        x = ScoreView.PADDING * 2 + ScoreView.SCORE_WIDTH + ScoreView.HEADER_WIDTH/2
        y = ScoreView.TITLE_HEIGHT + ScoreView.PADDING

        for player in self.game.players:
            if player in self.game.winners:
                bg_colour = colours.Colours.RED
            else:
                bg_colour = colours.Colours.BLUE

            draw_text(self.surface,"  {0}  ".format(player.name), bg_colour=bg_colour, x=x,y=y)
            x += ScoreView.HEADER_WIDTH + ScoreView.PADDING

        y = ScoreView.TITLE_HEIGHT + ScoreView.HEADER_HEIGHT + ScoreView.PADDING*2

        # Print upper section scores
        for i in range(1,7):

            x = ScoreView.PADDING + ScoreView.SCORE_WIDTH/2

            score_type = "{0}'s".format(i)
            draw_text(self.surface,x=x,y=y,msg="{0}'s".format(i),
                      fg_colour=colours.Colours.BLACK,
                      bg_colour=colours.Colours.BLUE,
                      size = ScoreView.SCORE_HEIGHT)

            for player in self.game.players:

                x += ScoreView.HEADER_WIDTH + ScoreView.PADDING

                if player.name in self.game.player_scores.keys():
                    player_scores = self.game.player_scores[player.name]
                    if score_type in player_scores.keys():
                        score = player_scores[score_type]
                        bg_colour = colours.Colours.BLUE
                        fg_colour = colours.Colours.BLACK
                    else:
                        score = "-"
                        bg_colour = colours.Colours.BLUE
                        fg_colour = colours.Colours.WHITE


                    draw_text(self.surface,msg = "{0}".format(score), x=x,y=y,
                              bg_colour=bg_colour,
                              fg_colour=fg_colour,
                              size = ScoreView.SCORE_HEIGHT)
                else:
                    draw_text(self.surface,msg = "-", x=x,y=y,
                              bg_colour=colours.Colours.BLUE,
                              fg_colour=colours.Colours.WHITE,
                              size=ScoreView.SCORE_HEIGHT)

            y += ScoreView.SCORE_HEIGHT + ScoreView.PADDING

        # Print lower section scores
        lower_score_types = (model.Scores.UPPER_TOTAL_BONUS,
                             model.Scores.THREE_OF_A_KIND,
                             model.Scores.FOUR_OF_A_KIND,
                             model.Scores.FULL_HOUSE,
                             model.Scores.SMALL_RUN,
                             model.Scores.LARGE_RUN,
                             model.Scores.YAHTZEE,
                             model.Scores.CHANCE,
                             model.Scores.YAHTZEE_MULTI_BONUS)

        for score_type in lower_score_types:

            x = ScoreView.PADDING + ScoreView.SCORE_WIDTH/2

            draw_text(self.surface, msg="{0}".format(score_type), x=x, y=y,
                      bg_colour=colours.Colours.BLUE,
                      fg_colour=colours.Colours.WHITE,
                      size=ScoreView.SCORE_HEIGHT)

            for player in self.game.players:

                x += ScoreView.HEADER_WIDTH + ScoreView.PADDING

                if player.name in self.game.player_scores.keys():
                    player_scores = self.game.player_scores[player.name]
                    if score_type in player_scores.keys():
                        score = player_scores[score_type]
                        bg_colour = colours.Colours.BLUE
                        fg_colour = colours.Colours.BLACK
                    else:
                        score = "-"
                        bg_colour = colours.Colours.BLUE
                        fg_colour = colours.Colours.WHITE

                    draw_text(self.surface, msg="{0}".format(score), x=x, y=y,
                              bg_colour=bg_colour,
                              fg_colour=fg_colour,
                              size=ScoreView.SCORE_HEIGHT)

                else:
                    draw_text(self.surface,msg = "-", x=x,y=y,
                              bg_colour=colours.Colours.BLUE,
                              fg_colour=colours.Colours.WHITE,
                              size=ScoreView.SCORE_HEIGHT)

            y += ScoreView.SCORE_HEIGHT + ScoreView.PADDING

class TurnView:

    DICE_WIDTH = 60
    DICE_HEIGHT = 60
    DICE_SPACING = 10
    HEADER_HEIGHT = 30

    def __init__(self, width : int = 500, height : int = None):

        if height is None:
            height = TurnView.HEADER_HEIGHT + TurnView.DICE_SPACING * 3 + TurnView.DICE_HEIGHT * 2

        self.surface = pygame.Surface((width, height))


    def initialise(self, game : model.Game):

        self.game = game

    def draw(self):
        if self.game is None:
            raise Exception("No game to view!!!")

        self.surface.fill(colours.Colours.RED)
        rolled_dice = pygame.sprite.Group()
        held_dice = pygame.sprite.Group()

        if self.game.state == model.Game.GAME_PLAYING:

            draw_text(self.surface,"  Player {0}: {1}, roll {2}  ".format(self.game.current_player.name,
                                                                        model.Turn.state_to_text[self.game.current_turn.state],
                                                                        self.game.current_turn.rolls),
                      self.surface.get_rect().centerx,
                      TurnView.HEADER_HEIGHT/2)

            x = TurnView.DICE_SPACING
            y = TurnView.HEADER_HEIGHT + TurnView.DICE_SPACING

            for dice in self.game.current_turn.current_roll:
                dice_view = SpriteView(x=x, y=y, image_file_name = "dice" + str(dice) + ".png", width=TurnView.DICE_WIDTH, height = TurnView.DICE_HEIGHT)
                rolled_dice.add(dice_view)
                x = dice_view.rect.right + TurnView.DICE_SPACING

            x = TurnView.DICE_SPACING
            y = TurnView.HEADER_HEIGHT + TurnView.DICE_HEIGHT + TurnView.DICE_SPACING * 2

            for dice in self.game.current_turn.slots:
                dice_view = SpriteView(x=x, y=y, image_file_name="dice" + str(dice) + ".png",
                                       width=TurnView.DICE_WIDTH, height=TurnView.DICE_HEIGHT)
                rolled_dice.add(dice_view)
                x = dice_view.rect.right + TurnView.DICE_SPACING

            rolled_dice.draw(self.surface)
            held_dice.draw(self.surface)



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


def draw_text(surface, msg, x, y, size=32, fg_colour=colours.Colours.WHITE, bg_colour=colours.Colours.BLACK):
    font = pygame.font.Font(None, size)
    text = font.render(msg, 1, fg_colour, bg_colour)
    textpos = text.get_rect()
    textpos.centerx = x
    textpos.centery = y
    surface.blit(text, textpos)


def main_loop():

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    game = model.Game()
    game.add_player(model.Player("Rosie"))
    game.add_player(model.Player("Jack"))
    game.add_player(model.Player("Keith"))

    frame = MainFrame("yahtzee", 600, 700)
    frame.initialise(game)

    FPSCLOCK = pygame.time.Clock()

    HOLD_KEYS = (K_1, K_2, K_3, K_4, K_5, K_6)
    UNHOLD_KEYS = (K_F1, K_F2, K_F3, K_F4, K_F5, K_F6)

    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == (K_SPACE):
                    try:
                        game.start()
                    except Exception as err:
                        print(str(err))

                elif event.key == (K_r):
                    try:
                        game.roll()
                    except Exception as err:
                        print(str(err))

                elif event.key == (K_e):
                    try:
                        game.end_turn()
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