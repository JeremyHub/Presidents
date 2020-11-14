# Presidents

Rules of the game (bear with me):

  In order to understand the program you really have to understand the rules of how the game works. If you have ever played any other card game that goes in “tricks” it will look familiar, such games include: hearts, spades, bridge, ect. The game plays out as such: the person who starts (the one with the four of clubs on the first round) plays any number of the same card (suits play no purpose in this game) and the next person must play the same number of a higher card. The play keeps going around like this until everyone has passed at which point the person who played the last set of cards “wins” the trick and gets to start the next one. The goal is to run out of cards. If someone can “match” a card (or set of cards) that someone else has played, and they do so as their play, they instantly win that trick and get to start the next one. Twos and threes have special properties in this game. Threes are wild, that is, if you are asked to play on two eights and you only have one nine and a three, you may play both your nine and the three as “two nines”. Threes cannot be used for “matching”. If someone has a two, that person can play a single two on their turn in order to instantly win any trick (even doubles, triples, ect) and start the next one (twos are the most powerful card in the game).
	
  Once everyone has gone out, the next round starts but with a few modifications. The play of the game is the exact same except that before the round starts the person who got out first (the president) gets the best two cards (best being: 2’s, then, 3’s, then, ace’s, king’s, queen’s, ect.) from the person who went out last (the ass). The vice president (second person to go out) gets the one best card from the “vice ass” (the person who went out second to last). After that happens the president gives any two cards to the ass and the VP gives any one card to the VA.
	
  There is an alternate way of playing where the ass and pres only exchange one card (still asses best and pres’ any). However, in this rule set VA gives any one card to VP and then VP gives any one card back to VA. The theory behind this second rule set is to be more fair to the “lower class” by having them pass less of their good cards but still give the upper class an advantage.

How the user interacts with the program:

  In the files you will find a python file called “script.py”, in this are tons of different example games that you can try. The main way that the user interacts with this program is simply by trying different games and either seeing the bots play the game or seeing the statistics that are created after the game(s) are finished.
  
  The way of creating different games is by creating game objects and then calling the startGame() method on them. The game object is the only one that the user should call and its parameters are explained in the “game” file under its __init__ function.
	
  There is another way that the user can interact with the game. That is, if one or more of the players in the game is the personInputPlayer. This player will ask for an input every time it is asked to play a card, allowing the user to play in the game. (see example calls to do this)
