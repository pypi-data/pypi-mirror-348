#imports

import random

class RandLetterStringError(Exception):
    pass
class RandLetterLengthError(Exception):
    pass
class RandLetterAlphabeticalError(Exception):
    pass
class RandNumberOrderError(Exception):
    pass
class RandNumberIntegerError(Exception):
    pass
class RandStringIntegerError(Exception):
    pass
class RandStringArgumentError(Exception):
    pass
class RandLetterArgumentError(Exception):
    pass
class RandNumberArgumentError(Exception):
    pass

def rand_letter(min:str = "", max:str = ""):

    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    if isinstance(min, str) and isinstance(max, str):
        max = max.upper()
        min = min.upper()
    if not isinstance(max, str) or not max in letters:
        raise RandLetterStringError(
            """Positional argument "min" and/or "max" not passed as a string. Check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)""")
    if len(min) < 1:
        raise RandLetterArgumentError(
            """Missing positional argument "min" and/or "max". Check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)""")
    max = max.upper()
    min = min.upper()
    if len(max) < 1:
        raise RandLetterArgumentError(
            """Missing positional argument "min" and/or "max". Check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)""")
    if not isinstance(min, str) or not min in letters:
        raise RandLetterStringError("""Positional argument "min" and/or "max" not passed as a string. Check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)""")
    if letters.index(min) > letters.index(max):
        raise RandLetterAlphabeticalError("""Positional argument "min" > "max". Check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)""")
    if len(min) > 1:
        raise RandLetterLengthError("""More than character passed in positional argument "min" and/or "max". Check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)""")
    if len(max) > 1:
        raise RandLetterLengthError("""More than character passed in positional argument "min" and/or "max". Check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)""")
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
    index1 = letters.index(min)
    index2 = letters.index(max)
    max_int = nums[index2]
    min_int = nums[index1]
    rand_int = random.randint(min_int, max_int)
    index = nums.index(rand_int)
    letter = letters[index]
    return letter

def rand_number(min_num:int = None, max_num:int = None):
    if not isinstance(min_num, int) or not isinstance(max_num, int):
        raise RandNumberIntegerError("""Positional argument "max_num" or "min_num" not passed as an integer. Check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)""")
    if min_num is None:
        raise RandNumberArgumentError("""missing positional argument "max_num" and/or "min_num. Check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)""")
    if max_num is None or not isinstance(max_num, int):
        raise RandNumberArgumentError("""missing positional argument "max_num" and/or "min_num. Check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)""")
    try:
        if not isinstance(min_num, int) or not isinstance(max_num, int):
            raise RandNumberIntegerError("""Positional argument "min_num" and/or "max_num" not passed as an integer. Check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)""")
        try:
            rand_num = random.randint(min_num, max_num)
            return rand_num
        except ValueError:
            raise RandNumberOrderError("""Positional argument "min_num" higher than positional argument "max_num". Check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)""")
    except TypeError:
        raise RandNumberIntegerError("""Positional argument "min_num" not passed as an integer. Check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)""")

def rand_hex():
    hex = []
    spaces = [1, 2, 3, 4, 5, 6]
    for _ in spaces:
        num_or_let = rand_number(1, 2)
        if num_or_let == 1:
            hex.append(rand_letter("A", "F"))
        if num_or_let == 2:
            hex.append(str(rand_number(0, 9)))
    hex_str = str(hex).replace("'", "").replace(" ", "").replace("[", "").replace("]", "").replace(",", "").strip()
    return f"#{hex_str}"

def rand_symbol():
    symbols = ["~", "`", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "[", "]", "{", "}", "\\", "|", ";", ":", "'", "\"", ",", ".", "<", ">", "/", "?"]
    symbol = random.choice(symbols)
    return symbol


def rand_character():
    lett_num_sym = rand_number(1, 3)
    if lett_num_sym == 1:
        char = rand_symbol()
    elif lett_num_sym == 2:
        char = str(rand_number(0, 9))
    elif lett_num_sym == 3:
        char = rand_letter("A", "z")
    return char

def rand_string(length:int = None):
    if length is None:
        raise RandStringArgumentError("""missing positional argument "length". Check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)""")
    if not isinstance(length, int):
        raise RandStringIntegerError("""positional argument "length" not passed as an integer. Check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)""")
    if length >= 5000000:
        print("Generating... (this make take a long time on lower end PCs)")
    if length < 500000:
        print("Generating...")
    spaces = list(range(1, length+1))
    string = [rand_character() for _ in spaces]
    string = str(string).replace(" ", "").replace(",", "").replace("[", "").replace("]", "").replace("'", "").strip()
    return string