# Randomade v1.5.2

**Randomade** is built using the `random` library, which comes preinstalled with Python.  
It is specifically built for getting random values. You can currently get:
- Random letters (custom range)
- Random numbers (custom range)
- Random hex codes
- Random strings with numbers, letters and symbols (specified length)
- Random symbols
- Random character (could be a number, symbol or letter)

---

## Docs
-------

## Usage

### **rand_number**  
The `rand_number()` function is for generating a random integer between 2 values (`min_num` and `max_num`).
 
The syntax is: `rand_number(min_num, max_num)`, which returns a random number.

`min_num` and `max_num` can be any number.



### **rand_letter**  
The `rand_letter()` function is for generating a random letter between 2 letters (`min` and `max`).  

The syntax is: `rand_letter(min, max)`, which returns a random letter.

`min` and `max` can be any letter.



### **rand_hex**

The `rand_hex()` is a function used for generating a random hex code.

The syntax is: `rand_hex()`, which returns a random hex code.



### **rand_symbol**

The `rand_symbol()` function is for generating a random symbol (or special character).

The syntax is: `rand_symbol()` (no positional arguments), which returns a random symbol

from the ones on a 100% keyboard. (Only native key ones)

### **rand_string**

The `rand_string()` function is for generating a random string of letters, numbers and symbols

with a specified length (positional argument `length`).

The syntax is: `rand_string(length)` (length can be any integer).



### **rand_character**

The `rand_character()` function is for generating any random character (letter, number or symbol).

The syntax is: `rand_character()` (no positional arguments).

-------------------------------

## Errors

### **rand_letter**


**RandLetterStringError**
Cause: positional argument `min` and/or `max` not passed as a string.

Solution: pass both `min` and `max` as strings.

**RandLetterLengthError**
Cause: more than one character passed in positional argument `min` and/or `max`.

Solution: pass only one character for `min` and `max`.

**RandLetterAlphabetticalError**
Cause: positional argument `max` earlier in alphabetical order than `min`.

Solution: pass `min` as earlier or `max` as later.

**RandLetterArgumentError**
Cause: missing positional argument `min` and/or `max`.

Solution: pass both `min` and `max` positional arguments.



### **rand_number**


**RandNumberOrderError**
Cause: positional argument `min_num` higher than positional argument `max_num`.

Solution: decrease `min_num` or increase `max_num`.

**RandNumberIntegerError**
Cause: position argument `min_num` and/or `max_num` not passed as an integer.

Solution: pass both `min_num` and max

**RandNumberArgumentError**
Cause: positional arguments `min_num` and/or `max_num` missing.

Solution: pass both `min_num` and `max_num` as integers.

### **rand_string**


**RandStringIntegerError**
Cause: positional argument `length` not passed as an integer.

Solution: pass `length` as an integer.


**RandStringArgumentError**
Cause: missing positional argument `length`.

Solution: pass a value as the `length` positional argument.

---

## Fun fact

I wrote all the `rand_letter()` function while waiting for an X-ray in the ER
after breaking my thumb.

Created by Lachy.

GitHub: github.com/backspace-studios