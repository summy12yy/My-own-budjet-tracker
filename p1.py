
from pyscript import when
from js import document

# Stores expenses while the page is open
expenses = []


# Display a message to the user
def show_message(text, message_type=""):
    message = document.querySelector("#message")
    message.textContent = text
    message.className = "message"

    if message_type:
        message.classList.add(message_type)


# Add an expense when the form is submitted
@when("submit", "#expense-form")
def add_expense(event):
    # Prevent the page from refreshing
    event.preventDefault()

    #to input what you want to input
    amount_text = document.querySelector("#amount").value
    category = document.querySelector("#category").value
    description = document.querySelector("#description").value.strip()

    # Check the fields
    if not amount_text or not category or not description:
        show_message("Please complete all fields.", "error")
        return
    #to input you amount 
    try:
        amount = float(amount_text)
    except ValueError:
        show_message("Please enter a valid amount.", "error")
        return

    if amount <= 0:
        show_message("Amount must be greater than zero.", "error")
        return

    # Create an expense record
    expense = {
        "amount": amount,
        "category": category,
        "description": description
    }

    # Store the expense
    expenses.append(expense)

    # Refresh the website information
    update_dashboard()

    # Clear the form
    document.querySelector("#expense-form").reset()

    show_message("Expense added successfully!", "success")


# Update the dashboard totals and transaction table
def update_dashboard():
    total = sum(expense["amount"] for expense in expenses)
    count = len(expenses)

    # Update total spending
    document.querySelector("#total").textContent = (
        f"₱{total:,.2f}"
    )

    # Update transaction count
    document.querySelector("#count").textContent = str(count)

    # Calculate average expense
    average = total / count if count > 0 else 0

    document.querySelector("#average").textContent = (
        f"₱{average:,.2f}"
    )

    # Update record label
    document.querySelector("#record-label").textContent = (
        f"{count} record{'s' if count != 1 else ''}"
    )

    # Update transaction table
    expense_list = document.querySelector("#expense-list")
    expense_list.textContent = ""

    if not expenses:
        row = document.createElement("tr")
        cell = document.createElement("td")

        cell.colSpan = 3
        cell.className = "empty-state"
        cell.textContent = "No expenses recorded yet."

        row.appendChild(cell)
        expense_list.appendChild(row)
        return

    # Display newest expenses first in what you input 
    for expense in reversed(expenses):
        row = document.createElement("tr")

        description_cell = document.createElement("td")
        description_cell.textContent = expense["description"]

        category_cell = document.createElement("td")
        category_tag = document.createElement("span")
        category_tag.className = "category-tag"
        category_tag.textContent = expense["category"]
        category_cell.appendChild(category_tag)

        amount_cell = document.createElement("td")
        amount_cell.textContent = f"₱{expense['amount']:,.2f}"

        row.appendChild(description_cell)
        row.appendChild(category_cell)
        row.appendChild(amount_cell)

        expense_list.appendChild(row)


# Initial dashboard display
update_dashboard()
    