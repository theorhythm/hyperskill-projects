import random

print("How many pencils would you like to use:")
while True:
    pencils = input()
    if not pencils.isdigit():
        print("The number of pencils should be numeric")
        continue
    if int(pencils) == 0:
        print("he number of pencils should be positive")
        continue
    break


pencils = int(pencils)
players = ["John", "Jack"]
print(f"Who will be the first ({players[0]}, {players[1]}):")
first_player = input()

while first_player not in players:
    print(f"Choose between '{players[0]}' and '{players[1]}'")
    first_player = input()

idx = 0 if first_player == players[0] else 1

while pencils > 0:
    print('|' * pencils)
    print(f"{players[idx]}'s turn")
    if idx % 2 == 1:
        if pencils > 1:
            if pencils % 4 == 1:
                pencils_removed = random.randint(1, 3)
            else:
                pencils_removed = (pencils - 1) % 4
        else:
            pencils_removed = 1
        print(pencils_removed)
    else:
        while True:
            pencils_removed = input()
            if not pencils_removed.isdigit() or int(pencils_removed) not in [1, 2, 3]:
                print("Possible values: '1', '2' or '3'")
                continue
            if pencils - int(pencils_removed) < 0:
                print("Too many pencils were taken")
                continue
            break

    pencils = pencils - int(pencils_removed)
    idx = (idx + 1) % 2

print(f"{players[idx]} won!")
