from collections import defaultdict
from random import randint

print("""Please give AI some data to learn...
The current data length is 0, 100 symbols left""")

total_num = ""
while True:
    print('Print a random string containing 0 or 1:')
    number = input()
    valid_num = ""
    required = 100
    for v in number:
        if v in ['0', '1']:
            valid_num += v

    total_num += valid_num
    cnt = len(total_num)
    if cnt < 100:
        print("Current data length is {}, {} symbols left".format(cnt, 100 - cnt))
    else:
        break

print("Final data string:")
print(total_num)
case_list = ['000', '001', '010', '011', '100', '101', '110', '111']
case_dict_0 = defaultdict(int)
case_dict_1 = defaultdict(int)
for i in range(len(total_num) - 3):
    if total_num[i + 3] == '0':
        case_dict_0[total_num[i:i + 3]] += 1
    else:
        case_dict_1[total_num[i:i + 3]] += 1

print("""You have $1000. Every time the system successfully predicts your next press, you lose $1.
Otherwise, you earn $1. Print "enough" to leave the game. Let's go!""")
balance = 1000

while True:
    print("Print a random string containing 0 or 1:")
    test_num = input()
    if test_num == "enough":
        print("Game over!")
        break
    valid_num = ""
    for v in test_num:
        if v in ['0', '1']:
            valid_num += v
    if len(valid_num) <= 3:
        continue

    predict: str = str(randint(0, 1)) + str(randint(0, 1)) + str(randint(0, 1))
    for i in range(len(test_num) - 3):
        if case_dict_0[test_num[i:i + 3]] > case_dict_1[test_num[i:i + 3]]:
            predict += '0'
        elif case_dict_0[test_num[i:i + 3]] < case_dict_1[test_num[i:i + 3]]:
            predict += '1'
        else:
            predict += str(randint(0, 1))

    correct = 0
    total = len(test_num) - 3
    for i in range(total):
        if test_num[i+3] == predict[i+3]:
            correct += 1
    rate = round(correct * 100 / (len(test_num) - 3), 2)
    balance = balance - correct + (total - correct)
    print("prediction:")
    print(predict)
    print(f"Computer guessed right {correct} out of {total} symbols ({rate} %)")
    print(f"Your balance is now ${balance}")


# for v in case_list:
#     print("{}: {},{}".format(v, case_dict_0[v], case_dict_1[v]))
