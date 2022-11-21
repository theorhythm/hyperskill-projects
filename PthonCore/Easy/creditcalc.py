# loan_principal = 'Loan principal: 1000'
# final_output = 'The loan has been repaid!'
# first_month = 'Month 1: repaid 250'
# second_month = 'Month 2: repaid 250'
# third_month = 'Month 3: repaid 500'
#
# # write your code here
# print(loan_principal)
# print(first_month)
# print(second_month)
# print(third_month)
# print(final_output)

from math import ceil, log
import argparse
import sys

parser = argparse.ArgumentParser(description="loan calculator")
parser.add_argument("--type")
parser.add_argument("--payment", type=int)
parser.add_argument("--principal", type=int)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float)

args = parser.parse_args()
flag_input = False
if args.type not in ["annuity", "diff"]:
    flag_input = True
elif args.type == "diff" and args.payment:
    flag_input = True
elif not args.interest:
    flag_input = True
elif bool(args.type) + bool(args.payment) + bool(args.principal) + bool(args.periods) < 3:
    flag_input = True
elif (args.payment and args.payment < 0) or (args.principal and args.principal < 0) \
        or (args.periods and args.periods < 0) or (args.interest < 0):
    flag_input = True

if flag_input:
    print("Incorrect parameters")
    sys.exit()

if not args.periods:
    i = args.interest / 12 / 100
    n = ceil(log(args.payment / (args.payment - i * args.principal), 1 + i))
    args.periods = n
    if n == 1:
        print("It will take 1 month to repay the loan")
    elif n < 12:
        print(f"It will take {n} months to repay the loan")
    elif n == 12:
        print("It will take 1 year to repay this loan!")
    elif n % 12 == 0:
        print("It will take {} years to repay this loan!".format(int(n / 12)))
    else:
        print("It will take {} years and {} months to repay this loan!".format(int(n / 12), n % 12))
elif args.type == "annuity" and not args.payment:
    i = args.interest / 12 / 100
    payment = args.principal * i * (1 + i)**args.periods / ((1 + i)**args.periods - 1)
    args.payment = ceil(payment)
    print(f"Your annuity payment = {args.payment}!")

    # if payment.is_integer():
    #     print(f"Your annuity payment = {payment}!")
    # else:
    #     payment_normal = ceil(payment)
    #     payment_last = args.principal - (args.periods - 1) * payment_normal
    #     print(f"Your annuity payment = {payment_normal} and the last payment = {payment_last}!")
elif args.type == "diff" and not args.payment:
    i = args.interest / 12 / 100
    P = args.principal
    n = args.periods
    m = 1
    total = 0
    for month in range(n):
        D = ceil(P/n + i * (P - P * (m - 1) / n))
        print("Month {}: payment is {}".format(m, D))
        m += 1
        total += D
    overpayment = total - P
    print("\nOverpayment = {}".format(overpayment))
    sys.exit()
elif not args.principal:
    i = args.interest / 12 / 100
    principal = int(args.payment / (i * (1 + i)**args.periods / ((1 + i)**args.periods - 1)))
    args.principal = principal
    print("Your loan principal = {}!".format(principal))

overpayment = args.periods * args.payment - args.principal
print(f"Overpayment = {overpayment}")


# print("""What do you want to calculate?
# type "n" for number of monthly payments,
# type "a" for annuity monthly payment amount,
# type "p" for loan principal:""")
# select = input()
# if select == 'n':
#     print("Enter the loan principal:")
#     principal = int(input())
#     print("Enter the monthly payment:")
#     payment = int(input())
#     print("Enter the loan interest:")
#     interest = float(input())
#     i = interest / 12 / 100
#     n = ceil(log(payment / (payment - i * principal), 1 + i))
#     if n == 1:
#         print("It will take 1 month to repay the loan")
#     elif n < 12:
#         print(f"It will take {n} months to repay the loan")
#     elif n == 12:
#         print("It will take 1 year to repay this loan!")
#     elif n % 12 == 0:
#         print("It will take {} years to repay this loan!".format(int(n / 12)))
#     else:
#         print("It will take {} years and {} months to repay this loan!".format(int(n / 12), n % 12))
#
# elif select == 'a':
#     print("Enter the loan principal:")
#     principal = int(input())
#     print("Enter the number of periods:")
#     periods = int(input())
#     print("Enter the loan interest:")
#     interest = float(input())
#     i = interest / 12 / 100
#     payment = principal * i * (1 + i)**periods / ((1 + i)**periods - 1)
#     if payment.is_integer():
#         print(f"Your monthly payment = {payment}!")
#     else:
#         payment_normal = ceil(payment)
#         payment_last = principal - (periods - 1) * payment_normal
#         print(f"Your monthly payment = {payment_normal} and the last payment = {payment_last}!")
#
# elif select == 'p':
#     print("Enter the annuity payment:")
#     payment = float(input())
#     print("Enter the number of periods:")
#     periods = int(input())
#     print("Enter the loan interest:")
#     interest = float(input())
#     i = interest / 12 / 100
#     principal = payment / (i * (1 + i)**periods / ((1 + i)**periods - 1))
#     print("Your loan principal = {}!".format(round(principal)))
