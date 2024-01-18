def decimal_to_binary(decimal_number, num_digits=None):
    if decimal_number == 0:
        return "0"
    binary_number = ''
    while decimal_number > 0:
        remainder = decimal_number % 2
        binary_number = str(remainder) + binary_number
        decimal_number = decimal_number // 2

    if num_digits:
        binary_number = binary_number.zfill(num_digits)
    return binary_number
