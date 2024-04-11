print("Loading...")

import gspread
from google.oauth2.service_account import Credentials

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
    print("Blackjack main menu\n")

    print('For leaderboard enter: "l"')
    print('To close the application enter: "q"')
    print("To login just enter anything else")

    command=input()
    print()

    if(command=="l"):
        leaderboard()
    elif(command=="q"):
        print("Blackjack is closed!")
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
    main()
    # As the enter is pressed, it goes back to the main menu

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
        main()
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
    print("This is the game")

print()
print("Welcome!\n")
main()