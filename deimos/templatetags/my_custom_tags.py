from django import template
from datetime import datetime

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
    
@register.filter   
def format_date(due_date_str):
    # Check if due_date_str is already a datetime object
    if isinstance(due_date_str, datetime):
        due_date = due_date_str
    else:
        # Parsing the date string
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d %H:%M:%S%z')
    # Getting the day with the appropriate suffix
    day = int(due_date.strftime('%d'))
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = 'th'
    else:
        suffix = ['st', 'nd', 'rd'][day % 10 - 1]

    # Formatting the date in the desired format
    formatted_date = due_date.strftime(f'%B {day}{suffix}, %Y at %I:%M%p')
    return formatted_date