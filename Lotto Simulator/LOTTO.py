
# mozliwosc gry z plusem lub bez

import random, custom_numbers


print("""\nThis is a polish lotery game "LOTTO" simulator.
It's made for practice and to demonstrate how small are chances to win larger price.
The game let's you choose 6 of 49 numbers.
You can choose your own numbers or get them randomly chosen by beting machine.\n""")


yrs_playing = int(input("How many years would you like to play? "))
draws = yrs_playing * 3 * 52  # 3 games in a week
available_numbers = range(1, 50)


def beting_method():
    options = ["custom", "random"]
    while True:
        try:
            method = input("\nWould you like to play with randomly generated numbers or your own?  (custom / random) \n")
        except:
            print("Try again")
            continue
        if method not in options:
            print("\nChoose one of possible options (custom / random)\n")
            continue
        if method == "custom":
            return 1
        else:
            return 2

result = {
    "szostka (all numbers)" : 0,
    "piatka (5/6 numbers match)": 0,
    "czworka (4/6 numbers match)" : 0,
    "trojka (3/6 numbers match)" : 0
}


def random_numbers_game():
    for draw in range(draws):
        drawn_numbers = set(random.sample(available_numbers, 6))
        
        for bet in range(bets):
            chosen = set(random.sample(available_numbers, 6))
            hits = len(chosen.intersection(drawn_numbers))
            
            if hits == 6:
                result["szostka (all numbers)"] += 1
            elif hits == 5:
                result["piatka (5/6 numbers match)"] += 1
            elif hits == 4:
                result["czworka (4/6 numbers match)"] += 1
            elif hits == 3:
                result["trojka (3/6 numbers match)"] += 1
            else:
                pass

def custom_numbers_game():
    for draw in range(draws):
        drawn_numbers = set(random.sample(available_numbers, 6))
        hits = len(chosen.intersection(drawn_numbers))
        
        if hits == 6:
            result["szostka (all numbers)"] += 1
        elif hits == 5:
            result["piatka (5/6 numbers match)"] += 1
        elif hits == 4:
            result["czworka (4/6 numbers match)"] += 1
        elif hits == 3:
            result["trojka (3/6 numbers match)"] += 1
        else:
            pass

if beting_method() == 1:
    chosen = set(custom_numbers.chosen_numbers())
    custom_numbers_game()
    for x, y in result.items():
        print(x,"->", y)
    print(f"\nMoney spent on a game: {draws * 3} pln")


else:
    bets = int(input("\nHow many bets do you want to make for each game?\n"))
    random_numbers_game()
    print("\n You chose a random game\n")
    for x, y in result.items():
        print(x,"->", y)
    print(f"\nMoney spent on a game: {draws * bets * 3} pln")


