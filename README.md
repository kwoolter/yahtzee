# Welcome to PyYahtzee
PyYahtzee By kwoolter :monkey: :copyright: 2017

## Requirements
- Python 3.2 - https://www.python.org/downloads/release/python-326/
- PyGame for Python 3.2 - http://pygame.org/ftp/pygame-1.9.2a0.win32-py3.2.msi

## What's New
- Added pygame GUI as an alternative to CLI
- Run `gui_controller.py` to launch GUI version

## Getting Started
- Written in Python 3.
- Run `run.py` to start the game.
- Type "help" to find out about the commands to play the game e.g. "help", "help scores", etc.
- 1 to 4 players can play the game.
- The rules of Yahtzee can be found [here](http://www.yahtzee.org.uk/rules.html)
- Colours work if the game is run inside PyCharm IDE.
- A high score table is saved as "PyYahtzee.hst".

## Structure
### Text Version
The game is structured using the **Model-View-Controller** paradigm:-

- **Model** - the `game.py` file is the "model" module holds the core of the game e.g. Player,
 Game, Turn.
- **View** - the `game_text_view.py` file is the "view" module holds the classes that display
 various aspects of the game e.g.the scorecard, the dice
- **Controller** - the `controller.py` file has the CLI to play the game using the
[cmd module](https://docs.python.org/3/library/cmd.html)
- The `utils` module has various utilities that are used by the game e.g. `HighScoreTable, is_numeric(), pick(), confirm()`

### Graphics Version
The game is structured using the <strong>Model-View-Controller</strong> paradigm:-

- **Model** - the same `game.py` as the text version
- **View** - the `graphics.py` file is the "view" module holds the classes that display
 various aspects of the game e.g.the scorecard, the turn, etc.
- **Controller** - the `gui_controller.py` file has the GUI controller main loop.

### Screen Shots

<table>
<tr>
<td>
<img height=400 width=400 src="https://github.com/kwoolter/yahtzee/blob/master/yahtzee/view/screenshots/yahtzee1.PNG" alt="game1">
</td>
<td>
<img height=400 width=400 src="https://github.com/kwoolter/yahtzee/blob/master/yahtzee/view/screenshots/yahtzee2.PNG" alt="game2">
</td>
</tr>
</table>



