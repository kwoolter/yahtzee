<html>
<body>
<h1>Welcome to PyYahtzee</h1>
<p>By kwoolter</p>
<p>(c) 2017</p>
<h2>Getting Started</h2>
<p>
<ul>
<li>Run "run.py" to start the game.</li>
<li>Type "help" to find out about the commands to play the game e.g. "help", "help scores", etc.</li>
<li>1 to 4 players can play the game.</li>
<li>The rules of Yahtzee can be found <a href=http://www.yahtzee.org.uk/rules.html>here.</a></li>
<li>Colours work if the game is run inside PyCharm IDE.</li>
<li>A high score table is saved as "PyYahtzee.hst".</li>
</ul>
</p>
<h2>Structure</h2>
<p>The game is structured using the <strong>Model-View-Controller</strong> paradigm:-<p>
<ul>
<li><strong>Model</strong> - the "game.py" file in the "model" module holds the core of the game e.g. Player,
 Game, Turn.</li>
<li><strong>View</strong> - the "game_text_view.py" file in the "view" module holds the classes that display
 various aspects of the game e.g.the scorecard, the dice.</li>
<li><strong>Controller</strong> - the "controller.py" file has the CLI to play the game using the 
cmd module.</li>
</ul>
<p>The "utils" module has various utilities that are used by the game e.g. HighScoreTable, is_numeric(), pick(), confirm()</p>
</body>
</html>
