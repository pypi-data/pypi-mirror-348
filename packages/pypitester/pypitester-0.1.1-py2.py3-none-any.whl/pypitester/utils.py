"""Utility functions for pypitester."""

def greet(name: str) -> str:
    """Return a greeting message.
    
    Args:
        name: The name to greet.
        
    Returns:
        A greeting message.
    """
    return f"Hello, {name}! Welcome to pypitester."

def add(a: int, b: int) -> int:
    """Add two numbers.
    
    Args:
        a: First number.
        b: Second number.
        
    Returns:
        The sum of a and b.
    """
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers.
    
    Args:
        a: First number.
        b: Second number.
        
    Returns:
        The product of a and b.
    """
    return a * b 