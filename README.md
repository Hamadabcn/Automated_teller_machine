# Automated Teller Machine (ATM)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Functionality](#functionality)
  - [GUI Class](#gui-class)
- [How It Works](#how-it-works)
- [License](#license)

## Overview
The Automated Teller Machine (ATM) is a Python-based GUI application that simulates the basic functionalities of a cash machine. Users can perform transactions such as withdrawing and depositing money, checking their balance, and managing their PIN securely.

## Features
- Secure PIN entry with hashing
- Balance checking
- Withdrawal and deposit transactions
- Transaction history tracking
- Ability to change PIN
- User-friendly graphical interface

## Installation
To run this project, ensure you have Python installed on your system. You will also need the Tkinter library, which is included with Python installations. To set it up, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Hamadabcn/Automated_teller_machine.git

2. Navigate to the project directory:
   ```bash
   cd Automated_teller_machine

3. Run the application:
   ```bash
   python gui.py

## Usage
The default PIN number is `1234`. Upon running the application, you will be prompted to enter your 4-digit PIN. After successful authentication, you can perform various transactions such as withdrawing money, depositing funds, and checking your balance.


## Functionality

### Cash Machine Class
The `CashMachine` class implements the core functionalities of the ATM:
- **PIN Management**: Load, save, and verify the user's PIN.
- **Transaction Handling**: Methods to deposit and withdraw money.
- **Balance Checking**: Retrieve the current account balance.
- **Transaction History**: Keep track of all transactions performed.
  
### GUI Class
The `CashMachineGUI` class provides a user interface using Tkinter:
- **Widgets**: Includes buttons for withdrawals, deposits, PIN changes, and viewing transaction history.
- **User Interaction**: Prompts for input and displays messages.
- **State Management**: Loads and saves the machine's state to a JSON file to retain information between sessions.
  
## How It Works
When the application starts, it checks for an existing PIN in pin.txt or sets a default PIN if none is found. Users are prompted to enter their PIN. After three failed attempts, the application will exit. Once authenticated, users can access different functionalities through the GUI, which dynamically updates the balance and transaction history.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
