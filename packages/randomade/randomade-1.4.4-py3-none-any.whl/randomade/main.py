import random

def rand_letter(min:str, max:str):
    try:
        letters = ["A", "B", "C", "D", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
        index1 = letters.index(min)
        index2 = letters.index(max)
        max_int = nums[index2]
        min_int = nums[index1]
        rand_int = random.randint(min_int, max_int)
        index = nums.index(rand_int)
        letter = letters[index]
        return letter
    except ValueError:
        print("RandLetterValueError: check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)")
        return "RandLetterValueError: check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)"

def rand_number(min_num:int, max_num:int):
    try:
        rand_num = random.randint(min_num, max_num)
        return rand_num
    except ValueError:
        print("RandNumberValueError: check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade")
        return "RandNumberValueError: check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)"
    except TypeError:
        print("RandNumberTypeError: check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)")
        return "RandNumberTypeError: check PyPi or GitHub docs for cause and solution (https://pypi.org/project/randomade or https://github.com/Backspace-Studios/Randomade)"

def rand_hex():
    global hex_str
    hex = []
    spaces = [1, 2, 3, 4, 5, 6]
    for _ in spaces:
        num_or_let = rand_number(1, 2)
        if num_or_let == 1:
            hex.append(rand_letter("A", "F"))
        if num_or_let == 2:
            hex.append(rand_number(0, 9))
        hex_str = str(hex).replace("'", "").replace(" ", "").replace("[", "").replace("]", "").replace(",", "").strip()
    return f"#{hex_str}"
