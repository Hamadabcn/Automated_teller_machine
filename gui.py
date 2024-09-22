# default pin number: 1234

import hashlib
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
import locale
import json


# Class representing the Cash Machine functionality
class CashMachine:
    """A class to represent the cash machine functionality."""

    def __init__(self):
        """Initialize the CashMachine with a balance, transaction history, and PIN."""
        self.balance = 0
        self.transaction_history = []
        self.pin = self.load_pin()

    def hash_pin(self, pin):
        """Hash the given PIN using SHA-256.

        Args:
            pin (str): The PIN to be hashed.

        Returns:
            str: The hashed PIN.
        """
        return hashlib.sha256(pin.encode()).hexdigest()

    def load_pin(self):
        """Load the PIN from a file or create a default one if the file doesn't exist.

        Returns:
            str: The loaded or default hashed PIN.
        """
        try:
            with open("pin.txt", "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            default_pin = self.hash_pin("1234")
            self.save_pin(default_pin)
            return default_pin

    def save_pin(self, pin):
        """Save the hashed PIN to a file.

        Args:
            pin (str): The hashed PIN to save.
        """
        with open("pin.txt", "w") as f:
            f.write(pin)

    def verify_pin(self, pin):
        """Verify if the given PIN matches the stored hashed PIN.

        Args:
            pin (str): The PIN to verify.

        Returns:
            bool: True if the PIN is correct, False otherwise.
        """
        return self.hash_pin(pin) == self.pin

    def check_balance(self):
        """Check the current balance.

        Returns:
            str: A message with the current balance formatted as currency.
        """
        return f"Your current balance: {self.format_currency(self.balance)}"

    def withdraw_money(self, amount):
        """Withdraw a specified amount from the balance.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            str: A message indicating the result of the withdrawal.
        """
        if amount <= 0:
            return "Amount must be positive."
        if self.balance < amount:
            return "Insufficient funds. Unable to withdraw."
        transaction_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.balance -= amount
        result = (f"Withdrawal: -{self.format_currency(amount)}. New balance: "
                  f"{self.format_currency(self.balance)}. Date: {transaction_time}\n")
        self.transaction_history.append(result)
        return result

    def deposit_money(self, amount):
        """Deposit a specified amount into the balance.

        Args:
            amount (float): The amount to deposit.

        Returns:
            str: A message indicating the result of the deposit.
        """
        if amount <= 0:
            return "Amount must be positive."
        transaction_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.balance += amount
        result = (f"Deposit: +{self.format_currency(amount)}. New balance: "
                  f"{self.format_currency(self.balance)}. Date: {transaction_time}\n")
        self.transaction_history.append(result)
        return result

    def format_currency(self, amount):
        """Format an amount as currency.

        Args:
            amount (float): The amount to format.

        Returns:
            str: The formatted currency string.
        """
        return locale.currency(amount, grouping=True)


class GUIConstants:
    """A class to store constant values for the GUI."""
    BACKGROUND_COLOR = "#B2DFDB"  # Soft teal
    BUTTON_COLOR = "#00796B"      # Dark teal for buttons
    ERROR_COLOR = "#D32F2F"       # Error red
    TEXT_AREA_COLOR = "#B2EBF2"   # Light aqua for text area
    TEXT_COLOR = "#004D40"        # Darker teal for text
    FONT_STYLE = ("Helvetica", 14)


class CashMachineGUI:
    """A class to represent the graphical user interface for the cash machine."""
    MAX_PIN_ATTEMPTS = 3

    def __init__(self, root):
        """Initialize the CashMachineGUI with the main application window.

        Args:
            root (tk.Tk): The root window of the GUI.
        """
        self.cash_machine = CashMachine()
        self.pin_attempts = 0
        self.verify_pin()
        self.root = root
        self.root.title("ATM GUI")
        self.root.geometry("700x800")
        self.root.configure(bg=GUIConstants.BACKGROUND_COLOR)
        self.create_widgets()
        self.load_state()

    def verify_pin(self):
        """Prompt the user to enter their PIN and verify it."""
        while self.pin_attempts < self.MAX_PIN_ATTEMPTS:
            pin = simpledialog.askstring("PIN", "Enter your 4-digit PIN:")
            if self.cash_machine.verify_pin(pin):
                break
            else:
                self.pin_attempts += 1
                messagebox.showerror("Error", f"Invalid PIN. Attempts left: "
                                              f"{self.MAX_PIN_ATTEMPTS - self.pin_attempts}")
        else:
            messagebox.showerror("Error", "Too many failed attempts. Exiting.")
            self.root.quit()

    def create_widgets(self):
        """Create and place all GUI widgets in the application window."""
        title_label = tk.Label(self.root, text="ATM", font=("Helvetica", 28, "bold"),
                               bg=GUIConstants.BUTTON_COLOR, fg=GUIConstants.TEXT_COLOR)
        title_label.pack(pady=10)

        self.balance_label = tk.Label(self.root, text=self.cash_machine.check_balance(),
                                      font=("Helvetica", 18), bg=GUIConstants.BACKGROUND_COLOR,
                                      fg=GUIConstants.TEXT_COLOR)
        self.balance_label.pack(pady=10)

        menu_frame = tk.Frame(self.root, bg=GUIConstants.BACKGROUND_COLOR)
        menu_frame.pack(pady=20)

        self.withdraw_button = tk.Button(menu_frame, text="Withdraw Money", command=self.withdraw_money,
                                         font=GUIConstants.FONT_STYLE, bg=GUIConstants.BUTTON_COLOR,
                                         fg=GUIConstants.TEXT_COLOR)
        self.withdraw_button.grid(row=0, column=0, padx=10)
        self.withdraw_button.bind("<Enter>", lambda e: self.withdraw_button.config(bg="#009688"))
        self.withdraw_button.bind("<Leave>", lambda e: self.withdraw_button.config(bg=GUIConstants.BUTTON_COLOR))

        self.deposit_button = tk.Button(menu_frame, text="Deposit Money", command=self.deposit_money,
                                        font=GUIConstants.FONT_STYLE, bg=GUIConstants.BUTTON_COLOR,
                                        fg=GUIConstants.TEXT_COLOR)
        self.deposit_button.grid(row=0, column=1, padx=10)
        self.deposit_button.bind("<Enter>", lambda e: self.deposit_button.config(bg="#009688"))
        self.deposit_button.bind("<Leave>", lambda e: self.deposit_button.config(bg=GUIConstants.BUTTON_COLOR))

        change_pin_button = tk.Button(menu_frame, text="Change PIN", command=self.change_pin,
                                      font=GUIConstants.FONT_STYLE, bg=GUIConstants.BUTTON_COLOR,
                                      fg=GUIConstants.TEXT_COLOR)
        change_pin_button.grid(row=1, column=0, padx=10)
        change_pin_button.bind("<Enter>", lambda e: change_pin_button.config(bg="#009688"))
        change_pin_button.bind("<Leave>", lambda e: change_pin_button.config(bg=GUIConstants.BUTTON_COLOR))

        history_button = tk.Button(menu_frame, text="Show History", command=self.show_history,
                                   font=GUIConstants.FONT_STYLE, bg=GUIConstants.BUTTON_COLOR,
                                   fg=GUIConstants.TEXT_COLOR)
        history_button.grid(row=1, column=1, padx=10)
        history_button.bind("<Enter>", lambda e: history_button.config(bg="#009688"))
        history_button.bind("<Leave>", lambda e: history_button.config(bg=GUIConstants.BUTTON_COLOR))

        quit_button = tk.Button(self.root, text="Quit", command=self.quit_program,
                                bg=GUIConstants.ERROR_COLOR, fg=GUIConstants.TEXT_COLOR,
                                font=GUIConstants.FONT_STYLE)
        quit_button.pack()

        # Add hover effect
        quit_button.bind("<Enter>", lambda e: quit_button.config(bg="#D50000"))  # Change color on hover
        quit_button.bind("<Leave>", lambda e: quit_button.config(bg=GUIConstants.ERROR_COLOR))  # Revert color

        self.amount_entry = tk.Entry(menu_frame, font=GUIConstants.FONT_STYLE, width=20, justify="left", insertwidth=4)
        self.amount_entry.grid(row=2, column=0, pady=10)
        self.amount_entry.insert(0, "Enter amount...")  # Default informative text
        self.amount_entry.config(fg="lightgray")
        self.amount_entry.bind("<FocusIn>", self.clear_default_text)
        self.amount_entry.bind("<FocusOut>", self.set_default_text)  # Set default text back if empty
        self.amount_entry.bind("<KeyRelease>", self.check_amount)

        self.history_frame = tk.Frame(self.root, bg=GUIConstants.BACKGROUND_COLOR)
        self.history_frame.pack(pady=20)

        self.history_text = tk.Text(self.history_frame, height=20, width=70, wrap=tk.WORD,
                                    font=("Helvetica", 12), bg=GUIConstants.TEXT_AREA_COLOR,
                                    fg=GUIConstants.TEXT_COLOR)
        self.history_text.pack()

        self.processing_label = tk.Label(self.root, text="", bg=GUIConstants.BACKGROUND_COLOR,
                                         fg=GUIConstants.TEXT_COLOR)
        self.processing_label.pack(pady=10)

    def check_amount(self, event):
        """Check if the entered amount is valid."""
        try:
            value = float(self.amount_entry.get())
            if value < 0:
                self.amount_entry.config(fg=GUIConstants.ERROR_COLOR)
            else:
                self.amount_entry.config(fg=GUIConstants.TEXT_COLOR)
        except ValueError:
            self.amount_entry.config(fg=GUIConstants.ERROR_COLOR)

    def clear_default_text(self, event):
        """Clear default text in the amount entry field when focused."""
        if self.amount_entry.get() == "Enter amount...":
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.config(fg=GUIConstants.TEXT_COLOR)

    def set_default_text(self, event):
        """Set default text in the amount entry field if empty."""
        if not self.amount_entry.get():
            self.amount_entry.insert(0, "Enter amount...")
            self.amount_entry.config(fg="lightgray")

    def withdraw_money(self):
        """Handle the withdrawal of money."""
        amount = self.amount_entry.get()
        try:
            amount = float(amount)
            result = self.cash_machine.withdraw_money(amount)
            self.update_balance_label()
            self.history_text.insert(tk.END, result)
            self.amount_entry.delete(0, tk.END)
            self.processing_label.config(text="Withdrawal processed.")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")

    def deposit_money(self):
        """Handle the deposit of money."""
        amount = self.amount_entry.get()
        try:
            amount = float(amount)
            result = self.cash_machine.deposit_money(amount)
            self.update_balance_label()
            self.history_text.insert(tk.END, result)
            self.amount_entry.delete(0, tk.END)
            self.processing_label.config(text="Deposit processed.")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")

    def update_balance_label(self):
        """Update the balance label to reflect the current balance."""
        self.balance_label.config(text=self.cash_machine.check_balance())

    def show_history(self):
        """Display the transaction history in the text area."""
        self.history_text.delete(1.0, tk.END)  # Clear previous history
        for transaction in self.cash_machine.transaction_history:
            self.history_text.insert(tk.END, transaction)
        self.history_text.see(tk.END)  # Scroll to the end

    def change_pin(self):
        """Change the current PIN after verifying the old PIN."""
        old_pin = simpledialog.askstring("Change PIN", "Enter your old PIN:")
        if self.cash_machine.verify_pin(old_pin):
            new_pin = simpledialog.askstring("Change PIN", "Enter your new 4-digit PIN:")
            if new_pin and len(new_pin) == 4:
                self.cash_machine.save_pin(self.cash_machine.hash_pin(new_pin))
                messagebox.showinfo("Success", "PIN changed successfully.")
            else:
                messagebox.showerror("Error", "New PIN must be 4 digits.")
        else:
            messagebox.showerror("Error", "Old PIN is incorrect.")

    def quit_program(self):
        """Quit the program."""
        self.save_state()
        self.root.quit()

    def save_state(self):
        """Save the current state of the cash machine (e.g., balance, transaction history) to a JSON file."""
        state = {
            "balance": self.cash_machine.balance,
            "transaction_history": self.cash_machine.transaction_history,
        }
        with open("cash_machine_state.json", "w") as f:
            json.dump(state, f)

    def load_state(self):
        """Load the saved state of the cash machine from a JSON file."""
        try:
            with open("cash_machine_state.json", "r") as f:
                state = json.load(f)
                self.cash_machine.balance = state.get("balance", 0)
                self.cash_machine.transaction_history = state.get("transaction_history", [])
                self.update_balance_label()
        except FileNotFoundError:
            pass  # No saved state to load


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    root = tk.Tk()
    app = CashMachineGUI(root)
    root.mainloop()
