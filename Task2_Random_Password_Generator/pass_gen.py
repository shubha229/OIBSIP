import random
import string

def get_user_preferences():
    """Ask the user for password preferences."""
    while True:
        try:
            length = int(input("Enter desired password length (minimum 4): "))
            if length < 4:
                print("Password length must be at least 4.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    use_letters = input("Include letters? (y/n): ").strip().lower() == 'y'
    use_numbers = input("Include numbers? (y/n): ").strip().lower() == 'y'
    use_symbols = input("Include symbols? (y/n): ").strip().lower() == 'y'

    if not (use_letters or use_numbers or use_symbols):
        print("You must select at least one character type.")
        return get_user_preferences()

    return length, use_letters, use_numbers, use_symbols

def generate_password(length, use_letters, use_numbers, use_symbols):
    """Generate a random password based on user preferences."""
    characters = ""
    if use_letters:
        characters += string.ascii_letters
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    print("=== Random Password Generator ===")
    length, use_letters, use_numbers, use_symbols = get_user_preferences()
    password = generate_password(length, use_letters, use_numbers, use_symbols)
    print(f"\nGenerated password: {password}\n")

if __name__ == "__main__":
    main()
