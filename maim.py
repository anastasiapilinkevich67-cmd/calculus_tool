"""Command-line interface for the advanced calculator.

The module translates user input gathered from the console into structured
calls to :class:`calculus_core.AdvancedCalculator`. Every handler function is
responsible for validating raw text input, converting it into the correct
types, and routing the request to the core calculator object.
"""

from __future__ import annotations

from typing import Callable, Dict, Tuple

from calculus_core import AdvancedCalculator, CalculatorError

Menu = Dict[str, Tuple[str, Callable[[AdvancedCalculator], None]]]


def prompt(message: str) -> str:
    """Return user input (may be empty).

    The helper performs a `strip` so interactive prompts can uniformly work
    with unpadded strings and detect empty responses.
    """
    return input(message).strip()


def prompt_required(message: str) -> str:
    """Request a mandatory value and raise if nothing was provided.

    The function reuses :func:`prompt` to keep the message formatting identical
    and raises a :class:`CalculatorError` so callers share the same error-handling
    path as core calculator failures.
    """
    value = prompt(message)
    if not value:
        raise CalculatorError("Value cannot be empty.")
    return value


def handle_add(calc: AdvancedCalculator) -> None:
    """Collect operands for addition and display the simplified result."""
    a = prompt_required("First addend: ")
    b = prompt_required("Second addend: ")
    print(f"Result: {calc.add(a, b)}")


def handle_subtract(calc: AdvancedCalculator) -> None:
    """Collect operands for subtraction and display the simplified result."""
    a = prompt_required("Minuend: ")
    b = prompt_required("Subtrahend: ")
    print(f"Result: {calc.subtract(a, b)}")


def handle_multiply(calc: AdvancedCalculator) -> None:
    """Collect operands for multiplication and display the simplified result."""
    a = prompt_required("First factor: ")
    b = prompt_required("Second factor: ")
    print(f"Result: {calc.multiply(a, b)}")


def handle_divide(calc: AdvancedCalculator) -> None:
    """Collect operands for division and display the simplified quotient."""
    a = prompt_required("Dividend: ")
    b = prompt_required("Divisor: ")
    print(f"Result: {calc.divide(a, b)}")


def handle_power(calc: AdvancedCalculator) -> None:
    """Collect base and exponent and display the simplified power."""
    base = prompt_required("Base: ")
    exponent = prompt_required("Exponent: ")
    print(f"Result: {calc.power(base, exponent)}")


def handle_root(calc: AdvancedCalculator) -> None:
    """Collect the radicand, optional degree, and display the simplified root."""
    value = prompt_required("Radicand: ")
    degree = prompt("Root degree (default 2): ") or "2"
    print(f"Result: {calc.root(value, degree)}")


def handle_absolute(calc: AdvancedCalculator) -> None:
    """Collect a single value and display its absolute value."""
    value = prompt_required("Argument for absolute value: ")
    print(f"Result: {calc.absolute(value)}")


def handle_logarithm(calc: AdvancedCalculator) -> None:
    """Collect logarithm parameters and display the simplified value."""
    value = prompt_required("Logarithm argument: ")
    base = prompt("Base (leave blank for natural logarithm): ")
    base_value = base if base else None
    print(f"Result: {calc.logarithm(value, base_value)}")


def handle_quadratic(calc: AdvancedCalculator) -> None:
    """Collect coefficients of a quadratic equation and print both roots."""
    a = prompt_required("Coefficient a: ")
    b = prompt_required("Coefficient b: ")
    c = prompt_required("Coefficient c: ")
    roots = calc.solve_quadratic(a, b, c)
    print(f"Roots: {roots[0]}, {roots[1]}")


def handle_geometry(calc: AdvancedCalculator) -> None:
    """Route a geometry helper request and show a labeled result.

    The handler expects a symbolic name that matches one of the calculator's
    geometry helpers. Parameter parsing accepts a lightweight ``key=value``
    syntax so multiple values can be supplied without additional prompts.
    """
    print(
        "Available operations: circle_area, circle_circumference, rectangle_area, "
        "rectangle_perimeter, triangle_area, triangle_perimeter"
    )
    figure = prompt_required("Operation name: ")
    params_raw = prompt("Parameters (comma separated, e.g. radius=3 or side_a=3,side_b=4,side_c=5): ")

    parameters: Dict[str, str] = {}
    if params_raw:
        for item in params_raw.split(","):
            item = item.strip()
            if not item:
                continue
            if "=" not in item:
                raise CalculatorError(f"Invalid parameter: {item}")
            key, value = item.split("=", maxsplit=1)
            parameters[key.strip()] = value.strip()

    result = calc.geometry(figure, **parameters)
    print(f"{result.name}: {result.value}")


def handle_limit(calc: AdvancedCalculator) -> None:
    """Collect limit parameters, including direction, and print the evaluation."""
    expression = prompt_required("Expression: ")
    variable = prompt_required("Variable: ")
    approaching = prompt_required("Approaches: ")
    direction = prompt("Direction [both/plus/minus] (default both): ") or "both"
    print(f"Limit: {calc.limit(expression, variable, approaching, direction)}")


def handle_expression(calc: AdvancedCalculator) -> None:
    """Collect an expression and optional substitutions and display the result."""
    expression = prompt_required("Expression: ")
    subs_raw = prompt("Substitutions (format x=1,y=2, optional): ")

    substitutions: Dict[str, str] = {}
    if subs_raw:
        for item in subs_raw.split(","):
            item = item.strip()
            if not item:
                continue
            if "=" not in item:
                raise CalculatorError(f"Invalid substitution: {item}")
            key, value = item.split("=", maxsplit=1)
            substitutions[key.strip()] = value.strip()

    result = calc.evaluate_expression(expression, substitutions or None)
    print(f"Result: {result}")


def handle_equation(calc: AdvancedCalculator) -> None:
    """Collect an equation definition and show the symbolic solution set."""
    equation = prompt_required("Equation (use '=' or imply =0): ")
    variable = prompt_required("Solve for variable: ")
    solutions = calc.solve_equation(equation, variable)
    print(f"Solutions: {solutions}")


def get_menu() -> Menu:
    """Assemble the CLI menu mapping identifiers to handler functions."""
    return {
        "1": ("Addition", handle_add),
        "2": ("Subtraction", handle_subtract),
        "3": ("Multiplication", handle_multiply),
        "4": ("Division", handle_divide),
        "5": ("Exponentiation", handle_power),
        "6": ("Root", handle_root),
        "7": ("Absolute value", handle_absolute),
        "8": ("Logarithm", handle_logarithm),
        "9": ("Quadratic equation", handle_quadratic),
        "10": ("Geometry helper", handle_geometry),
        "11": ("Limit", handle_limit),
        "12": ("Expression mode", handle_expression),
        "13": ("Equation mode", handle_equation),
    }


def main() -> None:
    """Start the interactive loop that powers the command-line interface."""
    calculator = AdvancedCalculator()
    menu = get_menu()

    print("Advanced calculator (press Enter on empty choice to exit).")

    while True:
        print("\nChoose an action:")
        for key, (label, _) in menu.items():
            # The menu is rendered on every loop iteration to reflect potential
            # future dynamic updates and keep the UX predictable.
            print(f"  {key}. {label}")
        choice = prompt("\nYour choice: ")
        if not choice:
            print("Goodbye!")
            break

        action = menu.get(choice)
        if not action:
            print("Unknown command. Try again.")
            continue

        _, handler = action
        try:
            handler(calculator)
        except CalculatorError as exc:
            # Surface human-readable errors without displaying stack traces.
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
