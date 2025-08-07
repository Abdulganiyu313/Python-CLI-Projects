# calculator/main.py
from __future__ import annotations
from decimal import Decimal, getcontext
import ast
import operator as op
import re

# =========================================
# 1) Your existing basic calculator (KEEP)
#    If you already have this function, use yours
# =========================================
def basic_calculator(num1: float, num2: float, operation: str) -> float:
    if operation == '+': return num1 + num2
    if operation == '-': return num1 - num2
    if operation == '*': return num1 * num2
    if operation == '/':
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        return num1 / num2
    raise ValueError("Unsupported operation")

# =========================================
# 2) Classic Mode (your current step-by-step UX)
# =========================================
OPERATIONS = {"+", "-", "*", "/"}

def get_number(prompt: str) -> float:
    while True:
        val = input(prompt).strip()
        try:
            return float(val)
        except ValueError:
            print("❌ Invalid number. Try again.")

def get_operation(prompt: str) -> str:
    while True:
        op_in = input(prompt).strip()
        if op_in in OPERATIONS:
            return op_in
        print(f"❌ Invalid operation. Choose from: {', '.join(OPERATIONS)}.")

def classic_mode():
    print("\n[Classic Mode] Step-by-step calculator")
    while True:
        num1 = get_number("Enter the first number: ")
        operation = get_operation("Enter the operation (+, -, *, /): ")
        num2 = get_number("Enter the second number: ")
        try:
            result = basic_calculator(num1, num2, operation)
            print(f"= {result}")
        except Exception as e:
            print(f"Error: {e}")

        again = input("Calculate again? (y/n): ").strip().lower()
        if again != "y":
            break

# =========================================
# 3) Pro Mode: Safe expression engine + features
# =========================================
getcontext().prec = 28  # change via :prec N
HISTORY: list[tuple[str, Decimal]] = []
LAST: Decimal | None = None
MEMORY = Decimal("0")

OPS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv,
    ast.Pow: op.pow, ast.USub: op.neg, ast.UAdd: op.pos
}

def _to_decimal(value) -> Decimal:
    return Decimal(str(value))

def eval_expr(expr: str) -> Decimal:
    """Safely evaluate + - * / ^ (via **) with parentheses and unary +/- using AST."""
    tree = ast.parse(expr, mode="eval")
    def _eval(node) -> Decimal:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):     # Py3.8+ numbers only
            if isinstance(node.value, (int, float)):
                return _to_decimal(node.value)
            raise ValueError("Only numbers are allowed.")
        if isinstance(node, ast.Num):          # Py<3.8 fallback
            return _to_decimal(node.n)
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
            return OPS[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](_eval(node.left), _eval(node.right))
        raise ValueError("Unsupported expression.")
    return _eval(tree)

PERCENT_LINE = re.compile(r'^\s*([-+]?\d+(?:\.\d+)?)\s*([+-])\s*([-+]?\d+(?:\.\d+)?)%\s*$')

def eval_with_percent(expr: str) -> Decimal:
    """
    Handles:
      A + B%  => A + (A * B/100)
      A - B%  => A - (A * B/100)
    Generic: '10%' becomes (10/100) inside expressions.
    """
    m = PERCENT_LINE.match(expr)
    if m:
        A = Decimal(m.group(1))
        sign = m.group(2)
        B = Decimal(m.group(3)) / Decimal(100)
        return A + (A * B) if sign == '+' else A - (A * B)

    expr = re.sub(r'(\d+(?:\.\d+)?)%', r'(\1/100)', expr)
    return eval_expr(expr)

def show_help():
    print("""
Commands:
  :history        Show last 10 calculations
  :undo           Remove the most recent result
  :mem            Show memory value (MR)
  :mc             Clear memory
  :m+             Add last result to memory
  :m-             Subtract last result from memory
  :prec N         Set decimal precision to N (default 28)
  :help           Show help
  :exit           Quit

Tips:
  • Enter math like: 2.5*(3-1)/-4,  200 + 10%,  (1+2)^3
  • Use ^ for power (converted to **) and parentheses.
  • Chain with last result: if last was 18, input: * 2
""".strip())

def pro_mode():
    global LAST, MEMORY
    print("\n[Pro Mode] Expression calculator (type :help for commands)")
    print("Tips: 2*(3+4), 200 + 10%, (1+2)^3, chain with last: * 2")

    while True:
        expr = input(">>> ").strip()
        if not expr:
            continue
        if expr in (":q", ":quit", ":exit"):
            print("Goodbye!")
            break
        if expr == ":help":
            show_help(); continue
        if expr == ":history":
            if not HISTORY: print("History is empty.")
            else:
                for i, (e, r) in enumerate(HISTORY[-10:], 1):
                    print(f"{i}) {e} = {r}")
            continue
        if expr == ":undo":
            if HISTORY:
                HISTORY.pop()
                LAST = HISTORY[-1][1] if HISTORY else None
                print("Undone.")
            else:
                print("Nothing to undo.")
            continue
        if expr == ":mem":
            print(f"MR = {MEMORY}"); continue
        if expr == ":mc":
            MEMORY = Decimal("0"); print("Memory cleared (MC)."); continue
        if expr == ":m+":
            if LAST is None: print("No last result to add.")
            else: MEMORY += LAST; print("M+ done.")
            continue
        if expr == ":m-":
            if LAST is None: print("No last result to subtract.")
            else: MEMORY -= LAST; print("M- done.")
            continue
        if expr.startswith(":prec"):
            parts = expr.split()
            if len(parts) == 2 and parts[1].isdigit():
                getcontext().prec = int(parts[1])
                print(f"Precision set to {parts[1]}")
            else:
                print("Usage: :prec N")
            continue

        # shorthand chaining: "* 2" -> "<LAST> * 2"
        if LAST is not None and expr[0] in "+-*/^":
            expr = f"{LAST} {expr.replace('^', '**')}"
        else:
            expr = expr.replace("^", "**")

        try:
            result = eval_with_percent(expr)
            print(f"= {result}")
            HISTORY.append((expr, result))
            LAST = result
        except Exception as e:
            print(f"Error: {e}. Try :help")

# =========================================
# 4) Entry point: choose mode (backwards-compatible)
# =========================================
def main():
    print("Calculator")
    print("1) Classic Mode (step-by-step)")
    print("2) Pro Mode (expressions, %, history, memory, precision)")
    choice = input("Choose mode (1/2): ").strip()
    if choice == "2":
        pro_mode()
    else:
        classic_mode()

if __name__ == "__main__":
    main()
