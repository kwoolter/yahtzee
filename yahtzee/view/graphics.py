import pygame, os, sys, random
from pygame.locals import *
import yahtzee.utils.colours as colours
import yahtzee.model.game as model
import yahtzee.utils as utils


class MainFrame:

    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"
    PANE_PADDING = 5

    def __init__(self, name: str, width: int = 800, height: int = 800):
        self.name = name
        self.game = None
        self.surface = pygame.display.set_mode((width, height))

        self.turn_view = TurnView(width=width - MainFrame.PANE_PADDING * 2)
        self.score_view = ScoreView(width=width - MainFrame.PANE_PADDING * 2)
        self.score_picker = ScorePickerView(width=width - MainFrame.PANE_PADDING * 2,
                                            height=self.score_view.surface.get_height())
        self.hst = HighScoreTableView(width=width - MainFrame.PANE_PADDING * 2,
                                      height=self.score_view.surface.get_height())

        self.game_over = GameOverView(width = width, height = self.turn_view.surface.get_height())

    def initialise(self, game: model.Game):
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
        self.score_picker.initialise(self.game)
        self.hst.initialise(self.game.hst)
        self.game_over.inititalise(self.game)

    def tick(self):
        self.score_view.tick()
        self.turn_view.tick()
        self.hst.tick()
        self.game_over.tick()


    def draw(self):

        self.surface.fill(colours.Colours.BLACK)

        pane_rect = self.surface.get_rect()

        x=MainFrame.PANE_PADDING

        if self.game.state == model.Game.GAME_PLAYING:


            y = MainFrame.PANE_PADDING

            self.turn_view.draw()
            self.surface.blit(self.turn_view.surface, (x, y))

            y = self.turn_view.surface.get_rect().bottom + MainFrame.PANE_PADDING

            self.score_view.draw()
            self.surface.blit(self.score_view.surface, (x, y))

            y = self.turn_view.surface.get_rect().bottom + MainFrame.PANE_PADDING

            if self.game.current_turn is not None and \
                            self.game.current_turn.state == model.Turn.LAST_ROLL_DONE:
                self.score_picker.draw()
                self.surface.blit(self.score_picker.surface, (x, y))

            y = pane_rect.bottom - 20
            draw_text(self.surface, "1-6:Hold    F1-F6:Unhold    R:Roll    E:End    Q:Quit", x=pane_rect.centerx, y=y, size=30)


        if self.game.state == model.Game.GAME_READY:

            filename = MainFrame.RESOURCES_DIR + "logo.jpg"
            image = pygame.image.load(filename)
            image = pygame.transform.scale(image, (self.surface.get_rect().width, 190))
            self.surface.blit(image,(0,0))

            y = self.turn_view.surface.get_rect().bottom + MainFrame.PANE_PADDING

            self.hst.draw()
            self.surface.blit(self.hst.surface, (x, y))

            y = pane_rect.bottom - 20
            draw_text(self.surface, "  Press 'Space Bar' to play or 'Q' to quit.  ", x=pane_rect.centerx, y=y, size=30)


        if self.game.state == model.Game.GAME_OVER:

            self.game_over.draw()
            self.surface.blit(self.game_over.surface, (0, 0))

            y = self.game_over.surface.get_rect().bottom + MainFrame.PANE_PADDING

            self.hst.draw()
            self.surface.blit(self.hst.surface, (x, y))

            y = pane_rect.bottom - 20
            draw_text(self.surface, "  Press 'Space Bar' to play or 'Q' to quit.  ", x=pane_rect.centerx, y=y, size=30)

    def update(self):
        pygame.display.update()


class ScoreView:
    TITLE_HEIGHT = 30
    HEADER_HEIGHT = 20
    HEADER_WIDTH = 100
    SCORE_HEIGHT = 18
    SCORE_WIDTH = 170
    PADDING = 3
    SCORE_TEXT_SIZE = 22
    HEADER_TEXT_SIZE = 32
    NO_SCORE = "---"

    def __init__(self, width: int = 500, height: int = None):

        self.game = None

        if height is None:
            height = ScoreView.TITLE_HEIGHT + \
                     ScoreView.PADDING + \
                     ScoreView.HEADER_HEIGHT + \
                     ScoreView.PADDING + \
                     (ScoreView.SCORE_HEIGHT + ScoreView.PADDING) * 16 + ScoreView.PADDING * 2

        self.surface = pygame.Surface((width, height))

    def initialise(self, game: model.Game):
        self.game = game

    def tick(self):
        pass

    def draw(self):

        if self.game is None:
            raise ("No game to view scores!")

        pane_rect = self.surface.get_rect()

        if self.game is None:
            raise Exception("No game to view!!!")

        self.surface.fill(colours.Colours.BLUE)
        rect = pygame.Rect(0, 0, pane_rect.width, ScoreView.TITLE_HEIGHT)
        pygame.draw.rect(self.surface, colours.Colours.GREY, rect)

        if self.game.state == model.Game.GAME_PLAYING:
            draw_text(self.surface, "  Scores  ({0})  ".format(model.Game.STATE[self.game.state]),
                      pane_rect.centerx,
                      ScoreView.TITLE_HEIGHT / 2,
                      size=ScoreView.HEADER_TEXT_SIZE,
                      bg_colour=colours.Colours.GREY)

        # Game to update current leaders so that we can highlight them
        self.game.calc_leaders()

        # Draw The players names at the top of the score view
        x = ScoreView.PADDING * 2 + ScoreView.SCORE_WIDTH + ScoreView.HEADER_WIDTH / 2
        y = ScoreView.TITLE_HEIGHT + ScoreView.PADDING + ScoreView.HEADER_HEIGHT / 2

        for player in self.game.players:
            if player == self.game.current_player:
                bg_colour = colours.Colours.GREEN
            elif player in self.game.winners:
                bg_colour = colours.Colours.RED
            else:
                bg_colour = colours.Colours.BLUE

            draw_text(self.surface, "  {0}  ".format(player.name), bg_colour=bg_colour, x=x, y=y)
            x += ScoreView.HEADER_WIDTH + ScoreView.PADDING

        y += ScoreView.HEADER_HEIGHT + ScoreView.PADDING * 2

        # Print upper section scores
        for i in range(1, 7):

            x = ScoreView.PADDING + ScoreView.SCORE_WIDTH / 2

            score_type = "{0}'s".format(i)
            draw_text(self.surface, x=x, y=y, msg="{0}'s".format(i),
                      fg_colour=colours.Colours.WHITE,
                      bg_colour=colours.Colours.BLUE,
                      size=ScoreView.SCORE_TEXT_SIZE)

            x = ScoreView.PADDING * 2 + ScoreView.SCORE_WIDTH + ScoreView.HEADER_WIDTH / 2

            for player in self.game.players:

                if player.name in self.game.player_scores.keys():
                    player_scores = self.game.player_scores[player.name]
                    if score_type in player_scores.keys():
                        score = player_scores[score_type]
                        bg_colour = colours.Colours.BLUE
                        fg_colour = colours.Colours.WHITE
                    else:
                        score = ScoreView.NO_SCORE
                        bg_colour = colours.Colours.BLUE
                        fg_colour = colours.Colours.BLACK

                    draw_text(self.surface, msg="{0}".format(score), x=x, y=y,
                              bg_colour=bg_colour,
                              fg_colour=fg_colour,
                              size=ScoreView.SCORE_TEXT_SIZE)
                else:
                    draw_text(self.surface, msg=ScoreView.NO_SCORE, x=x, y=y,
                              bg_colour=colours.Colours.BLUE,
                              fg_colour=colours.Colours.BLACK,
                              size=ScoreView.SCORE_TEXT_SIZE)

                x += ScoreView.HEADER_WIDTH + ScoreView.PADDING

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

            x = ScoreView.PADDING + ScoreView.SCORE_WIDTH / 2

            draw_text(self.surface, msg="{0}".format(score_type), x=x, y=y,
                      bg_colour=colours.Colours.BLUE,
                      fg_colour=colours.Colours.WHITE,
                      size=ScoreView.SCORE_TEXT_SIZE)

            x = ScoreView.PADDING * 2 + ScoreView.SCORE_WIDTH + ScoreView.HEADER_WIDTH / 2

            for player in self.game.players:

                if player.name in self.game.player_scores.keys():
                    player_scores = self.game.player_scores[player.name]
                    if score_type in player_scores.keys():
                        score = player_scores[score_type]
                        bg_colour = colours.Colours.BLUE
                        fg_colour = colours.Colours.WHITE
                    else:
                        score = ScoreView.NO_SCORE
                        bg_colour = colours.Colours.BLUE
                        fg_colour = colours.Colours.BLACK

                    draw_text(self.surface, msg="{0}".format(score), x=x, y=y,
                              bg_colour=bg_colour,
                              fg_colour=fg_colour,
                              size=ScoreView.SCORE_TEXT_SIZE)

                else:
                    draw_text(self.surface, msg=ScoreView.NO_SCORE, x=x, y=y,
                              bg_colour=colours.Colours.BLUE,
                              fg_colour=colours.Colours.BLACK,
                              size=ScoreView.SCORE_TEXT_SIZE)

                x += ScoreView.HEADER_WIDTH + ScoreView.PADDING

            y += ScoreView.SCORE_HEIGHT + ScoreView.PADDING

        # Print score table footer
        x = ScoreView.PADDING + ScoreView.SCORE_WIDTH / 2
        y += ScoreView.PADDING

        draw_text(self.surface, msg="TOTAL", x=x, y=y,
                  bg_colour=colours.Colours.BLUE,
                  fg_colour=colours.Colours.WHITE,
                  size=ScoreView.SCORE_TEXT_SIZE)

        x = ScoreView.PADDING * 2 + ScoreView.SCORE_WIDTH + ScoreView.HEADER_WIDTH / 2

        for player in self.game.players:

            if player == self.game.current_player:
                bg_colour = colours.Colours.GREEN
                fg_colour = colours.Colours.WHITE
            elif player in self.game.winners:
                bg_colour = colours.Colours.RED
                fg_colour = colours.Colours.WHITE
            else:
                bg_colour = colours.Colours.BLUE
                fg_colour = colours.Colours.WHITE

            if player.name in self.game.player_scores.keys():

                player_scores = self.game.player_scores[player.name]
                score = sum(player_scores.values())
                draw_text(self.surface, msg="  {0}  ".format(score), x=x, y=y,
                          fg_colour=fg_colour,
                          bg_colour=bg_colour,
                          size=ScoreView.SCORE_TEXT_SIZE)
            else:
                draw_text(self.surface, msg=ScoreView.NO_SCORE, x=x, y=y,
                          fg_colour=fg_colour,
                          bg_colour=bg_colour,
                          size=ScoreView.SCORE_TEXT_SIZE)

            x += ScoreView.PADDING + ScoreView.HEADER_WIDTH


class TurnView:
    DICE_WIDTH = 60
    DICE_HEIGHT = 60
    DICE_SPACING = 10
    HEADER_HEIGHT = 30
    HEADER_BG_COLOUR = colours.Colours.GREY
    HEADER_FG_COLOUR = colours.Colours.WHITE
    HEADER_FONT_SIZE = 30

    def __init__(self, width: int = 500, height: int = None):

        if height is None:
            height = TurnView.HEADER_HEIGHT + TurnView.DICE_SPACING * 3 + TurnView.DICE_HEIGHT * 2

        self.surface = pygame.Surface((width, height))
        self.current_rotation = 0

    def initialise(self, game: model.Game):

        self.game = game

    def tick(self):
        #self.current_rotation += 5
        pass

    def draw(self):

        if self.game is None:
            raise Exception("No game to view!!!")

        pane_rect = self.surface.get_rect()

        self.surface.fill(colours.Colours.RED)

        rect = pygame.Rect(0, 0, pane_rect.width, TurnView.HEADER_HEIGHT)
        pygame.draw.rect(self.surface, TurnView.HEADER_BG_COLOUR, rect)


        if self.game.state == model.Game.GAME_PLAYING:

            self.held_dice = pygame.sprite.Group()
            self.rolled_dice = pygame.sprite.Group()

            draw_text(self.surface, "  Player {0}: {1}, roll {2}  ".format(self.game.current_player.name,
                                                                           model.Turn.state_to_text[
                                                                               self.game.current_turn.state],
                                                                           self.game.current_turn.rolls),
                      x=self.surface.get_rect().centerx,
                      y=TurnView.HEADER_HEIGHT / 2,
                      bg_colour=TurnView.HEADER_BG_COLOUR,
                      fg_colour=TurnView.HEADER_FG_COLOUR,
                      size=TurnView.HEADER_FONT_SIZE)

            x = TurnView.DICE_SPACING
            y = TurnView.HEADER_HEIGHT + TurnView.DICE_SPACING

            for dice in self.game.current_turn.current_roll:
                dice_view = SpriteView(x=x, y=y, image_file_name="dice" + str(dice) + ".png", width=TurnView.DICE_WIDTH,
                                       height=TurnView.DICE_HEIGHT)

                self.rolled_dice.add(dice_view)
                x = dice_view.rect.right + TurnView.DICE_SPACING

            x = TurnView.DICE_SPACING
            y = TurnView.HEADER_HEIGHT + TurnView.DICE_HEIGHT + TurnView.DICE_SPACING * 2

            for dice in self.game.current_turn.slots:
                dice_view = SpriteView(x=x, y=y, image_file_name="dice" + str(dice) + ".png",
                                       width=TurnView.DICE_WIDTH, height=TurnView.DICE_HEIGHT)
                dice_view.rotate(self.current_rotation)
                self.held_dice.add(dice_view)
                x = dice_view.rect.right + TurnView.DICE_SPACING

            self.rolled_dice.draw(self.surface)
            self.held_dice.draw(self.surface)


class SpriteView(pygame.sprite.Sprite):
    def __init__(self, x: int = 0, y: int = 0, width: int = None, height: int = None, image_file_name: str = None):

        super(SpriteView, self).__init__()

        self._x = x
        self._y = y

        self.image_file_name = image_file_name

        if self.image_file_name is not None:
            filename = MainFrame.RESOURCES_DIR + self.image_file_name
            image = pygame.image.load(filename)

            if width is None:
                if height is None:
                    width = image.get_rect().width
                else:
                    width = int(image.get_rect().width * height / image.get_rect().height)
            if height is None:
                if width is None:
                    height = image.get_rect().height
                else:
                    height = int(image.get_rect().height * width / image.get_rect().width)

            self.image = pygame.transform.smoothscale(image, (width, height))
            self.original_image = self.image.copy()

        self.rect = self.image.get_rect()
        self.rect.x = int(self._x)
        self.rect.y = int(self._y)

    def rotate(self, rotation : int):
        loc = self.original_image.get_rect().center
        self.image = pygame.transform.rotate(self.original_image, rotation)
        self.image.get_rect().center = loc


class ScorePickerView:
    TITLE_HEIGHT = 40
    TITLE_TEXT_SIZE = 30
    CHOICE_HEIGHT = 20
    CHOICE_TEXT_SIZE = 24

    def __init__(self, width: int = 500, height: int = None):

        self.game = None

        if height is None:
            height = 200

        self.surface = pygame.Surface((width, height))

    def initialise(self, game: model.Game):

        self.game = game

    def draw(self):

        if self.game is None:
            raise ("No game set for Score Picker View!")

        self.surface.fill(colours.Colours.BLACK)

        pane_rect = self.surface.get_rect()

        y = ScorePickerView.TITLE_HEIGHT / 2
        x = pane_rect.centerx

        draw_text(self.surface, msg="Pick a score for this turn:-", x=x, y=y,
                  size=ScorePickerView.TITLE_TEXT_SIZE)

        y = ScorePickerView.TITLE_HEIGHT + 10

        available_scores = sorted(self.game.available_scores())
        choice_number = 1
        for score in available_scores:
            draw_text(self.surface, msg="{0}. {1}".format(choice_number, score), x=x, y=y,
                      size=ScorePickerView.CHOICE_TEXT_SIZE)
            choice_number += 1
            y += ScorePickerView.CHOICE_HEIGHT


class HighScoreTableView:

    TITLE_HEGHT = 24
    TITLE_TEXT_SIZE = 20
    SCORE_HEIGHT = 20
    SCORE_TEXT_SIZE = 20

    def __init__(self, width: int, height: int = 500):
        self.hst = None
        self.dice_group = None

        self.surface = pygame.Surface((width, height))

    def initialise(self, hst: utils.HighScoreTable):
        self.hst = hst

        self.random_dice_generate()

    def random_dice_generate(self):

        dice_count = int(self.surface.get_rect().width/(TurnView.DICE_WIDTH + TurnView.DICE_SPACING))

        self.dice_group = pygame.sprite.Group()

        for i in range(dice_count + 1):
            dice = SpriteView(x = (i*TurnView.DICE_WIDTH + TurnView.DICE_SPACING),
                              y = (self.surface.get_rect().bottom - TurnView.DICE_HEIGHT),
                              width=TurnView.DICE_WIDTH,
                              height=TurnView.DICE_HEIGHT,
                              image_file_name="dice{0}.png".format(random.randint(1,6)))

            self.dice_group.add(dice)

    def tick(self):
        self.random_dice_generate()

    def draw(self):

        if self.hst is None:
            raise ("No High Score Table to view!")

        self.surface.fill(colours.Colours.BLACK)

        self.dice_group.draw(self.surface)

        pane_rect = self.surface.get_rect()

        y = ScorePickerView.TITLE_HEIGHT / 2
        x = pane_rect.centerx

        draw_text(self.surface, msg="High Score Table", x=x, y=y,
                  size=ScorePickerView.TITLE_TEXT_SIZE,
                  fg_colour=colours.Colours.GOLD)

        rank = 1
        for entry in self.hst.table:
            y += HighScoreTableView.SCORE_HEIGHT

            name, score = entry
            draw_text(self.surface, msg="{0}. {1} - {2}".format(rank, name, score), x=x, y=y,
                      size=HighScoreTableView.SCORE_TEXT_SIZE)
            rank += 1


class GameOverView:
    def __init__(self, width: int, height: int = 500):

        self.game = None
        self.dice_group = None

        self.surface = pygame.Surface((width, height))

    def inititalise(self, game : model.Game):
        self.game = game
        self.random_dice_generate()

    def tick(self):
        self.random_dice_generate()

    def random_dice_generate(self):

        dice_count = int(self.surface.get_rect().width/(TurnView.DICE_WIDTH + TurnView.DICE_SPACING))

        self.dice_group = pygame.sprite.Group()

        pane_rect = self.surface.get_rect()

        dice = SpriteView(x = int(pane_rect.width/4- TurnView.DICE_WIDTH/2),
                          y = 100,
                          width=TurnView.DICE_WIDTH,
                          height=TurnView.DICE_HEIGHT,
                          image_file_name="dice{0}.png".format(random.randint(1,6)))

        self.dice_group.add(dice)

        dice = SpriteView(x = int(pane_rect.width*3/4 - TurnView.DICE_WIDTH/2),
                          y = 100,
                          width=TurnView.DICE_WIDTH,
                          height=TurnView.DICE_HEIGHT,
                          image_file_name="dice{0}.png".format(random.randint(1,6)))

        self.dice_group.add(dice)


    def draw(self):
        if self.game is None:
            raise ("No game to view!")

        pane_rect = self.surface.get_rect()

        self.surface.fill(colours.Colours.BLACK)

        self.dice_group.draw(self.surface)

        y=30

        draw_text(self.surface, "  G A M E    O V E R  ", x=pane_rect.centerx, y=y, size=50,fg_colour=colours.Colours.RED)

        y += 35
        draw_text(self.surface, "  Winners:  ", x=pane_rect.centerx, y=y, size=30, fg_colour=colours.Colours.GOLD)
        for player in self.game.winners:
            y += 30
            draw_text(self.surface, "{0} with a score of {1}".format(player.name, self.game.winning_score),
                      x=pane_rect.centerx, y=y, size=30, fg_colour=colours.Colours.GOLD)

        y += 35
        draw_text(self.surface, "  Final Scores:  ", x=pane_rect.centerx, y=y, size=30)
        for player in self.game.player_scores.keys():
            if player not in self.game.winners:
                y += 20
                draw_text(self.surface,
                          "{0} with a score of {1}".format(player, sum(self.game.player_scores[player].values())),
                          x=pane_rect.centerx, y=y, size=20)

def draw_text(surface, msg, x, y, size=32, fg_colour=colours.Colours.WHITE, bg_colour=colours.Colours.BLACK):
    font = pygame.font.Font(None, size)
    text = font.render(msg, 1, fg_colour, bg_colour)
    textpos = text.get_rect()
    textpos.centerx = x
    textpos.centery = y
    surface.blit(text, textpos)
