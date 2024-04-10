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

    print('For leaderboard enter "l"')
    print('To close the application enter:"q"')
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
    print("leaderboard")

def login():
    print("login")

print()
print("Welcome!\n")
main()