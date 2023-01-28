# Simulator for polish lotery game "LOTTO"

# mozliwosc gry z plusem lub bez

import random

print("""\nThis is a polish lotery game "LOTTO" simulator.
It's made for practice and to demonstrate how small are chances to win larger price.
The game let's you choose 6 of 49 numbers.
You can choose your own numbers or get them randomly chosen by beting machine.\n""")


# import custom_numbers

yrs_playing = 1
draws = yrs_playing * 3 * 52  # 3 games in a week
available_numbers = range(1, 50)
bets = 10

result = {
    "szostka (all numbers)" : 0,
    "piatka (5/6 numbers match)": 0,
    "czworka (4/6 numbers match)" : 0,
    "trojka (3/6 numbers match)" : 0
}

# wybrane = set(custom_numbers.numbers())

for draw in range(draws):
    
    wylosowane = set(random.sample(available_numbers, 6))
    
    for bet in range(bets):

        wybrane = set(random.sample(available_numbers, 6))

        trafienia = len(wybrane.intersection(wylosowane))
        
        if trafienia == 6:
            result["szostka (all numbers)"] += 1
        elif trafienia == 5:
            result["piatka (5/6 numbers match)"] += 1
        elif trafienia == 4:
            result["czworka (4/6 numbers match)"] += 1
        elif trafienia == 3:
            result["trojka (3/6 numbers match)"] += 1
        else:
            pass

for x, y in result.items():
    print(x,"->", y)
print(f"""\nMoney spent on a game: {draws*bets* 3} pln 

Money won: {result.get("trojka (3/6 numbers match)")*3}""")

    
    