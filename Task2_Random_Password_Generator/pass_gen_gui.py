import random
import string
import tkinter as tk
from tkinter import messagebox

# -----------------------------
# Functions
# -----------------------------
def generate_password():
    try:
        length = int(length_entry.get())
        if length < 4:
            messagebox.showerror("Error", "Password length must be at least 4.")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for length.")
        return

    use_letters = letters_var.get()
    use_numbers = numbers_var.get()
    use_symbols = symbols_var.get()
    exclude_chars = exclude_entry.get()


    if not (use_letters or use_numbers or use_symbols):
        messagebox.showerror("Error", "Select at least one character type.")
        return

    characters = ""
    if use_letters:
        characters += string.ascii_letters
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    # Remove excluded characters
    characters = ''.join(c for c in characters if c not in exclude_chars)

    if not characters:
        messagebox.showerror("Error", "No characters left to generate password after exclusions.")
        return

    password = ''.join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

def copy_to_clipboard():
    password = password_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "No password to copy.")

# -----------------------------
# GUI Setup
# -----------------------------
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("400x250")
root.resizable(False, False)

# Labels
tk.Label(root, text="Password Length:").pack(pady=(10,0))
length_entry = tk.Entry(root, width=10)
length_entry.pack()

# Checkbuttons
letters_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Letters", variable=letters_var).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Include Numbers", variable=numbers_var).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Include Symbols", variable=symbols_var).pack(anchor='w', padx=20)

# Exclude characters entry
tk.Label(root, text="Exclude Characters (optional):").pack(pady=(10,0))
exclude_entry = tk.Entry(root, width=30)
exclude_entry.pack()

# Generate button
tk.Button(root, text="Generate Password", command=generate_password, bg="#4CAF50", fg="white").pack(pady=10)

# Password display
password_entry = tk.Entry(root, width=35)
password_entry.pack(pady=(0,10))

# Copy button
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, bg="#2196F3", fg="white").pack()

# Run the GUI
root.mainloop()
