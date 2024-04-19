# Blackjack

![Blackjack](documentation/blackjack)

Blackjack is one of the most famos caisino game. Requires not just luck, but knowlage of the best stategy. Try yourself against the house. Reach more than the house and take all the chips. [Blackjack](https://blackjack-nyz-4419f61705c1.herokuapp.com/)

You can play the real simulation of the game with real shuffling system with real odds, and rules. For learn more about the game read the relevant [Wikipedia](https://en.wikipedia.org/wiki/Blackjack) page.

## Contents
  - [Application goals](#application-goals)
  - [Planing](#planing)
  - [Featchers](#featchers)
    - [Loading screen](#loading-screen)
    - [Main menu](#main-menu)
    - [Leaderboard](#leaderboard)
    - [Login / registration](#login-/-registration)
    - [Game](#game)
    - [Shuffle](#shuffle)
    - [Bet](#bet)
    - [Deal](#deal)
    - [Player move](#player-move)
    - [Dealer move](#dealer-move)
    - [Turn end](#turn-end)
    - [](#)
    - [](#)
    - [](#)
    - [](#)

## Application goals

 - Have a "database" what holds the player names and their chips.
 - Possibility to register a new player.
 - Leaderboard amoung of the players by chips.
 - The players can enter the game with his name.
 - The game it self with real game flow.
   - Card shaffle and deal with the same probalities as in the real world.
   - Same rules, moves in the same order as in a real cassino.

## Planing

All the options what the player can do in the application is visible on the player experience flowchart below.

![Flowchart](documentation/blackjack-flowchart)

## Featchers

### Loading screen

As the application is started blackjack title and "loading..." text appear. The appliaction reachs out the google sheet via gspread, when it is succeed "Welcome!" text appears and we enter the main menu.

### Main menu

From here the player can
 - go to leaderboard
 - go to login / registration
 - or close the application.
Also the player can return here from everywhere.

### Leaderboard

Here shows up the top 10 player by chips.

### Login / registration

The player enter his player name here, if it's already exist than enters to the game. If isn't than he can register it if he decide to do so.

### Game

Game starts with shuffle than the players bet.

#### Shuffle

Everytime the cars are shuffled
  - in the beginning of the game
  - and if the most of the cards already played from the deck
the application notify the usere about it.

#### Bet

The player can place his bet.

#### Deal

After betting. The player gets 2 cards and the dealer one. These cards will be removed from the deck until a new shuffle. And the player can see the cards. In case of the player has blackjack the player wins except the dealer has also blackjack. In this case it's a tie.

#### Player move

Seeing the cards the player can decide his move.
 - He can either ask a new card
 - or stop.

#### Dealer move

After the player finished his turn. It's the dealers turn. All the new cards appers with a 2 second dealy.

#### Turn end

In the end the player gets his reward or loses his bet depending of he or the dealer had better cards or any of them busted and gets back his chips if it was a tie.
