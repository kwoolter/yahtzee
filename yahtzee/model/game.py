import copy
import logging
import random

import yahtzee.utils as utils

class Player:
    '''A class to represent the basic details of a Player.'''
    def __init__(self, name :str):
        self.name = name

class Game:
    '''A class to represent the whole game of Yahtzee.'''

    GAME_OVER = 0
    GAME_READY = 1
    GAME_PLAYING = 2
    MAX_ROUNDS = 13
    #MAX_ROUNDS = 5
    STATE = {GAME_OVER: "Game Over", GAME_READY : "Game Ready", GAME_PLAYING : "Game Playing"}

    def __init__(self):
        self.winning_score = 0
        self.winners = []
        self.players = []
        self.player_scores = {}
        self.current_round = 0
        self.current_player_id = 0
        self.current_turn = None
        self._state = Game.GAME_READY

        self.hst = utils.HighScoreTable("PyYahtzee")
        self.hst.load()

    @property
    def current_player(self):
        if self.players is None or len(self.players) == 0:
            return None
        else:
            return self.players[self.current_player_id]

    @property
    def state(self):
        if self.current_round == 0:
            return Game.GAME_READY
        elif self.current_round > Game.MAX_ROUNDS:
            return Game.GAME_OVER
        elif self.current_round == Game.MAX_ROUNDS \
                and self.current_player_id == len(self.players)-1 \
                and self.current_turn.state == Turn.TURN_OVER:
            return Game.GAME_OVER
        else:
            return Game.GAME_PLAYING

    def roll(self):
        if self.state != Game.GAME_PLAYING:
            raise Exception("Game not in a state to do a roll!")

        if self.current_turn.state == Turn.TURN_OVER:
            self.next_player()

        if self.current_turn.state in (Turn.READY, Turn.PLAYING):
            self.current_turn.roll()

    def hold(self, dice_number : int):
        if self.state != Game.GAME_PLAYING:
            raise Exception("Game not in a state to do a hold!")

        self.current_turn.hold(dice_number)

    def hold_all(self):
        if self.state != Game.GAME_PLAYING:
            raise Exception("Game not in a state to do a hold!")

        self.current_turn.hold_all()

    def stop_rolling(self):
        if self.state != Game.GAME_PLAYING:
            raise Exception("Game not in a state to score a turn!")

        if self.current_turn.state != Turn.PLAYING:
            raise Exception("Can't stop rolling as Turn not being played!")

        self.current_turn.stop_rolling()

    def score_turn(self, chosen_score : str):

        if self.state != Game.GAME_PLAYING:
            raise Exception("Game not in a state to score a turn!")

        if self.current_turn.state == Turn.READY:
            raise Exception("Turn not started yet to score a turn!")

        # Get the list of possible scores from the current turn
        available_scores = self.available_scores()

        if chosen_score not in available_scores:
            raise Exception("Score type {0} is not available to select!".format(chosen_score))

        # Get the current player scores
        player_scores = self.player_scores[self.current_player.name]

        # Get the list of possible scores from the current turn
        scores = self.current_turn.score()

        # Store the selected score type in the current player's list of scores
        player_scores[chosen_score] = scores[chosen_score]
        print("Player {0} got a turn score of {1} with {2}.".format(self.current_player.name,
                                                                    scores[chosen_score],
                                                                    chosen_score))

        # See if the player has got an upper total bonus and add to their score types
        upper_total = 0
        for i in range(1,7):
            if "{0}'s".format(i) in player_scores.keys():
                upper_total += player_scores["{0}'s".format(i)]

        # If the total upper score is greater than or equal to the threshold...
        if upper_total >= Scores.UPPER_TOTAL_THRESHOLD:
            #...then award a bonus.
            upper_total_bonus = Scores.scores_to_points[Scores.UPPER_TOTAL_BONUS]
            logging.info("Player {0} got an upper total bonus of {1}".format(self.current_player.name,upper_total_bonus))
            player_scores[Scores.UPPER_TOTAL_BONUS] = upper_total_bonus

        # Now see if the player got an additional Yahtzee bonus..
        # If the player has already had a Yahtzee scored...
        # And the player did not choose Yahtzee..
        # And they had the option to...
        if Scores.YAHTZEE in player_scores.keys() and player_scores[Scores.YAHTZEE] > 0:

            if chosen_score != Scores.YAHTZEE and scores[Scores.YAHTZEE]:
                yahtzee_bonus = Scores.scores_to_points[Scores.YAHTZEE_MULTI_BONUS]
                logging.info("Player {0} got a multi-yahtzee bonus of {1}".format(self.current_player.name,yahtzee_bonus))

                if Scores.YAHTZEE_MULTI_BONUS not in player_scores.keys():
                    player_scores[Scores.YAHTZEE_MULTI_BONUS] = 0
                player_scores[Scores.YAHTZEE_MULTI_BONUS] += yahtzee_bonus

        # The turn is now ended
        self.current_turn.end()
        self.calc_leaders()

    def available_scores(self):

        # Get the list of possible scores from the current turn
        scores = self.current_turn.score()

        # Get the list of score types that the current player has selected already
        if self.current_player.name not in self.player_scores.keys():
            self.player_scores[self.current_player.name] = {}

        player_scores = self.player_scores[self.current_player.name]

        # Build a list of available scores i.e. scores types that the player has not yet selected
        available_scores = []
        for score in scores.keys():
            if  score not in player_scores.keys():
                available_scores.append(score)

        return available_scores

    def end_turn(self):
        '''Game.end_turn() - processing that happens at the end of a players turn.'''

        if self.state != Game.GAME_PLAYING:
            raise Exception("Game not in a state to end turn!")

        # Get the list of possible scores from the current turn
        scores = self.current_turn.score()

        # Get the list of score types that the current player has selected already
        if self.current_player.name not in self.player_scores.keys():
            self.player_scores[self.current_player.name] = {}

        player_scores = self.player_scores[self.current_player.name]

        # Build a list of available scores i.e. scores types that the player has not yet selected
        available_scores = []
        for score in scores.keys():
            if  score not in player_scores.keys():
                available_scores.append(score)

        # Ask the player to pick which score type they want to use this turn for
        # This really belongs in the controller but hey ho!!!!
        chosen_score = utils.pick("Score", sorted(available_scores))

        # Store the selected score type in the current player's list of scores
        player_scores[chosen_score] = scores[chosen_score]
        print("Player {0} got a turn score of {1} with {2}.".format(self.current_player.name,
                                                                    scores[chosen_score],
                                                                    chosen_score))

        # See if the player has got an upper total bonus and add to their score types
        upper_total = 0
        for i in range(1,7):
            if "{0}'s".format(i) in player_scores.keys():
                upper_total += player_scores["{0}'s".format(i)]

        # If the total upper score is greater than or equal to the threshold...
        if upper_total >= Scores.UPPER_TOTAL_THRESHOLD:
            #...then award a bonus.
            upper_total_bonus = Scores.scores_to_points[Scores.UPPER_TOTAL_BONUS]
            logging.info("Player {0} got an upper total bonus of {1}".format(self.current_player.name,upper_total_bonus))
            player_scores[Scores.UPPER_TOTAL_BONUS] = upper_total_bonus

        # Now see if the player got an additional Yahtzee bonus..
        # If the player has already had a Yahtzee scored...
        # And the player did not choose Yahtzee..
        # And they had the option to...
        if Scores.YAHTZEE in player_scores.keys() and player_scores[Scores.YAHTZEE] > 0:

            if chosen_score != Scores.YAHTZEE and scores[Scores.YAHTZEE]:
                yahtzee_bonus = Scores.scores_to_points[Scores.YAHTZEE_MULTI_BONUS]
                logging.info("Player {0} got a multi-yahtzee bonus of {1}".format(self.current_player.name,yahtzee_bonus))

                if Scores.YAHTZEE_MULTI_BONUS not in player_scores.keys():
                    player_scores[Scores.YAHTZEE_MULTI_BONUS] = 0
                player_scores[Scores.YAHTZEE_MULTI_BONUS] += yahtzee_bonus

        # The turn is now ended
        self.current_turn.end()
        self.calc_leaders()

    def unhold(self, dice_number : int):

        if self.state != Game.GAME_PLAYING:
            raise Exception("Game not in a state to do an unhold!")

        self.current_turn.unhold(dice_number)

    def add_player(self, new_player : Player):
        '''Game.add_player - Add a new player to the game.'''

        if self.state != Game.GAME_READY:
            raise Exception("Game not in a state to add players!")

        self.players.append(new_player)

    def start(self):
        '''Game.start() - start the game by initialising the core game variables.'''
        self.player_scores = {}
        self.winning_score = 0
        self.winners = []
        self.current_player_id = 0
        self.current_round = 1
        self.current_turn = Turn(self.current_player)

    def next_player(self):

        self.current_player_id += 1
        if self.current_player_id == len(self.players):
            self.current_player_id = 0
            self.current_round += 1

        self.current_turn = Turn(self.current_player)

        if self.state == Game.GAME_OVER:
            raise Exception("All rounds have been completed.")

    def print(self):
        print("PyYahtzee: state={2}, players={0}, round={1} of {4}, current player={3}".format(len(self.players),
                                                                                             self.current_round,
                                                                                             Game.STATE[self.state],
                                                                                             self.current_player.name,
                                                                                             Game.MAX_ROUNDS))

        if self.state == Game.GAME_PLAYING:
            self.current_turn.print()

    def scores(self):
        if self.state == Game.GAME_READY:
            raise Exception("Game is not currently playing!")

        print("Current Scores")

        for player in self.player_scores.keys():
            print("Player {0} scores: {1} = {2}".format(player, self.player_scores[player], sum(self.player_scores[player].values())))

        hst = utils.HighScoreTable("PyYahtzee current scores",max_size=len(self.players))
        for player in self.player_scores.keys():
            hst.add(player, sum(self.player_scores[player].values()))

        hst.print()

    def end(self):
        '''Game.end() - end the game.'''

        if self.state != Game.GAME_OVER:
            raise Exception("Game is not over yet")

        # Calculate which players are the winners.
        self.calc_leaders()

        # See which player's made it into the High Score Table
        for player in self.players:
            if player.name in self.player_scores.keys():
                player_scores = self.player_scores[player.name]
                total_score = sum(player_scores.values())
                if self.hst.is_high_score(total_score):
                    logging.info("Player {0} got a new high score of {1}!".format(player.name, total_score))
                    self.hst.add(player.name, total_score)

        self.hst.save()

    def calc_leaders(self):
        '''Game.calc_leaders() - Calculate who the current leaders are.'''
        self.winning_score = 0
        self.winners = []

        for player in self.players:
            if player.name in self.player_scores.keys():
                player_scores = self.player_scores[player.name]
                total_score = sum(player_scores.values())
                if total_score > self.winning_score:
                    self.winning_score = total_score

        for player in self.players:
            if player.name in self.player_scores.keys():
                player_scores = self.player_scores[player.name]
                total_score = sum(player_scores.values())
                if total_score == self.winning_score:
                    self.winners.append(player)


class Scores:
    '''A class to capture the types of score and the score you get for rolling them.'''

    THREE_OF_A_KIND = "3 of a kind"
    FOUR_OF_A_KIND = "4 of a kind"
    YAHTZEE = "Yahtzee"
    YAHTZEE_MULTI_BONUS = "Yahtzee multi-bonus"
    FULL_HOUSE = "Full House"
    LARGE_RUN = "Large Straight"
    SMALL_RUN = "Small Straight"
    CHANCE = "Chance"
    UPPER_TOTAL_THRESHOLD = 63
    UPPER_TOTAL_BONUS = "Upper total bonus"


    scores_to_points = {YAHTZEE:50,
                        YAHTZEE_MULTI_BONUS: 100,
                        FULL_HOUSE:25,
                        LARGE_RUN:40,
                        SMALL_RUN:30,
                        UPPER_TOTAL_BONUS: 35,
                        THREE_OF_A_KIND: 0,
                        FOUR_OF_A_KIND: 0}

    @staticmethod
    def blank_score_sheet():
        new_score_sheet = {}

        # Populate with upper score card score types
        for i in range(1,7):
            new_score_sheet["{0}'s".format(i)] = 0

        # Populate with lower score card types except the bonuses
        for lower_score_type in Scores.scores_to_points.keys():
            new_score_sheet[lower_score_type] = 0
        del new_score_sheet[Scores.UPPER_TOTAL_BONUS]
        del new_score_sheet[Scores.YAHTZEE_MULTI_BONUS]

        return new_score_sheet

class Turn:
    '''A class to represent a player's turn in the game of Yahtzee.'''

    TURN_OVER = 0
    READY = 1
    PLAYING = 2
    LAST_ROLL_DONE = 3

    state_to_text = {READY:"Ready", PLAYING:"Playing", LAST_ROLL_DONE:"Last roll done", TURN_OVER:"Turn over"}

    MAX_ROLLS = 3
    DICE = 5

    def __init__(self, player : Player):
        self.player = player
        self.rolls = 0
        self.slots = []
        self.current_roll = []
        self.complete = False

    @property
    def state(self):
        '''Turn.state() - return the current state of the turn.'''

        if self.complete is True:
            return Turn.TURN_OVER
        elif self.rolls == 0:
            return Turn.READY
        elif self.rolls > 0 and self.rolls < Turn.MAX_ROLLS:
            return Turn.PLAYING
        elif self.rolls == Turn.MAX_ROLLS:
            return Turn.LAST_ROLL_DONE

    def roll(self):
        '''Turn.roll() - roll all non-held dice.'''

        if self.state not in (Turn.READY, Turn.PLAYING):
            raise Exception("You don't have any more rolls")

        if len(self.slots) == Turn.DICE:
            raise Exception("You don't have any more dice to rolls")

        self.rolls += 1

        self.current_roll = []
        for i in range(0, Turn.DICE - len(self.slots)):
            self.current_roll.append(random.randint(1,6))
            #self.current_roll.append(6)

        logging.info("Player %s rolled %s." % (self.player.name, str(self.current_roll)))

    def hold(self, dice_number : int):
        '''Turn.hold(int) - Hold a dice from the current roll that matches the specified number.'''

        if self.state != Turn.PLAYING:
            raise Exception("You don't have any more rolls")

        dice_choice = utils.is_numeric(dice_number)

        if dice_choice is None or dice_choice < 1 or dice_choice > 6:
            raise Exception("{0} is not a valid dice number.  Must be between 1 and 6.".format(dice_number))

        if dice_choice in self.current_roll:
            self.slots.append(dice_choice)
            self.current_roll.remove(dice_choice)
            logging.info("Player %s held dice number %i in a free slot." % (self.player.name, dice_choice))
        else:
            raise Exception("Dice value {0} not in current roll {1}".format(dice_choice, self.current_roll))

    def hold_all(self):
        ''' Turn.hold_all() - hold all dice'''
        if self.state != Turn.PLAYING:
            raise Exception("You don't have any more rolls")

        for dice_number in copy.deepcopy(self.current_roll):
            self.hold(dice_number)

    def unhold(self, dice_number : int):
        '''Turn.unhold(int) - unhold a held dice that matches the specified number.'''

        if self.state != Turn.PLAYING:
            raise Exception("You don't have any more rolls")

        dice_choice = utils.is_numeric(dice_number)

        if dice_choice is None or dice_choice < 1 or dice_choice > 6:
            raise Exception("{0} is not a valid dice number.  Must be between 1 and 6.".format(dice_number))

        if dice_choice in self.slots:
            self.slots.remove(dice_choice)
            self.current_roll.append(dice_choice)
            logging.info("Player %s removed dice number %i from a slot." % (self.player.name, dice_choice))
        else:
            raise Exception("Dice value {0} not held in slots {1}".format(dice_choice, self.slots))

    def end(self):
        '''Turn.end() - set the state of the turn to finished.'''
        logging.info("Player %s has ended their turn" % self.player.name)
        self.complete = True

    def stop_rolling(self):
        self.rolls = Turn.MAX_ROLLS

    def score(self):
        '''Turn.score() - Calculate all of the possible scores that can be achieved from the current rice roll.
        Returns a dict that contains a map from score type to the score achieved e.g. Yahtzee : 50.'''

        # Create a list of all possible types of score
        scores = Scores.blank_score_sheet()

        # Find the possible scores of all dice
        all_dice = self.slots + self.current_roll

        # First calculate the basic number scores and build a list of the frequency of each number
        # at the same time for use later on e.g. (1,3,3,6,6) -> (1,0,2,0,0,2)
        number_counts = []
        for i in range(1,7):

            # Store the frequency of the dice number in the rolled dice
            number_counts.append(all_dice.count(i))

            # Store the score of each number i.e. dice number x frequency
            scores["{0}'s".format(i)] = all_dice.count(i) * i

        # Chance is a sum of all dice regardless of any patterns...
        scores[Scores.CHANCE] = sum(all_dice)

        # Now see if we got Yahtzee...
        if 5 in number_counts:
            scores[Scores.YAHTZEE] = Scores.scores_to_points[Scores.YAHTZEE]

        # 4 of a kind..
        if max(number_counts) >= 4:
            scores[Scores.FOUR_OF_A_KIND] = sum(all_dice)

        # 3 of a kind...
        if max(number_counts) >= 3:
            scores[Scores.THREE_OF_A_KIND] = sum(all_dice)

        # or a full house
        if 2 in number_counts and 3 in number_counts:
            scores[Scores.FULL_HOUSE] = Scores.scores_to_points[Scores.FULL_HOUSE]

        # Now look for runs....
        sequential = 0
        max_sequential = sequential

        # Go through the frequency of each number and look for sequences
        for number in number_counts:
            # If we rolled the number then...
            if number >= 1:
                # increase the number of sequential numbers
                sequential +=1
                # If the count of sequential numbers is better than the recorded maximum...
                # Then store the new maximum
                if sequential > max_sequential:
                    max_sequential = sequential
            # If there were no dice for the rolled number then the sequence has ended
            else:
                # Store the maximum if applicable
                if sequential > max_sequential:
                    max_sequential = sequential
                # Reset the sequential count to 0
                sequential = 0

        # If we found 5 numbers in a row large run...
        if max_sequential == 5:
            scores[Scores.LARGE_RUN] = Scores.scores_to_points[Scores.LARGE_RUN]

        # If we found 4 numbers or more in a row, a small run...
        if max_sequential >= 4:
            scores[Scores.SMALL_RUN] = Scores.scores_to_points[Scores.SMALL_RUN]

        return scores

    def print(self):
        print("Player {0} turn (state={5}): rolled {1} of {3}, slots={2}, roll={4}".format(self.player.name,
                                                                    self.rolls,
                                                                    self.slots,
                                                                    Turn.MAX_ROLLS,
                                                                    self.current_roll,
                                                                    Turn.state_to_text[self.state]
                                                                    ))
        self.score()

