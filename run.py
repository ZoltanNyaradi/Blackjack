import gspread
import random
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
    num_of_chips = int(chips_worksheet.cell(2,player_index).value)
    # Get player chips
    
    ## while(True):

    deck = shuffle()
    # Create a shuffled deck

    # while(True):
    player_bet = bet(num_of_chips)
    if (player_bet == "q"):
        return 

    player_cards = []
    dealer_cards = []
    player_cards.append(deck.pop())
    dealer_cards.append(deck.pop())
    player_cards.append(deck.pop())
    dealer_cards.append(deck.pop())

    print(player_cards)
    print(dealer_cards)
    # deal()
        # display cards()#

    # while()

    # play()
        # display cards()

    # dealer_play()
        # display cards()
    # end_of_the_turn()

    # deck_check()

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
                except():
                    print("Wrong value!\n")
                        # If it is not a number

print()
print("Welcome!\n")
#main()
game("Zoltan")