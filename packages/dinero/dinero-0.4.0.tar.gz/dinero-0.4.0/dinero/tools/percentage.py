from dinero import Dinero

from ._validators import ToolValidators


def calculate_percentage(amount: Dinero, percentage: int | float) -> Dinero:
    """
    Calculates the percentage of a given Dinero object.

    Args:
        amount (Dinero): The amount to calculate the percentage of.
        percentage (int | float): The percentage to calculate.

    Returns:
        Dinero: The calculated percentage of the amount.

    Raises:
        InvalidOperationError: If the amount is not an instance of Dinero.
        TypeError: If the percentage argument is not a number.
        ValueError: If the percentage argument is negative.

    Examples:
        >>> amount = Dinero("3000", USD)
        >>> percentage_amount = calculate_percentage(amount, 15)
        >>> percentage_amount.format(symbol=True, currency=True)
        '$450.00 USD'
    """
    validate = ToolValidators()
    validate.percentage_inputs(amount, percentage)
    return amount * (percentage / 100)
