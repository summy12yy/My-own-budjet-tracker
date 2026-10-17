
from pyscript import when
from js import document, localStorage
import json


# Stores expenses and allowance
expenses = []
allowance = 0


# Display a message to the user
def show_message(text, message_type=""):
    message = document.querySelector("#message")
    message.textContent = text
    message.className = "message"

    if message_type:
        message.classList.add(message_type)


# Save allowance and expenses in browser storage
def save_data():
    data = {
        "allowance": allowance,
        "expenses": expenses
    }

    localStorage.setItem(
        "expenseAnalyzerData",
        json.dumps(data)
    )


# Load saved allowance and expenses
def load_data():
    global allowance, expenses

    saved_data = localStorage.getItem("expenseAnalyzerData")

    if saved_data:
        try:
            data = json.loads(saved_data)

            allowance = float(data.get("allowance", 0))
            expenses = data.get("expenses", [])

        except (ValueError, TypeError):
            allowance = 0
            expenses = []


# Add an expense when the form is submitted
@when("submit", "#expense-form")
def add_expense(event):
    
    # Prevent the page from refreshing
    event.preventDefault()

    # Read the user's input
    amount_text = document.querySelector("#amount").value
    category = document.querySelector("#category").value
    description = document.querySelector(
        "#description"
    ).value.strip()

    # Check whether all fields are completed
    if not amount_text or not category or not description:
        show_message("Please complete all fields.", "error")
        return

    # Convert the amount into a number
    try:
        amount = float(amount_text)
    except ValueError:
        show_message("Please enter a valid amount.", "error")
        return

    # Prevent zero or negative expenses
    if amount <= 0:
        show_message(
            "Amount must be greater than zero.",
            "error"
        )
        return

    # Create an expense record
    expense = {
        "amount": amount,
        "category": category,
        "description": description
    }

    # Add the expense to the list
    expenses.append(expense)

    # Save the updated information
    save_data()

    # Update the dashboard
    update_dashboard()

    # Clear the form
    document.querySelector("#expense-form").reset()

    # Display a message
    total = sum(item["amount"] for item in expenses)

    if total > allowance:
        show_message(
            "Expense added, but you have exceeded your allowance!",
            "error"
        )
    else:
        show_message(
            "Expense added successfully!",
            "success"
        )


# Set or update the allowance
@when("submit", "#allowance-form")
def set_allowance(event):
    global allowance

    # Prevent the page from refreshing
    event.preventDefault()

    # Read the allowance input
    amount_text = document.querySelector(
        "#allowance-input"
    ).value

    # Convert the input into a number
    try:
        new_allowance = float(amount_text)
    except ValueError:
        show_message(
            "Please enter a valid allowance.",
            "error"
        )
        return

    # Prevent zero or negative allowance
    if new_allowance <= 0:
        show_message(
            "Allowance must be greater than zero.",
            "error"
        )
        return

    # Update and save the allowance
    allowance = new_allowance
    save_data()

    # Refresh dashboard information
    update_dashboard()

    show_message(
        "Allowance set successfully!",
        "success"
    )


# Update dashboard totals and transaction table
def update_dashboard():
    # Calculate total spending and number of expenses
    total = sum(expense["amount"] for expense in expenses)
    count = len(expenses)

    # Calculate the remaining allowance
    balance = allowance - total

    # Display allowance
    document.querySelector(
        "#allowance-total"
    ).textContent = f"₱{allowance:,.2f}"

    # Display remaining balance
    document.querySelector(
        "#balance"
    ).textContent = f"₱{balance:,.2f}"

    # Display total spending
    document.querySelector(
        "#total"
    ).textContent = f"₱{total:,.2f}"

    # Display the number of expenses
    document.querySelector("#count").textContent = str(count)

    # Calculate and display average expense
    average = total / count if count > 0 else 0

    document.querySelector(
        "#average"
    ).textContent = f"₱{average:,.2f}"

    # Update transaction count label
    document.querySelector(
        "#record-label"
    ).textContent = (
        f"{count} record{'s' if count != 1 else ''}"
    )

    # Clear the old transaction table
    expense_list = document.querySelector("#expense-list")
    expense_list.textContent = ""

    # Show a message if there are no expenses
    if not expenses:
        row = document.createElement("tr")
        cell = document.createElement("td")

        cell.colSpan = 3
        cell.className = "empty-state"
        cell.textContent = "No expenses recorded yet."

        row.appendChild(cell)
        expense_list.appendChild(row)
        return

    # Display newest expenses first
    for expense in reversed(expenses):
        row = document.createElement("tr")

        # Description column
        description_cell = document.createElement("td")
        description_cell.textContent = expense["description"]

        # Category column
        category_cell = document.createElement("td")
        category_tag = document.createElement("span")

        category_tag.className = "category-tag"
        category_tag.textContent = expense["category"]

        category_cell.appendChild(category_tag)

        # Amount column
        amount_cell = document.createElement("td")
        amount_cell.textContent = f"₱{expense['amount']:,.2f}"

        # Add columns to the row
        row.appendChild(description_cell)
        row.appendChild(category_cell)
        row.appendChild(amount_cell)

        # Add the row to the table
        expense_list.appendChild(row)


# Load saved data before displaying the dashboard
load_data()
update_dashboard()
