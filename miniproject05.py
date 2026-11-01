import datetime as dt
import random
import expense_utils as eu

from expense_utils import (
    validate_amount,
    get_month_expenses
)

from report_utils import generate_report, save_report


expenses = []


def generate_reference():
    while True:
        number = random.randint(100000, 999999)
        reference = f"EXP-{number}"

        existing_ids = [
            expense["reference"] for expense in expenses
        ]

        if reference not in existing_ids:
            return reference


def add_expense():

    print("\n------ ADD NEW EXPENSE ------")

    description = input("Enter description: ").strip()

    if not description:
        print("Description cannot be empty.")
        return

    category = input(
        "Enter category (Food/Travel/Study/Bills/Other): "
    ).strip()

    if not category:
        print("Category cannot be empty.")
        return

    while True:
        amount_input = input("Enter amount (Rs.): ").strip()

        if validate_amount(amount_input):
            amount = round(float(amount_input), 2)
            break

        print("Please enter a valid positive amount.")

    while True:
        date_input = input(
            "Enter date (YYYY-MM-DD, blank for today): "
        ).strip()

        if date_input == "":
            expense_date = dt.date.today()
            break

        try:
            expense_date = dt.datetime.strptime(
                date_input, "%Y-%m-%d"
            ).date()
            break

        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD.")

    reference = generate_reference()

    expense = {
        "reference": reference,
        "description": description,
        "category": category.title(),
        "amount": amount,
        "date": expense_date
    }

    expenses.append(expense)

    print("\nExpense added successfully!")
    print("Transaction Reference:", reference)


def show_all_expenses():

    print("\n------ ALL EXPENSES ------")

    if not expenses:
        print("No expenses have been recorded yet.")
        return

    from tabulate import tabulate

    headers = [
        "Reference ID",
        "Date",
        "Description",
        "Category",
        "Amount"
    ]

    rows = []

    for expense in expenses:
        rows.append([
            expense["reference"],
            expense["date"].strftime("%Y-%m-%d"),
            expense["description"],
            expense["category"],
            f"Rs. {expense['amount']:.2f}"
        ])

    print(tabulate(rows, headers=headers, tablefmt="grid"))


def show_monthly_report():

    today = dt.date.today()

    monthly_expenses = get_month_expenses(
        expenses,
        today.year,
        today.month
    )

    report = generate_report(
        monthly_expenses,
        today.year,
        today.month
    )

    print(report)

    choice = input(
        "\nDo you want to save this report? (y/n): "
    ).strip().lower()

    if choice == "y":
        save_report(report, today.year, today.month)


def show_summary():

    print("\n------ EXPENSE SUMMARY ------")

    if not expenses:
        print("No expenses available.")
        return

    total = eu.calculate_total(expenses)

    categories = eu.category_totals(expenses)

    print(f"Total Expenses: Rs. {total:.2f}")

    print("\nCategory-wise Expenses:")

    for category, amount in categories.items():
        print(f"{category}: Rs. {amount:.2f}")


def main():

    print("===================================")
    print("     PERSONAL EXPENSE TRACKER")
    print("===================================")

    while True:

        print("\n1. Add New Expense")
        print("2. View All Expenses")
        print("3. Generate Monthly Report")
        print("4. View Expense Summary")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            add_expense()

        elif choice == "2":
            show_all_expenses()

        elif choice == "3":
            show_monthly_report()

        elif choice == "4":
            show_summary()

        elif choice == "5":
            print("\nThank you for using Personal Expense Tracker!")
            break

        else:
            print("Invalid choice. Please select between 1 and 5.")


if __name__ == "__main__":
    main()