def greet(name):
    """Returns a greeting string."""
    return f"Hello, {name}! Welcome to connectionprovider."

def multiply(a, b):
    """Multiplies two numbers and returns the result."""
    return a * b

# Expose functions from the gcp submodule
from .gcp import connect_to_gcp_service, list_gcp_buckets

__all__ = ['greet', 'multiply', 'connect_to_gcp_service', 'list_gcp_buckets'] 