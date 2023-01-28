# Choosing custom numbers for Lotto game

def numbers():
    num_list = []
    for i in range (1,7):
        while True:
            try:
                a = int(input(f"Choose your {i} number (1-49) "))
            except: 
                print("Choose only a number from 1 to 49")
                continue
            if a < 1 or a > 49:
                print("\nChoose only from 1 to 49!\n")
                continue
            elif a in num_list:
                print("\nThis number has been chosen already\n")
                continue
            else:
                num_list.append(a)
                break
    
    num_list.sort()
    return num_list


