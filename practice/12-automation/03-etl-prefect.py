#!/usr/bin/env python3
import random
from prefect import flow, task


@task
def get_number(min_value=0, max_value=10):
    """Get a random number between min_value and max_value"""
    number = random.randint(min_value, max_value)
    print(f"Getting number: {number}")
    return number

@task
def divide(n1, n2):
    """Divide n1 by n2"""
    print(f"Dividing {n1} by {n2}")
    return n1 / n2

@task
def add(numbers):
    """Add the numbers in the list"""
    print(f"Adding {numbers}")
    return sum(numbers)

@flow(name="Numbers Workflow", log_prints=True)
def main():
    """Main workflow
    The .submit invokes the task in the background
    This enables parallel execution of independent tasks
    """
    number1 = get_number.submit()
    number2 = get_number.submit()
    sum = add.submit([number1, number2])

    number3 = get_number.submit(min_value=1, max_value=3)

    result = divide.submit(sum, number3).result()
    print(f"Result: {result}")


if __name__ == "__main__":
    main()