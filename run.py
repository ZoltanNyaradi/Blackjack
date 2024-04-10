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

    input("quit(Enter)")
    print()
    main()
    # As the enter is pressed, it goes back to the main menu

def login():
    print("login")

print()
print("Welcome!\n")
main()