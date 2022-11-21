# write your code here
import random

lv1 = "simple operations with numbers 2-9"
lv2 = "integral squares 11-29"
desc = ''
mark = 0
i = 0
lv = ''
while True:
    print("Which level do you want? Enter a number:")
    lv = input()
    if lv not in ['1', '2']:
        print("Incorrect format.")
        continue
    break

if lv == '1':
    desc = "simple operations with numbers 2-9"
    for _ in range(5):
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        sign = random.choice(["+", "-", "*"])
        print(f"{a} {sign} {b}")

        ans = 0
        if sign == "+":
            ans = a + b
        elif sign == "-":
            ans = a - b
        elif sign == "*":
            ans = a * b

        while True:
            test = input()
            try:
                if int(test) == ans:
                    print("Right!")
                    mark += 1
                else:
                    print("Wrong!")
                break
            except ValueError:
                print("Incorrect format")
else:
    desc = "integral squares 11-29"
    for _ in range(5):
        a = random.randint(11, 29)
        print(a)
        ans = a**2
        while True:
            test = input()
            try:
                if int(test) == ans:
                    print("Right!")
                    mark += 1
                else:
                    print("Wrong!")
                break
            except ValueError:
                print("Incorrect format")

print(f"Your mark is {mark}/5. Would you like to save the result? Enter yes or no.")
ans = input()
if ans in ['yes', 'YES', 'y', 'Yes']:
    print("What's your name?")
    name = input()
    file = open("results.txt", 'a')
    file.write(f"{name}: {mark}/5 in level {lv} ({desc})\n")
    file.close()
    print('The results are saved in "results.txt".')
