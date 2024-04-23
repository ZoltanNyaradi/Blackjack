# Testing

## Start

| Feature | Action | Expected Result | Result |
|---|---|---|---|
| Loading screen | Start app | The logo and "Loading..." appear | Works |
| Game loaded | Wait after "Loading..." | "Welcome!" and Main Menu appear  | Works |

## Main menu

| Feature | Action | Expected Result | Result |
|---|---|---|---|
| Close game | Enter "q" | Closing text comes up, app stops | Works |
| Leaderboard | Enter "l" | Leaderboard opens | Works |
| Login/ Registration | Enter "r" | Login/ Registration opens | Works |
| Incorrect input | Enter anything else | Error message comes up and stays in main | Works |

## Leaderboard

| Feature | Action | Expected Result | Result |
|---|---|---|---|
| Leaderboard | Enter to leaderboard | Top 10 player comes up in order | Works |
| Back to Main | Enter anything | Main opens | Works |
| Name length | Enter under 3 or over 15 | Error message comes up after confirmation | Works |
| Blank name | Enter name starts or ends with space | Error message comes up after confirmation  | Works |

## Login/ Registration

| Feature | Action | Expected Result | Result |
|---|---|---|---|
| Login | Enter existing name | Game start with the correct player | Works |
| Ask registration | Enter new name | Confirmation question comes up | Works |
| Back to Main | Enter "q" | Main opens | Works |


### Confirmation

| Feature | Action | Expected Result | Result |
|---|---|---|---|
| No registration | Enter "n" | Login/ Registration opens | Works |
| Registration | Enter "y" | Registrates new player with 10000 and the game starts | Works |Doubble

## Game

### Shuffle

| Feature | Action | Expected Result | Result |
|---|---|---|---|
| Shuffle | Start game | "Shuffle cards." message comes up | Works |
| Reshuffle | Play till 90 cards left | "Shuffle cards." message comes up | Works |

### Bet

| Feature | Action | Expected Result | Result |
|---|---|---|---|
| Bet | Enter a correct number | Turn starts | Works |
| Bet too much | Enter more than number of chips | Error message comes up | Works |
| Bet too small | Enter 0 or under | Error message comes up | Works |
| Bet non-integer or non-number | Enter non-integer number or enter not a number | Error message comes up | Works |
| Back to Main | Enter "q" | Main opens | Works |

### Player move

| Feature | Action | Expected Result | Result |
|---|---|---|---|
| Blackjack | Get blackjack | Player move skipped | Works |
| Ask card | Enter "c" | Gets a new card | Works |
| Bust | Get more than 21 after new card | Bust message | Works |
| 21 | Get 21 after new card | Player can't make more move | Works |
| Stop | Enter "s" | Player turns end | Works |
| Back to Main | Enter "q" | Main opens | Works |
| Invalid move | Enter anything else | Error message comes up | Works |

### Dealer move

| Feature | Action | Expected Result | Result |
|---|---|---|---|
| Bust | Get more than 21 | Dealer stops | Works |
| Blackjack | Get blackjack | Dealer stops | Works |
| Stop | Get between 17-20  | Dealer stops | Works |
| Pull | Get 16 or under | Dearer pulls card | Works |

### Game End

| Feature | Action | Expected Result | Result |
|---|---|---|---|
| Player blackjack | Only the player has blackjack | Player win 1.5x bet | Works |
| Dealer blackjack | Only the dealer has blackjack | Player lose bet | Works |
| Both blackjack | Both have blackjack | Player get back bet | Works |
| Player bust | Player have bust | Player lose bet | Works |
| Dealer bust | Only the dealer bust | Player win bet | Works |
| Player has bigger | Player has bigger | Player win bet | Works |
| Dealer has bigger | Dealer has bigger | Player lose bet | Works |
| Tie | Both have the same number | Player get back bet | Works |

### Others

| Feature | Action | Expected Result | Result |
|---|---|---|---|
| Dispaly | Correct bet, Player move new card, Dealer move new car | Display the card when there is a new one | Works |
| J Q K | Play till these cards appears | These cards worth 10  | Works |
| A | Play till both scenario | Ace worth 1 or 11  | Works |
