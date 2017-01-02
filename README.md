# yahtzee
<html>
<body>
<h1>Welcome to PyYahtzee</h1>
<h2>Getting Started</h2>
<p>
Run "run.py" to start the game<br>
Rules of Yahtzee can be found here - http://www.yahtzee.org.uk/rules.html<br>
Colours work if the game is run inside PyCharm IDE<br>
</p>
<h2>Structure</h2>
<p>The game is structured using the <strong>Model-View-Controller</strong> paradigm<p>
<ul>
<li><strong>Model</strong> - the game.py file in the "model" module holds the core of the game e.g. Player, Game, Turn</li>
<li><strong>View</strong> - the "game_text_view.py" file in the "view" module holds the classes that display various aspects of the game e.g.the scorecard, the dice</li>
<li><strong>Controller</strong> - the controller.py file has the CLI to play the game using the cmd module</li>
</ul>
</body>
</html>
