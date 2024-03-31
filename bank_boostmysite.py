import os
import pickle
import pathlib
import time
from plyer import notification


class Account:
    def __init__(self, acc_no, name, acc_type, deposit, pin):
        self.acc_no = acc_no
        self.name = name
        self.acc_type = acc_type
        self.deposit = deposit
        self.pin = pin


def load_accounts():
    file_path = "accounts.data"
    if pathlib.Path(file_path).exists():  # opens a file in binary mode
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    return []


def save_accounts(accounts):
    with open("accounts.data", 'wb') as file:
        pickle.dump(accounts, file)


def create_account():
    acc_no = int(input("Enter account number: "))
    name = input("Enter name: ")
    acc_type = input("Enter account type: ")
    deposit = float(input("Enter initial deposit: "))
    pin = input("Enter PIN: ")
    return Account(acc_no, name, acc_type, deposit, pin)


def add_deposit_withdrawal(accounts, num, amount, deposit=True):
    for account in accounts:
        if account.acc_no == num:
            if deposit:
                account.deposit += amount
            else:
                if account.deposit >= amount:
                    account.deposit -= amount
                else:
                    print("Insufficient funds.")
            return True
    print("Account not found.")
    return False


def view_account_users(accounts):
    if not accounts:
        print("No records to display")
    else:
        for account in accounts:
            print(account.acc_no, account.name, account.acc_type, account.deposit, account.pin)


def change_pin_number(accounts, num, old_pin, new_pin):
    for account in accounts:
        if account.acc_no == num:
            if account.pin == old_pin:  # Check if the old pin matches
                account.pin = new_pin  # Update the pin
                save_accounts(accounts)  # Save the updated account list
                print("PIN changed successfully.")
                return
            else:
                print("Incorrect old PIN. PIN change failed.")
                return
    print("Account not found.")


def balance_enquiry(accounts, num):
    for account in accounts:
        if account.acc_no == num:
            deposit = account.deposit
            print(deposit)


def close_account(accounts, num):
    for account in accounts:
        if account.acc_no == num:
            accounts.remove(account)
            save_accounts(accounts)
            notification.notify(
                title="Welcome To the bank",
                message="The account is closed. Thank you for your trust.",
                timeout=3
            )
            return
    print("Account not found.")


def main():
    accounts = load_accounts()
    result = ''
    while result != '8':
        print("Welcome to BANK..")
        print("======================")
        print("1. Add Account")
        print("2. Add Deposit")
        print("3. Withdraw Amount")
        print("4. Change PIN")
        print("5. Balance Enquiry")
        print("6. View All Users")
        print("7. Close the account")
        print("8. EXIT")

        result = input("Enter your choice: ")
        if result == '1':
            accounts.append(create_account())
            save_accounts(accounts)
        elif result in {'2', '3'}:
            num = int(input("Enter the account number: "))
            amount = float(input("Enter amount: "))
            add_deposit_withdrawal(accounts, num, amount, result == '2')
            save_accounts(accounts)
        elif result == '4':
            num = int(input("Enter the account number: "))
            old_pin = int(input("Enter your current pin number:"))
            new_pin = int(input("Enter the new pin number:"))
            change_pin_number(accounts, num, old_pin, new_pin)
            save_accounts(accounts)
        elif result == '5':
            num = int(input("Enter the account number: "))
            balance_enquiry(accounts, num)
        elif result == '6':
            view_account_users(accounts)
        elif result == '7':
            num = int(input("Enter the account number: "))
            close_account(accounts, num)


if __name__ == "__main__":
    main()
