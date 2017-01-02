import yahtzee.model.game as game

class TextColours:
    COLOUR_LOGO = "\x1B[36;44m"
    COLOUR_SEA = "\x1B[36;44m"
    COLOUR_TEXT = "\x1B[30;48m"
    COLOUR_COORDS = "\x1B[30;47m"
    COLOUR_DICE_ROLLED = "\x1B[1;31;43m"
    COLOUR_DICE_HELD = "\x1B[1;33;41m"
    COLOUR_NAMES = "\x1B[1;37;44m"
    COLOUR_LEADER_NAMES = "\x1B[1;37;41m"
    COLOUR_NORMAL = "\x1B[0m"
    COLOUR_SCORE_TYPES = "\x1B[1;30;43m"
    COLOUR_SCORES = "\x1B[1;34;47m"
    COLOUR_UPPER_SCORE_TYPES = "\x1B[1;30;47m"
    COLOUR_TOTALS = "\x1B[1;37;40m"



class ScoreCardView:
    def __init__(self, game : game.Game):
        self.game = game

    def print(self):
        if self.game is None:
            raise Exception("No game to view!!!")

        # Fore game to update current leaders
        self.game.calc_leaders()

        #Print score table header
        #print("="*(22+len(self.game.players)*11))
        print(TextColours.COLOUR_NAMES +"{0:^21}".format("SCORES")+TextColours.COLOUR_NORMAL, end=" ")
        for player in self.game.players:
            if player in self.game.winners:
                colour = TextColours.COLOUR_LEADER_NAMES
            else:
                colour = TextColours.COLOUR_NAMES
            print(colour+"{0:^10}".format(player.name[0:10])+TextColours.COLOUR_NORMAL, end=" ")

        print()
        #print("="*(22+len(self.game.players)*11))

        # Print upper section scores
        for i in range(1,7):
            score_type = "{0}'s".format(i)
            print(TextColours.COLOUR_UPPER_SCORE_TYPES+"{0:^21}".format(score_type)+TextColours.COLOUR_NORMAL,end=" ")
            for player in self.game.players:
                if player.name in self.game.player_scores.keys():
                    player_scores = self.game.player_scores[player.name]
                    if score_type in player_scores.keys():
                        score = player_scores[score_type]
                        colour = TextColours.COLOUR_SCORES
                    else:
                        score = "-"
                        colour = TextColours.COLOUR_NORMAL
                    print(colour + "{0:^10}".format(score) + TextColours.COLOUR_NORMAL,end=" ")
                else:
                    print("{0:^10}".format("-"),end=" ")
            print()

        # Print lower section scores
        lower_score_types = (game.Scores.UPPER_TOTAL_BONUS,
                             game.Scores.THREE_OF_A_KIND,
                             game.Scores.FOUR_OF_A_KIND,
                             game.Scores.FULL_HOUSE,
                             game.Scores.SMALL_RUN,
                             game.Scores.LARGE_RUN,
                             game.Scores.YAHTZEE,
                             game.Scores.CHANCE,
                             game.Scores.YAHTZEE_MULTI_BONUS)

        for score_type in lower_score_types:
            print(TextColours.COLOUR_SCORE_TYPES+"{0:^21}".format(score_type)+TextColours.COLOUR_NORMAL,end=" ")
            for player in self.game.players:
                if player.name in self.game.player_scores.keys():
                    player_scores = self.game.player_scores[player.name]
                    if score_type in player_scores.keys():
                        score = player_scores[score_type]
                        colour = TextColours.COLOUR_SCORES
                    else:
                        score = "-"
                        colour = TextColours.COLOUR_NORMAL
                    print(colour + "{0:^10}".format(score) + TextColours.COLOUR_NORMAL,end=" ")
                else:
                    print("{0:^10}".format("-"),end=" ")
            print()

        #Print score table footer
        #print("=" * (21 + len(self.game.players) * 11))
        print(TextColours.COLOUR_TOTALS+"{0:^21}".format("TOTAL")+TextColours.COLOUR_NORMAL+" ", end="")
        for player in self.game.players:
            if player.name in self.game.player_scores.keys():
                player_scores = self.game.player_scores[player.name]
                score = sum(player_scores.values())
                print(TextColours.COLOUR_TOTALS+"{0:^10}".format(score)+TextColours.COLOUR_NORMAL, end=" ")
            else:
                print("{0:^10}".format("-"), end=" ")
        print()
        #print("=" * (22 + len(self.game.players) * 11))


class TurnView:

    def __init__(self, game : game.Game):
        self.game = game

    def print(self):

        turn = self.game.current_turn

        print("Player {0} turn (state={5}): rolled {1} of {3}, slots={2}, roll={4}".format(turn.player.name,
                                                                                           turn.rolls,
                                                                                           turn.slots,
                                                                                           game.Turn.MAX_ROLLS,
                                                                                           turn.current_roll,
                                                                                           game.Turn.state_to_text[turn.state]))

        # Print the dice that are held in the slots
        print("DICE HELD")
        if len(turn.slots) == 0:
            print("No Dice held")
        else:
            slots_grid = ["","",""]
            for number in turn.slots:
                view = DiceView(number)
                row = 0
                for row_grid in view.grid():
                    slots_grid[row] += TextColours.COLOUR_DICE_HELD + row_grid + TextColours.COLOUR_NORMAL + "   "
                    row += 1

            for row in slots_grid:
                print(row)

        # Print the dice that are in the current roll
        print("DICE ROLLED")
        if len(turn.current_roll) == 0:
            print("No Dice rolled")
        else:
            slots_grid = ["","",""]
            for number in turn.current_roll:
                view = DiceView(number)
                row = 0
                for row_grid in view.grid():
                    slots_grid[row] += TextColours.COLOUR_DICE_ROLLED + row_grid + TextColours.COLOUR_NORMAL + "   "
                    row += 1

            for row in slots_grid:
                print(row)



class DiceView:

    dice = [(),("   "," ø ", "   "),("ø  ","   ","  ø"),("ø  "," ø ","  ø"),
            ("ø ø","   ","ø ø"),("ø ø"," ø ","ø ø"),("ø ø","ø ø","ø ø")]

    def __init__(self, number : int):
        self.number = number

    def print(self):
        print("_"*5)
        for row in DiceView.dice[self.number]:
            print("|" + row + "|")
        print("¯"*5)

    def grid(self):

        grid = []

        #grid.append("_"*5)
        for row in DiceView.dice[self.number]:
            grid.append(" "+row+" ")
       # grid.append("¯"*5)

        return grid

def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')