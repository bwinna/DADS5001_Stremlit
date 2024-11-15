import streamlit as st

# Function to perform the calculation
def calculate(num1, num2, operation):
    if operation == 'Add':
        return num1 + num2
    elif operation == 'Subtract':
        return num1 - num2
    elif operation == 'Multiply':
        return num1 * num2
    elif operation == 'Divide':
        if num2 != 0:
            return num1 / num2
        else:
            return "Error - Division by zero"
    else:
        return "Invalid operation"

# Streamlit layout
st.title("Calculator")

# Inputs for the two numbers
num1 = st.number_input("Enter first number:", value=0)
num2 = st.number_input("Enter second number:", value=0)

# Dropdown for selecting the operation
operation = st.selectbox("Select operation:", ["Add", "Subtract", "Multiply", "Divide"])

# Calculate button
if st.button("Calculate"):
    result = calculate(num1, num2, operation)
    st.success(f"Result: {result}")

# Clear button (optional, just reruns the app)
if st.button("Clear"):
    st.experimental_rerun()
