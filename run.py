"""Terminal blackjack game."""
import gspread
import random
import time
from google.oauth2.service_account import Credentials
from player import Player

print("""
    ■   ■■■ ■■■ ■  ■   ■ ■■■ ■■■ ■  ■
    ■   ■ ■ ■   ■ ■    ■ ■ ■ ■   ■ ■
    ■■■ ■■■ ■   ■■     ■ ■■■ ■   ■■
    ■ ■ ■ ■ ■   ■ ■  ■ ■ ■ ■ ■   ■ ■
    ■■■ ■ ■ ■■■ ■  ■ ■■■ ■ ■ ■■■ ■  ■


        """)
print("Loading...")

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("black_jack")


def main():
    """
    Make main menu.

    Asks a command and navigates to the chosen site.
    """
    while(True):
        print("Blackjack main menu\n")
        print("Leaderboard(l), Quit(q), Login/Registration(r)")

        command = input()
        print()

        if(command == "l"):
            leaderboard()
        elif(command == "q"):
            print("Blackjack is closed!")
            return
        elif(command == "r"):
            login()
        else:
            print("Incorrect input!\n")


def leaderboard():
    """
    Show the leaderboard.

    Shows the top 10 player by credits,
    than leads back to the main menu.
    """
    print("==================================")
    print("    ////   Leaderboard   \\\\\\\\")
    print("==================================")

    chips = SHEET.worksheet("chips").get_all_values()
    # Get the data from the worksheet

    chip_number = []
    for i in range(len(chips[1])):
        chip_number.append(int(chips[1][i]))
    # Copy the chips but int

    for i in range(min(len(chip_number), 10)):
        # List the players, but max 10 of them

        max_index = chip_number.index(max(chip_number))
        # Index of the largest score

        if(i < 9):
            print(end=" ")
        # Add a space to the lines with single digit place
        print(f" {i+1}.", end=" ")
        # Write the place
        print(chips[0][max_index], end=" ")
        # Write the name of the player
        for i in range(20 - len(chips[0][max_index])):
            print(" ", end="")
        # Write as many space that it will be 20 long with the name
        print(chips[1][max_index])
        # Write the score
        chip_number[max_index] = 0
        # Set the current max to 0 so the next highest score can be find

    print("==================================")

    input("Quit(Enter)\n")
    print()
    # As the enter is pressed, go back to the main menu


def login():
    """
    Login or registrate.

    Asks the player for a player name.
    If it doesn't exist he can create it.
    It is possible to go back to the main menu.
    """
    print("Enter you name!\nQuit(q)")
    player = Player("0", "", 10000)
    player.name = input("\n")
    print()
    # Ask the player name

    chips = SHEET.worksheet("chips").get_all_values()
    # Load the players

    if(player.name == "q"):
        return
        # Go back to main if it was "q" instead of a name
    elif(player.name in chips[0]):
        player.index = chips[0].index(player.name) + 1
        # Get player index
        player.chips = int(chips[1][player.index-1])
        game(player)
        # Enter the game with the given name
    else:
        print("This player name doesn't exist! Do you want to register?")
        # If this player doesn't exist, give the opportunity to create it
        while(True):
            register = input("Yes(y), No(n)\n")
            # Players decison
            print()
            if(register == "y"):
                if(len(player.name) < 2 or len(player.name) > 16):
                    # If the player's name is too short or too long.
                    print("Name's length has to be between 3 and 15!\n")
                    login()
                    # Go back to login.
                    break
                elif(player.name[0] == " " or player.name[-1] == " "):
                    # If the player's name start or and with a space.
                    print("Player's name can't start or end with space!\n")
                    login()
                    # Go back to login.
                    break
                else:
                    create_player(player)
                # If it is "y" create a player.
                break
            elif(register == "n"):
                login()
                # If it is "n" go back to login.
                break
            else:
                print("Incorrect input!")
                # If the aswer is incorrect don't break the loop
                # and repeat the question.


def create_player(player):
    """Create player and start game."""
    chips_worksheet = SHEET.worksheet("chips")
    # Get the chips worksheet
    player.index = len(chips_worksheet.row_values(1)) + 1
    # Get the last player index and add one
    chips_worksheet.update_cell(1, player.index, player.name)
    # Add the new player to the sheet
    chips_worksheet.update_cell(2, player.index, player.chips)
    # Add him 10000 chips
    game(player)
    # Start the game


def game(player):
    """
    Game handler.

    Calls subparts of the game pass data between them.
    """
    deck = shuffle()

    while(True):

        player_bet = bet(player)
        # Player bets and the bet is saved in a variable
        if (player_bet == "q"):
            return
            # Go back to main menu

        player_cards = []
        # Create / recreate players hand
        dealer_cards = []
        # Create / recreate dealers hand
        player_cards.append(deck.pop())
        # Add a card from deck to player
        dealer_cards.append(deck.pop())
        # Add a card from deck to dealer
        player_cards.append(deck.pop())
        # Add an other card from deck to player

        display_cards(player_cards, dealer_cards)
        # Show 2 cards for the player and one for the dealer

        player_move_result = player_move(player_cards, dealer_cards, deck)
        if (player_move_result[0] == "q"):
            lose(player_bet, player)
            # Player lose his bet
            return
            # Go back to main menu
        elif (player_move_result[0] == "bust"):
            print("Bust")
            lose(player_bet, player)
        else:
            player_cards = player_move_result[0]
            player_hand = player_move_result[2]
            # Assign players hands value in a variable
            deck = player_move_result[1]
            # Update deck

            dealer_move_result = dealer_play(player_cards, dealer_cards, deck)
            # Dealers turn
            dealer_hand = dealer_move_result[0]
            # Assign dealers hands value in a variable
            deck = dealer_move_result[1]
            # Update deck

            end_of_turn(player_hand, dealer_hand, player_bet, player)
            # Calculate the winner and update the accont

        if (len(deck) < 90):
            deck = shuffle()

        chips_worksheet = SHEET.worksheet("chips")
        player.chips = int(chips_worksheet.cell(2, player.index).value)
        # Update chips


def shuffle():
    """Give back 4 shuffled deck."""
    print("Shuffle cards.\n")
    card_types = ["♠", "♥", "♦", "♣"]
    card_ranks = [str(card) for card in range(2, 11)] + ["J", "Q", "K", "A"]
    # A list of card numbers
    deck_in_order = []
    for c_type in range(4):
        for c_rank in range(13):
            for deck_number in range(4):
                deck_in_order.append(card_types[c_type] + card_ranks[c_rank])
    # Create four decks in order
    card_order = [random.randint(0, d) for d in reversed(range(208))]
    # Create a list of random number in a decreasing range

    shuffled_deck = []
    for i in range(208):
        shuffled_deck.append(deck_in_order.pop(card_order[i]))
        # Take a random card from the ordered to the unorderd deck
    return shuffled_deck


def bet(player):
    """Ask and wait for bet."""
    while(True):

        print(f"Place your bet! Your chips: {player.chips}$")
        bet = input("Bet(Any number), Quit(q)\n")
        # Input
        print()
        if(bet == "q"):
            return "q"
            # Return q so the game def can also return
        else:
            try:
                bet_int = int(bet)
                # Try to turn into an int the input
                if(player.chips < bet_int):
                    print("You don't have enough chips!\n")
                    # If not enough chips
                elif(0 >= bet_int):
                    print("Bet must be bigger than 0\n")
                    # In case of negative number or 0
                else:
                    return bet_int
                    # In case of a valid number return the bet
            except ValueError:
                print("Wrong value!\n")
                # If it is not a number


def display_cards(player_cards, dealer_cards):
    """Display the cards for the player."""
    print("==================================")
    print("Dealer's hand")
    for i in range(len(dealer_cards)):
        print(f"[{dealer_cards[i]}]", end="")
        # Display the dealers cards
    print("\n\nYour hand")
    for i in range(len(player_cards)):
        print(f"[{player_cards[i]}]", end="")
        # Display the player cards
    print("\n")


def player_move(cards, dealer_cards, deck):
    """
    Player's turn to play.

    Ask player's move. If he asks card, stop or quit.
    If he asks more card, he will be asked again if he doesn't bust or get 21.
    It returns q for quit, "bust",
    "blackjack or the number what the is in the player hand
    and the updated deck."
    """
    card_values = [card_value(cards[0][1]), card_value(cards[1][1])]
    # Collect the value of the player cards.

    if(card_values[0] + card_values[1] == 110):
        # For easier calculation ace worth 100 in the app
        # Ace and a card what worth 10 is a blackjeck
        print("Blackjack!\n")
        # Print for the player that he has blackjack
        return cards, deck, "blackjack"
        # Return the result and the deck

    while(True):
        # Loop till the player doesn't stop or have more than 20
        move = input("Card(c), Stop(s), Quit(q)\n")
        # Players options
        time.sleep(1)
        # Wait one second
        if (move == "c"):
            # If the player ask for a card
            cards.append(deck.pop())
            # Move card from deck to player
            display_cards(cards, dealer_cards)
            # Display the cards agian
            card_values.append(card_value(cards[-1][1]))
            # Catch the new cards value
            value_of_hand = hand_value(card_values)
            # Calculate the value of players hand

            if(value_of_hand > 21):
                # If the player have more than 21
                return "bust", deck, "bust"
                # Return "bust" and the updated deck

            elif(value_of_hand == 21):
                # If the player have 21
                return cards, deck, 21
                # Return 21 and the new deck
                # If its under 21 the loop continues

        elif(move == "s"):
            # If the player decided to stop
            value_of_hand = hand_value(card_values)
            return cards, deck, value_of_hand
            # Return "s" and the new deck

        elif(move == "q"):
            # If the player decided to quit
            return "q", deck, "q"
            # Return "q" and the new deck
        else:
            print("Invalid move!")
            # In case of other input this error massage comes


def card_value(card):
    """
    Take the cards rank and return a cards value.

    In case of ace return 100.
    """
    if(card == "A"):
        return 100
        # If it's ace return 100
    elif(card == "J" or card == "Q" or card == "K" or card == "1"):
        return 10
        # If the rank is J, Q, K or 10 returns 10
    else:
        int_card = int(card)
        return int_card
        # If the rank is a number return the number but first turn it to an int


def hand_value(hand):
    """Count and return the value of the hand."""
    sum_of_hand = sum(hand)
    # Sum the value of the hand
    while(sum_of_hand > 110):
        # If the current value is more then 110 it means
        # there is an ace, but if its value would be 11 it would be bust
        # So it has to be 1
        sum_of_hand -= 99
        # 100-99=1 We got the real value for this ace
        # Because more ace can have the value 1 it is in a loop
    if(sum_of_hand > 100):
        # If the value is between 101 and 110
        # there is an ace what has the value of 11
        sum_of_hand -= 89
        # 100-89=11
    return sum_of_hand
    # Return the value of the hand


def dealer_play(player_cards, dealer_cards, deck):
    """Display dealers turn."""
    dealer_card_values = [card_value(dealer_cards[0][1])]
    # Add player cards value to a list
    while(True):
        time.sleep(3)
        # wait 3 second
        dealer_cards.append(deck.pop())
        # Move a card from deck to dealers hand
        dealer_card_values.append(card_value(dealer_cards[-1][1]))
        # Add the new cards value to the list
        display_cards(player_cards, dealer_cards)
        # Display the current cards
        value_of_dealer_hand = hand_value(dealer_card_values)
        # Calculate the value of dealers hand
        if (value_of_dealer_hand > 21):
            return "bust", deck
            # If the dealer has more than 21
            # return "busted", and the updated deck
        elif (value_of_dealer_hand == 21 and len(dealer_cards) == 2):
            return "blackjack", deck
            # If the dealer has 21 from two cards
            # return 21 and the updated deck
        elif (value_of_dealer_hand > 16):
            return value_of_dealer_hand, deck
            # If the dealer has more than 16
            # return this value and the updated deck
            # If the dealer has less or equal 16
            # the dealer pull an other card the loop contineu


def end_of_turn(player_hand_value, dealer_hand_value, player_bet, player):
    """
    Commpear the players and the dealers hand.

    Than call either the win or lose def or none of them.
    """
    if (player_hand_value == "blackjack"):
        if (dealer_hand_value == "blackjack"):
            # If both the player and the dealer have blackjack
            print("Tie!")
            # Print tie, the turn is ended
        else:
            # If only the player has blackjack
            print("You won!")
            # Print win
            if (player_bet % 2 == 1):
                player_bet += 1
            # In case of odd bet add 1 to it
            # to avoid flooting number in the next step
            win(player_bet * 1.5, player)
            # Add the bet 1.5 times to players account
    elif (dealer_hand_value == "blackjack"):
        # If only the dealer has blackjack
        print("You lost!")
        # Print lose
        lose(player_bet, player)
        # Take the bet from the players account
    elif (dealer_hand_value == "bust"):
        # If the dealer busted
        print("You won!")
        # Print win
        win(player_bet, player)
        # Add the bet to the players account
    elif (player_hand_value > dealer_hand_value):
        # If the player have bigger number
        print("You won!")
        # Print win
        win(player_bet, player)
        # Add the bet to the players account
    elif (player_hand_value == dealer_hand_value):
        # If the player and the dealer have the same number
        print("Tie!")
        # Print tie
    elif (player_hand_value < dealer_hand_value):
        # If the player has less
        print("You lost!")
        # Print lose
        lose(player_bet, player)
        # Take the bet from the players account


def win(player_bet, player):
    """Add the bet to the players account."""
    chips_worksheet = SHEET.worksheet("chips")
    # Get the chips worksheet
    player.chips += player_bet
    # Add the bet to the chips
    chips_worksheet.update_cell(2, player.index, player.chips)
    # Load back the updated chips


def lose(player_bet, player):
    """Subtrack the bet from the players account."""
    chips_worksheet = SHEET.worksheet("chips")
    # Get the chips worksheet
    player.chips -= player_bet
    # Subtrack the bet from the chips
    chips_worksheet.update_cell(2, player.index, player.chips)
    # Load back the updated chips


print()
print("Welcome!\n")
main()
