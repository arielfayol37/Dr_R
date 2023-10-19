from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        # Convert both to float for multiplication
        result = float(value) * float(arg)
        # If the result is an integer (e.g., 2.0), convert it to int for cleaner output
        if result.is_integer():
            return int(result)
        return result
    except (ValueError, TypeError):
        return "Invalid multiplication"
    
@register.filter
def divide(value, arg):
    try:
        # Convert both to float for multiplication
        result = float(value) / float(arg)
        # If the result is an integer (e.g., 2.0), convert it to int for cleaner output
        if result.is_integer():
            return int(result)
        return result
    except (ValueError, TypeError):
        return 0