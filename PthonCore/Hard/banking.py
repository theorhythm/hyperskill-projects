# Write your code here
import random
import sys
import sqlite3

cards_dict = {}


def gen_card():
    global conn, cur
    number = '400000'
    for _ in range(9):
        number += str(random.randint(0, 9))
    tmp_list = [int(number[i]) if (i % 2) else int(number[i])*2 for i in range(15)]
    digit_list = [x - 9 if x > 9 else x for x in tmp_list]
    tmp_digit = sum(digit_list) % 10
    last_digit = 0 if tmp_digit == 0 else 10 - tmp_digit
    number += str(last_digit)
    p = ''
    for _ in range(4):
        p += str(random.randint(0, 9))
    cur.execute(f"insert into card (number, pin)\n"
                f"values ({number}, {p})\n")
    conn.commit()
    print(f"Your card has been created\nYour card number:\n{number}\nYour card PIN:\n{p}\n")


def check_info(number, p):
    global conn, cur
    cur.execute("select * from card;")
    res = cur.fetchall()
    if res:
        for row in res:
            if row[1] == number and row[2] == p:
                print("You have successfully logged in!")
                return row[0]
    print("Wrong card number or PIN!")
    return False


def login(card_id):
    global conn, cur
    print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
    sel = input()
    if sel == '0':
        print('bye!')
        conn.close()
        sys.exit()
    elif sel == '1':
        balance = cur.execute(f"select balance from card where id={card_id}").fetchone()
        print("Balance:", balance[0])
    elif sel == '2':
        print("Enter income:")
        income = int(input())
        cur.execute(f"update card set balance = balance + {income} where id={card_id}")
        conn.commit()
        print("Income was added!")
    elif sel == '3':
        print("Transfer\nEnter card number:")
        dest_num = input()
        if check_luhn(dest_num):
            print("Probably you made a mistake in the card number. Please try again!")
            return False
        transfer(dest_num, card_id)
    elif sel == '4':
        cur.execute(f"delete from card where id={card_id}")
        conn.commit()
        print('The account has been closed!')
        return True
    elif sel == '5':
        print("You have successfully logged out!")
        return True
    return False


def transfer(number, own_id):
    cur.execute(f"select * from card where number = {number}")
    res = cur.fetchone()
    if not res:
        print("Such a card does not exist.")
        return

    print("Enter how much money you want to transfer:")
    money = input()
    balance = cur.execute(f"select balance from card where id={own_id}").fetchone()
    if int(money) > int(balance[0]):
        print("Not enough money!")
        return

    cur.execute(f"update card set balance = balance + {money} where id={res[0]}")
    cur.execute(f"update card set balance = balance - {money} where id={own_id}")
    conn.commit()
    print("Success!")


def check_luhn(number):
    if len(number) != 16:
        return True
    last_digit = int(number[-1])
    tmp_list = [int(number[i]) if (i % 2) else int(number[i])*2 for i in range(15)]
    digit_list = [x - 9 if x > 9 else x for x in tmp_list]
    total = sum(digit_list) + last_digit
    return total % 10


conn = sqlite3.connect("card.s3db")
cur = conn.cursor()
if not cur.execute("SELECT name FROM sqlite_master").fetchone():
    cur.execute("create table card("
                "id integer primary key AUTOINCREMENT, "
                "number text, "
                "pin text, "
                "balance integer default 0"
                ");")
    conn.commit()

while True:
    print("1. Create an account\n2. Log into account\n0. Exit")
    selection = input()
    if selection == '0':
        print('bye!')
        conn.close()
        sys.exit()
    elif selection == '1':
        gen_card()
    elif selection == '2':
        print("Enter your card number:")
        card_num = input()
        print("Enter your PIN:")
        pin = input()
        own_id = check_info(card_num, pin)
        if own_id:
            while True:
                if login(own_id):
                    break
