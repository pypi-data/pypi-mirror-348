def decimal_to_binary(number: int) -> str:
    if not isinstance(number, int):
        raise ValueError("Input must be an integer.")
    return bin(number)[2:]

def binary_to_decimal(binary_str: str) -> int:
    if not all(c in "01" for c in binary_str):
        raise ValueError("Input must be a binary.")
    return int(binary_str, 2)