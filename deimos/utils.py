import math
import re
from urllib.parse import urlparse
from urllib.parse import unquote  # Import unquote for URL decoding
from sympy import symbols, simplify

def transform_expression(expr):
    """Insert multiplication signs between combined characters, except within trig functions."""
    expression = remove_extra_spaces_around_operators(expr)
    expression = expression.replace(', ', '')
    expression = expression.replace(' ', '*')
    expression = re.sub(r'1e\+?(-?\d+)', r'10^\1', expression)
    trig_functions = {
        'asin': 'ò', 'acos': 'ë', 'atan': 'à', 'arcsin': 'ê', 'arccos': 'ä',
        'arctan': 'ï', 'sinh': 'ù', 'cosh': 'ô', 'tanh': 'ü', 'sin': 'î', 'cos': 'â', 'tan': 'ö', 'log': 'ÿ', 'ln': 'è',
        'cosec': 'é', 'sec': 'ç', 'cot': 'û', 'sqrt':'у́', 'pi': 'я',
    }

    expression = encode(expression, trig_functions)
    transformed_expression = ''.join(
        char if index == 0 or not needs_multiplication(expression, index, trig_functions)
        else '*' + char for index, char in enumerate(expression)
    )
    transformed_expression = transformed_expression.replace('^', '**')
    return decode(transformed_expression, trig_functions)

def remove_extra_spaces_around_operators(text):
    pattern = r'(\s*([-+*/^])\s*)'
    return re.sub(pattern, lambda match: match.group(2), text)

def needs_multiplication(expr, index, trig_functions):
    char = expr[index]
    prev_char = expr[index - 1]
    return (
        (char.isalpha() or char in trig_functions.values()) and prev_char.isalnum() or
        char.isdigit() and prev_char.isalpha() or
        char == "(" and (prev_char.isalpha() and not prev_char in trig_functions.values())
    )

def encode(text, trig_functions):
    """Takes a string and replaces trig functions with their corresponding special character."""
    result = text
    for key, value in trig_functions.items():
        result = result.replace(key, value)
    return result

def decode(text, trig_functions):
    """Takes a string and replaces special character with their corresponding trig function."""
    special_chars = {'e':'E', 'i':'((-1)^0.5)'}
    result = text
    # !Important.  special_chars for loop must come before 
    # the trig_functions for loop!
    for sc, value in special_chars.items():
        result = result.replace(sc, value)
    for key, value in trig_functions.items():
        result = result.replace(value, key)
    return result
def  extract_numbers(text):
    """
    Returns a list of numbers and subscrippted characters in a string.
    # E.g of a subscriptted char: 'e_1'
    """
    # Regular expression pattern to match numbers and subscriptted chars.
    
    pattern = r'[-+]?\d*\.\d+|\d+|\w+_\w+'
    
    # Find all matches using the pattern
    matches = re.findall(pattern, text)
    
    return matches

def compare_expressions(expression1, expression2, for_units=False):
    """
    Given two strings e1 and e2,
    returns True if they are algebraically equivalent,
    returns False otherwise.
    """
    if not for_units:
        e1 = transform_expression(expression1)
        e2 = transform_expression(expression2)
        if not (isinstance(e1, str) and isinstance(e2, str)):
            raise ValueError("Both inputs should be strings")
    else:
        e1, e2 = expression1, expression2
    symbols_union = set(e1) | set(e2)  # Combined set of symbols from both expressions
    symbols_union.update(extract_numbers(e1 + e2))  # Update with extracted numbers
    symbls = symbols(' '.join(symbols_union), real=True, positive=True)
    sym_e1 = simplify(e1, symbols=symbls)
    sym_e2 = simplify(e2, symbols=symbls)
    difference = (simplify(sym_e1 - sym_e2, symbols=symbls))
    return True if difference == 0 else False

def compare_floats(correct_answer, simplified_answer, margin_error=0.0, get_feedback=True):
    """
    Takes two floats f1 and f2,
    returns True if they are equal or close,
    returns False otherwise
    """
    f1 = eval(str(correct_answer))
    f2 = eval(str(simplified_answer))
    feedback_message = ""
    correct = (abs(f1-f2) <= margin_error * abs(f1)) and f1*f2 >= 0
    if not correct and get_feedback:
        feedback_message = feedback_floats(f1, f2, margin_error) 
    return (correct, feedback_message)

def feedback_floats(base_float, inputed_float, margin_error):
    """
    Helper function that returns a feedback message when two floats
    differ but may be integer multiples (within n=2) of each other.
    Margin error is a percentage.
    """
    assert 0 <= margin_error <= 1
    abs_quotient = abs(inputed_float)/abs(base_float) if base_float != 0 and inputed_float!= 0 else 0
    if abs_quotient == 0:
        return ""
    def check_int_interval(a, b):
        # Checking whether there is an integer between a and b
        if not a < b:
            a, b = b, a
        f_a = math.floor(a)
        f_b = math.floor(b)
        diff = abs(f_b - f_a)
        if a == b and (f_a - a) == 0:
            return int(a)
        if type(diff) == int and diff != 0:
            return f_a + diff
        else:
            return None
    sign = "-" if base_float * inputed_float < 0 else ""    
    a_0 = abs_quotient * (1 - margin_error)
    b_0 = abs_quotient * (1 + margin_error)
    n_0 = check_int_interval(a_0, b_0)
    if n_0 and n_0 < 3:
        # return f"Your answer is {sign}{n_0}x the correct answer"
        return f"Your answer is {sign}n times the correct answer"
    a_1 = (abs_quotient)**-1 * (1 - margin_error)
    b_1 = (abs_quotient)**-1 * (1 + margin_error)
    n_1 = check_int_interval(a_1, b_1)
    if n_1 and n_1 < 3:
        # return f"Your answer is {sign}{n_1 ** -1}x the correct answer"
        return f"Your answer is {sign}n times the correct answer"
    # Checking for 10^n submission mistake
    a = math.log10(abs_quotient * (1 - margin_error))
    b = math.log10(abs_quotient * (1 + margin_error))
    n = check_int_interval(a, b)
    if n:
        # return f"Your answer is {sign}10^{n} x the correct answer"
        return f"Your answer is {sign}10<sup>n</sup> x the correct answer"
    return ""
    
def compare_units(units_1, units_2):
    """
    Takes two units units_1 and units_2
    returns True if they are equivalent
    returns False otherwise
    """
    
    # custom_base_units = ['m', 's', 'cd', 'K', 'mol', 'g', 'A']
    scales = {'k':'(10^3)', 'u':'(10^-6)', 'm_':'(10^-3)', 'p':'(10^-12)', 'M':'(10^6)', 'n':'(10^-9)','µ':'(10^-6)'}
    # Important! Hz must come before H, as well as Sv before S, Wb before W etc
    correspondances = {
        'C': '(A*s)', 'V': '(k*g*m^2*s^-3*A^-1)','Ω': '(k*g m^2*s^-3*A^-2)',
        'T': '(k*g*s^-2*A^-1)','Hz': '(s^-1)','Pa': '(k*g*m^-1*s^-2)','N': '(k*g*m*s^-2)','J': '(k*g*m^2*s^-2)',
        'Wb':'(k*g*m^2*A*s^-2)','W': '(k*g*m^2*s^-3)', 'F':'(k*g*A^2*s^4*m^-2)', 'H':'(k*g*m^2*A^2*s^-2)',
        'Sv':'(m^2*s^-2)','S':'(k*g*s^3*A^2*m^-2)', 'lx':'(cd*m^-2)', 'Bq':'(s^-1)', 'Gy':'(m^2*s^-2)', 'kat':'(mol*s^-1)',
        'atm':'(101325*k*g*m^-1*s^-2)'
    }
    # transform_units_expression() must be done before to replacing the correspondances
    # and scales to reduce runtime.
    units_1 = transform_units_expression(units_1)
    units_2 = transform_units_expression(units_2)

    for key, value in correspondances.items():
        units_1 = units_1.replace(key, value)
        units_2 = units_2.replace(key, value)
    for key, value in scales.items():
        units_1 = units_1.replace(key, value)
        units_2 = units_2.replace(key, value)
    return compare_expressions(units_1, units_2, for_units=True)

def transform_units_expression(expr):
    """Insert multiplication signs between combined characters, except within trig functions."""
    expression = remove_extra_spaces_around_operators(expr)
    expression = expression.replace(', ', '')
    expression = expression.replace(' ', '*')
    expression = re.sub(r'1e\+?(-?\d+)', r'10^\1', expression)
    # replacements are units that are more than 1 character. e.g Hz, Pa, cd, mol
    replacements = {
        'cd': 'ò', 'mol': 'ë', 'Hz': 'à', 'Pa': 'ê','Wb': 'ä',
        'lx': 'Bq', 'Gy': 'ù', 'Sv': 'ô', 'kat': 'ü', 'atm':'у́'
    }

    expression = encode(expression, replacements)
    transformed_expression = ''.join(
        char if index == 0 or not needs_multiplication(expression, index, replacements)
        else '*' + char for index, char in enumerate(expression)
    )
    transformed_expression = transformed_expression.replace('^', '**')
    return decode(transformed_expression, replacements)
    
def replace_links_with_html(text):
    """
    Find linkes in text and return text with those links
    within html a-tags.
    """
    words = text.split()
    new_words = []
    for word in words:
        if word.startswith('http://') or word.startswith('https://'):
            parsed_url = urlparse(word)
            link_tag = f'<a href="{word}">{parsed_url.netloc}{parsed_url.path}</a>'
            new_words.append(link_tag)
        else:
            new_words.append(word)

    return ' '.join(new_words)

def replace_vars_with_values(text, variable_dict):
    # Deprecated
    """
    Find variables in text, and replace with highlited/colored values of instances.
    """
    for var_symbol in variable_dict:
        # TODO: !Important Make the replacements only when the text has something 
        # to indicate that a certain sequence of string will contain
        # variables. Perhaps  {}
        text = text.replace(var_symbol,f"<em class=\"variable\">{variable_dict[var_symbol]}</em>")
    return text

def replace_image_labels_with_links(text, labels_url_pairs):
    """
    Returns the text with labels within html link tags.
    labels_url_pairs = ("john_image", "astros/images/jjs.png")
    """
    for label, url in labels_url_pairs:
        replacement = f"<a href=\"#{url}\">{label}</a>"
        text = text.replace(label, replacement)
    return text