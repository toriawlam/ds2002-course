#!/usr/bin/env python3
import random

def get_number(min_value=0, max_value=10):
    """Get a random number between min_value and max_value"""
    number = random.randint(min_value, max_value)
    print(f"Getting number: {number}")
    return number

def divide(n1, n2):
    """Divide n1 by n2"""
    print(f"Dividing {n1} by {n2}")
    return n1 / n2

def add(numbers):
    """Add the numbers in the list"""
    print(f"Adding {numbers}")
    return sum(numbers)

def main():
    """Main workflow"""
    number1 = get_number()
    number2 = get_number()
    sum = add([number1, number2])
    
    number3 = get_number(min_value=1, max_value=3)
    
    result = divide(sum, number3)
    print(f"Result: {result}")
    
if __name__ == "__main__":
    main()