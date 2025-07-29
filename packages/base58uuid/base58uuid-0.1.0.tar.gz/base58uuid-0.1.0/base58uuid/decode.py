from typing import Union
from .alphabet import BASE58_ALPHABET, ALPHABET_LENGTH

# Fast lookup map from alphabet characters to their indices
BASE58_MAP = {char: i for i, char in enumerate(BASE58_ALPHABET)}

class Uuid58DecodeError(Exception):
    """Error thrown when an invalid Base58 string is provided for decoding."""
    pass

def uuid58_decode_safe(uuid58: str) -> Union[str, Uuid58DecodeError]:
    """
    Converts a 22-character Base58-encoded string back to a standard UUID format.
    Instead of throwing an error for invalid input, it returns an Uuid58DecodeError instance.

    Args:
        uuid58: The 22-character Base58-encoded UUID string to decode

    Returns:
        A standard UUID string (lowercase, with hyphens), or an Uuid58DecodeError if the input is not valid

    Example:
        >>> uuid58_decode_safe("XDY9dmBbcMBXqcRvYw8xJ2")
        "f4b247fd-1f87-45d4-aa06-1c6fc0a8dfaf"
        >>> uuid58_decode_safe("invalid")
        Uuid58DecodeError
    """
    if len(uuid58) != 22:
        return Uuid58DecodeError(
            f"Base58 string must be exactly 22 characters: {uuid58}"
        )

    num = 0
    for char in uuid58:
        try:
            index = BASE58_MAP[char]
        except KeyError:
            return Uuid58DecodeError(
                f"Invalid Base58 character '{char}' found in input: {uuid58}"
            )
        num = num * ALPHABET_LENGTH + index

    hex_str = format(num, '032x')
    if len(hex_str) != 32:
        return Uuid58DecodeError(
            f"Decoded hexadecimal string is not 32 characters: {uuid58}"
        )

    # Format as UUID with hyphens
    return f"{hex_str[:8]}-{hex_str[8:12]}-{hex_str[12:16]}-{hex_str[16:20]}-{hex_str[20:]}"

def uuid58_decode(uuid58: str) -> str:
    """
    Converts a 22-character Base58-encoded string back to a standard UUID string format.

    Args:
        uuid58: The 22-character Base58-encoded string to decode

    Returns:
        A standard UUID string in the format "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" (always in lowercase)

    Raises:
        Uuid58DecodeError: If the input string is not a valid 22-character Base58 string

    Example:
        >>> uuid58_decode("XDY9dmBbcMBXqcRvYw8xJ2")
        "f4b247fd-1f87-45d4-aa06-1c6fc0a8dfaf"
    """
    result = uuid58_decode_safe(uuid58)
    if isinstance(result, Uuid58DecodeError):
        raise result
    return result 