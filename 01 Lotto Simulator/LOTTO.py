
import random, custom_numbers


print("""\nThis is a polish lotery game "LOTTO" simulator.
It's made for practice and to demonstrate how small chances are to win larger price.
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

def plus_game_decision():
    options = ["y", "n"]
    while True:
        try:
            decision = input("\nWould you like to play with \"PLUS\" option?  (y / n) \n")
        except:
            print("Try again")
            continue
        if decision not in options:
            print("\nChoose one of possible options: (y / n)\n")
            continue
        elif decision == "y":
            return True
        else:
            return False

result = {
    "szostka (all numbers)" : 0,
    "piatka (5/6 numbers match)": 0,
    "czworka (4/6 numbers match)" : 0,
    "trojka (3/6 numbers match)" : 0,
    "\"plus\" game" : 0,
}


def random_numbers_game():
    for draw in range(draws):
        drawn_numbers = set(random.sample(available_numbers, 6))

        if plus_game:
            drawn_plus_numbers = set(random.sample(available_numbers, 6))
        
        for bet in range(bets):
            chosen = set(random.sample(available_numbers, 6))
            hits = len(chosen.intersection(drawn_numbers))
            if plus_game:
                hits_plus = len(chosen.intersection(drawn_plus_numbers))
                if hits_plus == 6:
                    result["plus game"] += 1

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
        if plus_game:
            drawn_plus_numbers = set(random.sample(available_numbers, 6))

        hits = len(chosen.intersection(drawn_numbers))
        if plus_game:
                hits_plus = len(chosen.intersection(drawn_plus_numbers))
                if hits_plus == 6:
                    result["plus game"] += 1
        
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
    plus_game = plus_game_decision()
    custom_numbers_game()

    print("\n You chose to play with you own numbers\n")
    print(f"You played {draws} times.\n")

    for x, y in result.items():
        print(x,"->", y)
    print(f"\nMoney spent on a games: {draws * 3} pln")


else:
    while True:
        try:
            bets = int(input("\nHow many bets do you want to make for each game?\n"))
            break
        except:
            print("Type a number")
            continue

    plus_game = plus_game_decision()
    random_numbers_game()
    
    print("\n You chose a random game\n")
    print(f"You played {draws} times, with {bets} bets for each game\n{draws * bets} bets.\n")
    
    for x, y in result.items():
        print(x,"->", y)
    print(f"\nMoney spent on a games: {draws * bets * 3} pln")


