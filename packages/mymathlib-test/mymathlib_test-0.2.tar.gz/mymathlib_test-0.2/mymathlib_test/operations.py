# mymathlib_test/operations.py

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def max(a, b):
    if a>b:
        return a
    elif b>a:
        return b
    else:
        return None
