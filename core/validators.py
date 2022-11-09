import re


def is_valid_iran_code(n_code):
    if not re.search(r"^\d{10}$", n_code):
        return False
    check = int(n_code[9])
    s = sum(int(n_code[x]) * (10 - x) for x in range(9)) % 11
    return check == s if s < 2 else check + s == 11
