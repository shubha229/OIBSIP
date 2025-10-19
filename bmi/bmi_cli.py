# bmi_cli.py
def get_float(prompt):
    while True:
        try:
            s = input(prompt).strip()
            if not s:
                print("Input cannot be empty.")
                continue
            value = float(s)
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number (e.g. 70 or 1.75).")

def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25.0:
        return "Normal weight"
    elif bmi < 30.0:
        return "Overweight"
    else:
        return "Obesity"

def main():
    print("=== BMI Calculator (CLI) ===")
    weight = get_float("Enter weight in kilograms (kg): ")
    height = get_float("Enter height in meters (m): ")
    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi)
    print(f"\nYour BMI is: {bmi:.2f}")
    print(f"Category: {category}")

if __name__ == "__main__":
    main()
