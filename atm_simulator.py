"""Simple ATM machine simulation with a text-based console interface.

This script lets a user:
1) Check balance
2) Withdraw money
3) Deposit money
4) View transaction history with timestamps

The design uses a class to keep account state and behavior organized.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    """Represents one account transaction in the ATM history."""

    timestamp: datetime
    kind: str
    amount: float
    balance_after: float


class ATMAccount:
    """Basic ATM account with balance tracking and transaction history."""

    def __init__(self, starting_balance: float = 0.0) -> None:
        self.balance = starting_balance
        self.transactions: list[Transaction] = []

    def check_balance(self) -> float:
        """Return the current account balance."""
        return self.balance

    def deposit(self, amount: float) -> bool:
        """Deposit money if amount is valid; return True if successful."""
        if amount <= 0:
            return False

        self.balance += amount
        self.transactions.append(
            Transaction(
                timestamp=datetime.now(),
                kind="DEPOSIT",
                amount=amount,
                balance_after=self.balance,
            )
        )
        return True

    def withdraw(self, amount: float) -> bool:
        """Withdraw money if amount is valid and no overdraft occurs."""
        if amount <= 0:
            return False

        # Prevent overdraft by rejecting amounts greater than current balance.
        if amount > self.balance:
            return False

        self.balance -= amount
        self.transactions.append(
            Transaction(
                timestamp=datetime.now(),
                kind="WITHDRAWAL",
                amount=amount,
                balance_after=self.balance,
            )
        )
        return True

    def get_history(self) -> list[Transaction]:
        """Return the full transaction list."""
        return self.transactions


def read_menu_choice() -> str:
    """Prompt user for menu selection and return a valid option."""
    valid_choices = {"1", "2", "3", "4", "5"}

    while True:
        print("\n=== ATM MENU ===")
        print("1) Check Balance")
        print("2) Withdraw Cash")
        print("3) Deposit Money")
        print("4) View Transaction History")
        print("5) Exit")

        choice = input("Enter your choice (1-5): ").strip()
        if choice in valid_choices:
            return choice

        print("Invalid selection. Please enter a number from 1 to 5.")


def read_positive_amount(prompt: str) -> float:
    """Prompt user repeatedly until a valid positive currency amount is entered."""
    while True:
        raw = input(prompt).strip()

        try:
            amount = float(raw)
        except ValueError:
            print("Invalid number. Please enter a numeric amount, e.g. 50 or 20.75.")
            continue

        if amount <= 0:
            print("Amount must be greater than 0.")
            continue

        # Round to 2 decimals to simulate currency handling.
        return round(amount, 2)


def format_currency(amount: float) -> str:
    """Format a float as USD-like currency string."""
    return f"${amount:,.2f}"


def show_transaction_history(account: ATMAccount) -> None:
    """Print all past transactions in a readable table-like format."""
    history = account.get_history()

    if not history:
        print("\nNo transactions yet.")
        return

    print("\n=== TRANSACTION HISTORY ===")
    for index, txn in enumerate(history, start=1):
        ts = txn.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"{index:>3}. {ts} | {txn.kind:<10} | "
            f"Amount: {format_currency(txn.amount):>10} | "
            f"Balance after: {format_currency(txn.balance_after):>10}"
        )


def run_atm() -> None:
    """Main loop for ATM simulation with user-friendly prompts and validation."""
    print("Welcome to the Python ATM Simulator!")

    # You can change this starting balance to test different scenarios.
    account = ATMAccount(starting_balance=1000.00)

    while True:
        choice = read_menu_choice()

        if choice == "1":
            print(f"\nCurrent balance: {format_currency(account.check_balance())}")

        elif choice == "2":
            amount = read_positive_amount("Enter amount to withdraw: $")

            if account.withdraw(amount):
                print(
                    f"Withdrawal successful. New balance: "
                    f"{format_currency(account.check_balance())}"
                )
            else:
                print(
                    "Withdrawal failed. Check that the amount is valid and "
                    "does not exceed your available balance."
                )

        elif choice == "3":
            amount = read_positive_amount("Enter amount to deposit: $")

            if account.deposit(amount):
                print(
                    f"Deposit successful. New balance: "
                    f"{format_currency(account.check_balance())}"
                )
            else:
                # This is unlikely due to input validation, but kept for safety.
                print("Deposit failed. Please try again with a valid amount.")

        elif choice == "4":
            show_transaction_history(account)

        elif choice == "5":
            print("\nThank you for using the ATM. Goodbye!")
            break


if __name__ == "__main__":
    run_atm()
