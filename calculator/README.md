# 🧮 Python CLI Calculator

A versatile **Command-Line Interface (CLI) calculator** written in Python.

It supports:
- **Classic Mode**: Step-by-step number + operation + number.
- **Pro Mode**: Full expression evaluation with memory, history, percentages, precision control, and chaining operations.

---

## 📦 Features

### Classic Mode
- Step-by-step input:
  1. Enter first number
  2. Enter operation (+, -, *, /)
  3. Enter second number
- Validates inputs (numbers and operations)
- Handles divide-by-zero gracefully

### Pro Mode
- **Full expressions** with parentheses & precedence:
  ```text
  2*(3+4) / 5
Power operator (^) is supported:

2^3 → 8
Percentage support:

200 + 10% → 220
50% * 80 → 40
## Memory keys:

:mem – Show memory (MR)

:mc – Clear memory

:m+ – Add last result to memory

:m- – Subtract last result from memory

## History & Undo:

:history – Show last 10 calculations

:undo – Remove the most recent result

Precision control:

:prec N – Set decimal precision (default: 28)

## Smart chaining:

After 18, typing * 2 → 36

Help command:

:help – Show all commands

## 🚀 How to Run
Make sure you have Python 3.8+ installed.

### Navigate to project root
cd path/to/project

### Run the calculator
python -m calculator.main
When prompted:

Choose 1 for Classic Mode

Choose 2 for Pro Mode

## 💻 Example Usage
### Classic Mode

[Classic Mode] Step-by-step calculator
Enter the first number: 12
Enter the operation (+, -, *, /): *
Enter the second number: 5
= 60

### Pro Mode
[Pro Mode] Expression calculator (type :help for commands)
>>> 2*(3+4)
= 14
>>> ^ 2
= 196
>>> 200 + 10%
= 220
>>> :m+
M+ done.
>>> :mem
MR = 220
>>> :history
1) 2*(3+4) = 14
2) 14 ^ 2 = 196
3) 200 + 10% = 220

## 📜 Commands (Pro Mode)
Command	Description
:help	Show all available commands
:history	Show last 10 calculations
:undo	Remove the most recent result
:mem	Show memory value
:mc	Clear memory
:m+	Add last result to memory
:m-	Subtract last result from memory
:prec N	Set decimal precision (default: 28)
:exit	Quit the calculator

## 🛠 Requirements
Python 3.8 or higher

No external dependencies (pure Python)

## 🧪 Tips & Notes
Use ^ for exponent in input; it’s automatically converted to **.

% can act as a percentage operator in two intuitive ways:

A + B%/A - B% adjusts A by B percent of A.

X% inside expressions becomes (X/100).

If you ever get stuck, type :help.

## 📄 License
This project is licensed under the MIT License – see the LICENSE file for details.