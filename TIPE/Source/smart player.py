import random
from time import sleep

a = [1, 3, 5, 7]
next_to_that = None
sp = None

def one_way(row):
    global a
    a[row - 1] -= 1
    print(f"Changing image for row {row}")0

def player_draught(row):
    global next_to_that, a
    if sum(a) != 0:
        if (next_to_that == 5 or next_to_that == 6) and a[row - 1] != 0:
            next_to_that = row
        if next_to_that == row and a[row - 1] != 0:
            one_way(row)
        if sum(a) == 0:
            print("Désolé... J'ai gagné!")

def m_way(row):
    global sp, a
    while a[row - 1] < sp:
        sp -= 1
        print(f"Changing image for row {row}")
        sleep(0.1)  # Ajout d'un délai pour simuler l'attente

def randomize():
    global iran
    iran = random.randint(0, 134456)

def chance(imax):
    global iran
    iran = (iran * 8121 + 28411) % 134456
    return int(iran / 134456 * imax)

def winning_position():
    q = (a[0] ^ a[1] ^ a[2] ^ a[3]) == 0
    r = (a[0] | a[1] | a[2] | a[3]) == 1
    s = q ^ r
    return s

def computer_draught():
    global next_to_that, a, sp
    if sum(a) != 0:
        if next_to_that != 5 and sum(a) != 0:
            next_to_that = 5
            z = chance(4) + 1
            if winning_position():
                while a[z - 1] == 0:
                    z = (z % 4) + 1
                one_way(z)
            else:
                while not winning_position():
                    z = (z % 4) + 1
                    while a[z - 1] == 0:
                        z = (z % 4) + 1
                    sp = a[z - 1]
                    while not winning_position() and a[z - 1] != 0:
                        a[z - 1] -= 1
                    if not winning_position():
                        a[z - 1] = sp
                m_way(z)
            sleep(0.1)  # Ajout d'un délai pour simuler l'attente
            if sum(a) == 0:
                print("Vous avez GAGNÉ!!! Félicitations...")

def new_game():
    global a, next_to_that
    a = [1, 3, 5, 7]
    next_to_that = 6

def draw(nr):
    if a[nr - 1] > 0:
        print(f"Clicked on row {nr}")
        player_draught(nr)
        computer_draught()
    else:
        print(f"Row {nr} is already empty")
