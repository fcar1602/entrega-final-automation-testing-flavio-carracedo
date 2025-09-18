# Basic calculator functions
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def divide (a, b):
    return a / b


def multiply(a, b):
    return a * b


# Mapping of supported operations
_OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}

# Perform the requested operation and return the result.
def simply_calc(operacion: str, a: float, b: float):
    op_key = operacion.strip().lower()
    if op_key not in _OPERATIONS:
        raise ValueError("Invalid operation. Use: +, -, *, /.")
    func = _OPERATIONS[op_key]
    return func(a, b)

# Repeatedly prompt the user until a valid float is entered.
def get_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


# Prompt the user for a valid operation from the supported list.
def get_operation(prompt: str) -> str:
    options = ", ".join(_OPERATIONS.keys())
    while True:
        op = input(f"{prompt} ({options}): ").strip().lower()
        if op in _OPERATIONS:
            return op
        print(f"Invalid operation. Please enter one of the following: {options}.")


# Number input when run as a script
if __name__ == "__main__":
    # Number input
    num1 = get_float("Enter the first number: ")
    num2 = get_float("Enter the second number: ")

    # Operation input
    operation = get_operation("Enter the operation")

    # Execution and exception handling
    try:
        result = simply_calc(operation, num1, num2)
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")
        exit()
    except ValueError as e:
        print(e)
        exit()
    else:
        print(f"Result of {operation} between {num1} and {num2}: {result}")
