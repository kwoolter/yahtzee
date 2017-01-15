#Welcome to PyYahtzee
By kwoolter :monkey: :copyright: 2017

##Requirements
- Python 3.2 - https://www.python.org/downloads/release/python-326/
- PyGame for Python 3.2 - http://pygame.org/ftp/pygame-1.9.2a0.win32-py3.2.msi

##What's New
- Added pygame GUI as an alternative to CLI
- Run _gui_controller.py_ to launch GUI version


<h2>Getting Started</h2>
<p>
<ul>
    <li>Written in Python 3.</li>
    <li>Run "run.py" to start the game.</li>
    <li>Type "help" to find out about the commands to play the game e.g. "help", "help scores", etc.</li>
    <li>1 to 4 players can play the game.</li>
    <li>The rules of Yahtzee can be found <a href=http://www.yahtzee.org.uk/rules.html>here.</a></li>
    <li>Colours work if the game is run inside PyCharm IDE.</li>
    <li>A high score table is saved as "PyYahtzee.hst".</li>
</ul>
</p>
<h2>Structure</h2>
<h3>Text Version</h3>
<p>The game is structured using the <strong>Model-View-Controller</strong> paradigm:-<p>
<ul>
<li><strong>Model</strong> - the "game.py" file in the "model" module holds the core of the game e.g. Player,
 Game, Turn.</li>
<li><strong>View</strong> - the "game_text_view.py" file in the "view" module holds the classes that display
 various aspects of the game e.g.the scorecard, the dice.</li>
<li><strong>Controller</strong> - the "controller.py" file has the CLI to play the game using the 
<a href="https://docs.python.org/3/library/cmd.html">cmd module</a>.</li>
</ul>
<p>The "utils" module has various utilities that are used by the game e.g. HighScoreTable, is_numeric(), pick(), confirm()</p>
<h3>Graphics Version</h3>
<p>The game is structured using the <strong>Model-View-Controller</strong> paradigm:-<p>
<ul>
<li><strong>Model</strong> - the same "game.py" as the text version.</li>
<li><strong>View</strong> - the "graphics.py" file in the "view" module holds the classes that display
 various aspects of the game e.g.the scorecard, the turn, etc.</li>
<li><strong>Controller</strong> - the "gui_controller.py" file has the GUI controller main loop.</li>
</ul>
