import uuid
from .alphabet import BASE58_ALPHABET, ALPHABET_LENGTH

def uuid58() -> str:
    """
    Generates a new Base58-encoded UUID (always 22 characters).

    This function combines the standard UUID generation with Base58 encoding
    to create a shorter, URL-safe identifier.

    Returns:
        A 22-character Base58-encoded string representing a newly generated UUID

    Example:
        >>> uuid58()
        "XDY9dmBbcMBXqcRvYw8xJ2"
    """
    # Generate UUID and convert to integer
    num = int(uuid.uuid4().hex, 16)

    # Pre-allocate list for better performance
    chars = [BASE58_ALPHABET[0]] * 22
    i = 21  # Start from the end of the list

    # Convert to Base58
    while num > 0:
        chars[i] = BASE58_ALPHABET[num % ALPHABET_LENGTH]
        num //= ALPHABET_LENGTH
        i -= 1

    return "".join(chars) 