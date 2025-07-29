from typing import Union
from .alphabet import BASE58_ALPHABET, ALPHABET_LENGTH

class Uuid58EncodeError(Exception):
    """Error thrown when an invalid UUID string is provided for encoding."""
    pass

def uuid58_encode_safe(uuid: str) -> Union[str, Uuid58EncodeError]:
    """
    Converts a standard UUID string to a 22-character Base58-encoded format.
    Instead of throwing an error for invalid input, it returns an Uuid58EncodeError instance.

    Args:
        uuid: The UUID string to encode (with or without hyphens)

    Returns:
        A 22-character Base58-encoded string, or an Uuid58EncodeError if the input is not a valid UUID

    Example:
        >>> uuid58_encode_safe("f4b247fd-1f87-45d4-aa06-1c6fc0a8dfaf")
        "XDY9dmBbcMBXqcRvYw8xJ2"
        >>> uuid58_encode_safe("invalid")
        Uuid58EncodeError
    """
    hex_str = uuid.replace("-", "")
    if len(hex_str) != 32:
        return Uuid58EncodeError(
            f"Invalid UUID length: expected 32 characters (excluding hyphens), got {len(hex_str)} characters in '{uuid}'"
        )

    try:
        num = int(hex_str, 16)
    except ValueError:
        return Uuid58EncodeError(
            f"Invalid UUID format: '{uuid}' contains non-hexadecimal characters"
        )

    # Pre-allocate list for better performance
    chars = [BASE58_ALPHABET[0]] * 22
    i = 21  # Start from the end of the list

    # Convert to Base58
    while num > 0:
        chars[i] = BASE58_ALPHABET[num % ALPHABET_LENGTH]
        num //= ALPHABET_LENGTH
        i -= 1

    return "".join(chars)

def uuid58_encode(uuid: str) -> str:
    """
    Converts a standard UUID string to a 22-character Base58-encoded format.

    Args:
        uuid: The UUID string to encode. Can be provided with or without hyphens
             (format: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" or "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx").
             The input is case-insensitive, so both uppercase and lowercase hexadecimal characters are accepted.

    Returns:
        A 22-character Base58-encoded string representation of the UUID

    Raises:
        Uuid58EncodeError: If the input string is not a valid UUID format

    Example:
        >>> uuid58_encode("f4b247fd-1f87-45d4-aa06-1c6fc0a8dfaf")
        "XDY9dmBbcMBXqcRvYw8xJ2"
    """
    result = uuid58_encode_safe(uuid)
    if isinstance(result, Uuid58EncodeError):
        raise result
    return result 