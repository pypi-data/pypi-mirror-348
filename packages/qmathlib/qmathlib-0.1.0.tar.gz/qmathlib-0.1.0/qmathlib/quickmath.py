import random

class QuickMath:
    def __init__(self):
        self.operations = {
            'addition': self.add,
            'subtraction': self.subtract,
            'multiplication': self.multiply,
            'division': self.divide
        }

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

    def generate_problem(self, operation):
        if operation not in self.operations:
            raise ValueError("Invalid operation. Choose from: addition, subtraction, multiplication, division.")
        
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        
        if operation == 'division' and b == 0:
            b = random.randint(1, 10)  # Ensure no division by zero
        
        return a, b