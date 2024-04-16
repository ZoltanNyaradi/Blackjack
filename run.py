import gspread
import random
import time
from google.oauth2.service_account import Credentials

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
    Main menu

    Asks a command and navigates to the chosen site.
    """
    while(True):
        print("Blackjack main menu\n")
        print("Leaderboard(l), Quit(q), Login(Enter)")

        command=input()
        print()

        if(command=="l"):
            leaderboard()
        elif(command=="q"):
            print("Blackjack is closed!")
            return
        else:
            login()

def leaderboard():
    """
    Shows the leaderboard

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

    for i in range(min(len(chip_number),10)):
        # List the players, but max 10 of them
        
        max_index = chip_number.index(max(chip_number))
        # Index of the largest score

        if(i<9):
            print(end=" ")
        # Add a space to the lines with single digit place
        print(f" {i+1}.",end=" ")
        # Write the place
        print(chips[0][max_index],end=" ")
        # Write the name of the player
        for i in range(20-len(chips[0][max_index])):
            print(" ",end="")
        # Write as many space that it will be 20 long with the name
        print(chips[1][max_index])
        # Write the score
        chip_number[max_index] = 0
        # Set the current max to 0 so the next highest score can be find

    print("==================================")

    input("Quit(Enter)")
    print()
    # As the enter is pressed, go back to the main menu

def login():
    '''
    Login or register

    Asks the player for a player name.
    If it doesn't exist he can create it.
    It is possible to go back to the main menu.
    '''
    print("Enter you name!\nQuit(q)")
    player = input()
    print()
    # Ask the player name

    chips = SHEET.worksheet("chips").get_all_values()
    # Load the players

    if(player=="q"):
        return
        # Go back to main if it was "q" instead of a name
    elif(player in chips[0]):
        game(player)
        # Enter the game whit the given name
    else:
        print("This player doesn't exist! Do you want to register?")
        # If this player doesn't exist, give the opportunity to create it
        while(True):
            register = input("Yes(y), No(n): ")
            # Players decison
            print()
            if(register == "y"):
                create_player(player)
                # If it is "y" create a player
                break
            elif(register == "n"):
                login()
                # If it is "n" go back to login
                break
            else:
                print("Incorrect input!")
                # If the aswer is incorrect don't break the loop
                # and repeat the question

def create_player(player):
    """
    Create player and start game
    """
    chips_worksheet = SHEET.worksheet("chips")
    # Get the chips worksheet
    new_player_index = len(chips_worksheet.row_values(1))+1
    # Get the last player index and add one
    chips_worksheet.update_cell(1,new_player_index,player)
    # Add the new player to the sheet
    chips_worksheet.update_cell(2,new_player_index,1000)
    # Add him 1000 chips
    game(player)
    # Start the game

def game(player):
    
    chips_worksheet = SHEET.worksheet("chips")
    # Get the chips worksheet
    player_index = chips_worksheet.row_values(1).index(player)+1
    # Get player index
    
    deck = shuffle()

    while(True):
        num_of_chips = int(chips_worksheet.cell(2,player_index).value)
        # Get player chips

        player_bet = bet(num_of_chips)
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
        if (player_move_result[0]=="q"):
            lose(player_bet, player_index)
            # Player lose his bet
            return
            # Go back to main menu
        elif (player_move_result[0]=="bust"):
            print("Bust")
            lose(player_bet, player_index)
        else:
            player_cards = player_move_result[0]
            player_hand_value = player_move_result[2]
            # Assign players hands value in a variable
            deck = player_move_result[1]
            # Update deck

            dealer_move_result = dealer_play(player_cards, dealer_cards, deck)
            # Dealers turn 
            dealer_hand_value = dealer_move_result[0]
            # Assign dealers hands value in a variable
            deck = dealer_move_result[1]
            # Update deck

            end_of_turn(player_hand_value, dealer_hand_value, player_bet, player_index)
            # Calculate the winner and update the accont

            if (len(deck)<120):
                deck = shuffle()

def shuffle():
    """
    Give back 4 shuffled deck
    """
    card_types = ["♠","♥","♦","♣"]
    card_numbers = [str(card_number) for card_number in range(2,11)]+["J","Q","K","A"]
    # A list of card numbers
    deck_in_order =  [card_types[card_type]+card_numbers[card_number] for card_type in range(4) for card_number in range(13) for deck_number in range(4)]
    # Create four decks in order 
    shuffle_methode = [random.randint(0, deck_size) for deck_size in reversed(range(208))]
    # Create a list of random number in a decreasing range
    
    shuffled_deck = []
    for i in range(208):
        shuffled_deck.append(deck_in_order.pop(shuffle_methode[i]))
        # Take a random card from the ordered to the unorderd deck
    return shuffled_deck

def bet(num_of_chips):
    """
    Ask and wait for bet.
    """
    while(True):
            bet = input("Take your bet!\nBet(Any number), Quit(q)\n")
            # Input
            if(bet == "q"):
                return "q"
                # Return q so the game def can also return
            else:
                try:
                    bet_int = int(bet)
                    # Try to turn into an int the input
                    if(num_of_chips<bet_int):
                        print("You don't have inaf chips!\n")
                        # If not inaf chips
                    
                    elif(0>=bet_int):
                        print("Bet must be bigger than 0\n")
                        # In case of negative number or 0
                    else:
                        print()
                        return bet_int
                        # In case of a valid number return the bet
                except:
                    print("Wrong value!\n")
                        # If it is not a number

def display_cards(player_cards, dealer_cards):
    """
    Display the cards for the player
    """
    print("Dealer's hand")
    for i in range(len(dealer_cards)):
        print(f"[{dealer_cards[i]}]",end="")
        # Display the dealers cards
    print("\n\nYour hand")
    for i in range(len(player_cards)):
        print(f"[{player_cards[i]}]",end="")
        # Display the player cards
    print("\n")

def player_move(player_cards, dealer_cards, deck):
    """
    Player's turn to play

    Ask player's move. If he asks card, stop or quit.
    If he asks more card, he will be asked again if he doesn't bust or get 21.
    It returns q for quit, "bust", "blackjack or the number what the is in the player hand
    and the updated deck."
    """
    player_card_values = [card_value(player_cards[0][1]), card_value(player_cards[1][1])]
    # Collect the value of the player cards. 

    if(player_card_values[0] + player_card_values[1] == 110):
        # For easier calculation ace worth 100 in the app
        # Ace and a card what worth 10 is a blackjeck
        print("Blackjack!\n")
        # Print for the player that he has blackjack
        return player_cards, deck, "blackjack"
        # Return the result and the deck

    while(True):
        # Loop till the player doesn't stop or have more than 20
        move = input("Card(c), Stop(s), Quit(q)\n")
        # Players options

        if (move=="c"):
            # If the player ask for a card
            player_cards.append(deck.pop())
            # Move card from deck to player
            display_cards(player_cards, dealer_cards)
            # Display the cards agian
            player_card_values.append(card_value(player_cards[-1][1]))
            # Catch the new cards value
            value_of_hand = hand_value(player_card_values)
            # Calculate the value of players hand

            if(value_of_hand > 21):
                # If the player have more than 21
                return "bust", deck, "bust"
                # Return "bust" and the updated deck

            elif(value_of_hand == 21):
                # If the player have 21
                return player_cards, deck, 21
                # Return 21 and the new deck
                # If its under 21 the loop continues

        elif(move=="s"):
            # If the player decided to stop
            value_of_hand = hand_value(player_card_values)
            return player_cards, deck, value_of_hand
            # Return "s" and the new deck 

        elif(move=="q"):
            # If the player decided to quit
            return "q", deck, "q"
            # Return "q" and the new deck
        else:
            print("Invalid move!")
            # In case of other input this error massage comes and the loop continue 
        
def card_value(card):
    """
    Take the cards rank and return a cards value.
    In case of ace return 100.
    """
    if(card=="A"):
        return 100
        # If it's ace return 100
    elif(card=="J" or card=="Q" or card=="K"):
        return 10
        # If the rank is J Q or K returns 10
    else:
        int_card = int(card)
        return int_card
        # If the rank is a number return the number but first turn it to an int

def hand_value(hand):
    """
    Count and return the value of the hand
    """
    sum_of_hand = sum(hand)
    # Sum the value of the hand
    while(sum_of_hand>110):
        # If the current value is more then 110 it means
        # there is an ace, but if its value would be 11 it would be bust
        # So it has to be 1
        sum_of_hand-=99
        # 100-99=1 We got the real value for this ace
        # Because more ace can have the value 1 it is in a loop
    if(sum_of_hand>100):
        # If the value is between 101 and 110 there is an ace what has the value of 11
        sum_of_hand-=89
        # 100-89=11
    return sum_of_hand
        # Return the value of the hand

def dealer_play(player_cards, dealer_cards, deck):
    """
    Display dealers turn
    """
    dealer_card_values = [card_value(dealer_cards[0][1])]
    # Add player cards value to a list
    while(True):
        time. sleep(2)
        # wait 2 second
        dealer_cards.append(deck.pop())
        # Move a card from deck to dealers hand
        dealer_card_values.append(card_value(dealer_cards[-1][1]))
        # Add the new cards value to the list
        display_cards(player_cards, dealer_cards)
        # Display the current cards
        value_of_dealer_hand = hand_value(dealer_card_values)
        # Calculate the value of dealers hand

        if (value_of_dealer_hand>21):
            return "bust", deck
            # If the dealer has more than 21 return "busted", and the updated deck
        elif (value_of_dealer_hand==21 and len(dealer_cards)==2):
            return "blackjack", deck
            # If the dealer has 21 from two cards return 21 and the updated deck 
        elif (value_of_dealer_hand>16):
            return value_of_dealer_hand, deck
            # If the dealer has more than 16 return this value and the updated deck
            # If the dealer has less or equal 16 the dealer pull an other card the loop contineu

def end_of_turn(player_hand_value, dealer_hand_value, player_bet, player_index):
    """
    Commpear the players and the dealers hand.
    Than call either the win or lose def or none of them. 
    """
    if (player_hand_value=="blackjack"):
        if (dealer_hand_value=="blackjack"):
            # If both the player and the dealer have blackjack
            print("Tie!")
            # Print tie, the turn is ended
        else:
            # If only the player has blackjack
            print("You won!")
            # Print win
            if (player_bet%2==1):
                player_bet+=1
            # In case of odd bet add 1 to it to avoid flooting number in the next step 
            win(player_bet*1.5, player_index)
            # Add the bet 1.5 times to players account
    elif (dealer_hand_value=="blackjack"):
        # If only the dealer has blackjack
        print("You lost!")
        # Print lose
        lose(player_bet, player_index)
        # Take the bet from the players account
    elif (dealer_hand_value=="bust"):
        # If the dealer busted
        print("You won!")
        # Print win
        win(player_bet, player_index)
        # Add the bet to the players account
    elif (player_hand_value>dealer_hand_value):
        # If the player have bigger number
        print("You won!")
        # Print win
        win(player_bet, player_index)
        # Add the bet to the players account
    elif (player_hand_value==dealer_hand_value):
        # If the player and the dealer have the same number 
        print("Tie!")
        # Print tie
    elif (player_hand_value<dealer_hand_value): 
        # If the player has less
        print("You lost!")
        # Print lose
        lose(player_bet, player_index)
        # Take the bet from the players account

def win(player_bet, player_index):
    """
    Add the bet to the players account.
    """
    chips_worksheet = SHEET.worksheet("chips")
    # Get the chips worksheet
    num_of_chips = int(chips_worksheet.cell(2, player_index).value)
    # Get the chips from the worksheet
    num_of_chips += player_bet
    # Add the bet to it
    chips_worksheet.update_cell(2, player_index, num_of_chips)
    # Load back the updated chips

def lose(player_bet, player_index):
    """
    Subtrack the bet from the players account
    """
    chips_worksheet = SHEET.worksheet("chips")
    # Get the chips worksheet
    num_of_chips = int(chips_worksheet.cell(2, player_index).value)
    # Get the chips from the worksheet
    num_of_chips -= player_bet
    # Subtrackt the bet from it
    chips_worksheet.update_cell(2, player_index, num_of_chips)
    # Load back the updated chips

print()
print("Welcome!\n")
#main()
game("Zoltan")