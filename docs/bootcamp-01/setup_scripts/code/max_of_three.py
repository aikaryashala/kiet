print("To find maximum of three numbers.")
num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))
num3 = int(input("Enter the third number: "))
print(f"The greatest of {num1}, {num2} and {num3} is ", end="")
if (num1 < num2):
    temp = num1
    num1 = num2
    num2 = temp
if (num1 < num3):
    temp = num1
    num1 = num3
    num3 = temp
greatest = num1
print(f"{greatest}.")
