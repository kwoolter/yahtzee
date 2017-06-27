import yahtzee.model as model
import yahtzee.view.game_text_view as view
import yahtzee.utils as utils
import logging, cmd

class GameCLI(cmd.Cmd):

    intro = "Welcome to the PyYahtzee.\nType 'start' to get going!"
    prompt = "What next?"

    def __init__(self, game : model.Game = None):
        super(GameCLI, self).__init__()
        if game is None:
            self.game = model.Game()
        else:
            self.game = game

        self.view = view.ScoreCardView(self.game)
        self.turn_view = view.TurnView(self.game)

    def do_start(self, args):
        """Start the game"""
        try:
            if len(self.game.players) == 0:
                self.enter_players()
            self.game.start()
            self.game.hst.print()
            self.game.print()
        except Exception as err:
            print(str(err))

    def do_print(self, args):
        """Print the current game state"""
        self.game.print()
        self.view.print()
        self.turn_view.print()

    def do_scores(self, args):
        """Print the current scores"""
        try:
            self.view.print()
        except Exception as err:
            print(str(err))

    def do_roll(self, args):
        """The current player rolls the dice"""
        try:
            self.game.roll()
            self.turn_view.print()
            if self.game.current_turn.state == model.Turn.LAST_ROLL_DONE:
                utils.type("\nLast roll complete\n")
                self.game.end_turn()
            if self.game.state == model.Game.GAME_OVER:
                self.game_over()

        except Exception as err:
            print(str(err))

    def do_hold(self, args):
        """hold number1 [number2 number3] - The current player holds the specified rolled number(s) e.g. 'hold 1 6'.  You can also use 'hold all'."""
        try:
            if args=="all":
                self.game.hold_all()
            else:
                if len(args) >= 1:
                    for arg in args.split():
                        try:
                            self.game.hold(arg)
                        except Exception as err:
                            print(str(err))
                else:
                    choice = utils.pick("Dice", self.game.current_turn.current_roll, auto_pick=True)
                    self.game.hold(choice)

            self.turn_view.print()

        except Exception as err:
            print(str(err))

    def do_unhold(self, args):
        """unhold number1 [number2 number3] - The current player unholds the specified held number(s) e.g. 'unhold 3 6'."""
        try:
            if len(args) >= 1:
                for arg in args.split():
                    try:
                        self.game.unhold(arg)
                    except Exception as err:
                        print(str(err))

            else:
                choice = utils.pick("Dice", self.game.current_turn.slots, auto_pick=True)
                self.game.unhold(choice)

            self.turn_view.print()

        except Exception as err:
            print(str(err))

    def do_end(self, args):
        """The current player ends their turn"""
        try:
            self.game.end_turn()
            if self.game.state == model.Game.GAME_OVER:
                self.game_over()
        except Exception as err:
            print(str(err))

    def do_quit(self, args):
        """Quit the game"""
        if utils.confirm("Are you sure you want to quit?"):
            exit(0)

    def enter_players(self):
        player_count = 0
        while player_count == 0:
            choice = input("How many players (1-4)?")
            choice =  utils.is_numeric(choice)
            if choice is None:
                print("You need to enter a number between 1 and 4")
            elif choice < 1 or choice > 4:
                print("Only 1-4 players allowed")
            else:
                player_count = choice

        for i in range(player_count):
            name = input("Player {0} name?".format(i+1))
            self.game.add_player(model.Player(name))


    def game_over(self):

        utils.type("\nG A M E  O V E R\n\n...and the winners are....\n\n")
        self.game.end()
        for player in self.game.winners:
            print("{0} with a score of {1}.".format(player.name, self.game.winning_score))
        utils.type("\nC O N G R A T U L A T I O N S\n\n\n")
        self.view.print()
        self.game.hst.print()

        if utils.confirm("Do you want to play again?"):
            self.game.start()
            self.game.hst.print()
            self.game.print()
        else:
            exit(0)

def controller_main():

    logging.basicConfig(level=logging.WARNING)

    game = model.Game()
    #game.add_player(model.Player("Rosie"))
    game.add_player(model.Player("Keith"))
    game.add_player(model.Player("Jack"))

    cli = GameCLI()
    cli.cmdloop()


if __name__ == "__main__":
    controller_main()
