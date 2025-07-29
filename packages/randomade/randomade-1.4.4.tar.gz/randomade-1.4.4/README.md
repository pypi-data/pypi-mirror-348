# Randomade v1.4.4
==============

**Randomade** is built using the `random` library, which comes preinstalled with Python.  
It is specifically built for getting random values. You can currently get:
- Random letters (custom range)
- Random numbers (custom range)
- Random hex codes (no range)

---

## Docs
-------

## Usage
--------

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

---

## Errors
------

### **RandLetterValueError**  
`RandLetterValueError` can occur for 4 reasons.

**Reason 1** - Lowercase used in `min` or `max` values on the `rand_letter()`  
**Reason 2** - `max` value before `min` alphabetically  
**Reason 3** - Anything except string passed as `min` or `max` values  
**Reason 4** - `min` or `max` contain anything except a single letter

**Solution 1** - Use uppercase for both `min` and `max` values  
**Solution 2** - Use an earlier `min` or later `max` value  
**Solution 3** - Use a string for both `min` and `max` values  
**Solution 4** - Make sure the value of `min` and `max` contain just a single letter

---

### **RandNumberTypeError**  
`RandNumberTypeError` can occur for 1 reason.

**Reason 1** - Anything except an integer passed as `min_num` or `max_num`  
**Solution 1** - Use an integer for both `min_num` and `max_num` values

---

### **RandNumberValueError**  
`RandNumberValueError` can occur for 1 reason.

**Reason 1** - `min_num` higher than `max_num`  
**Solution 1** - Use a lower `min_num` or higher `max_num`

---

## Fun fact
---------
I wrote all the `rand_letter()` function while waiting for an X-ray in the ER
after breaking my thumb.
