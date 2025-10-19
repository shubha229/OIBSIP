import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

CSV_FILE = os.path.join(os.path.dirname(__file__), "bmi_history.csv")

# ---------- Utility Functions ----------
def calculate_bmi(weight, height):
    try:
        weight = float(weight)
        height = float(height)
        if height <= 0:
            raise ValueError("Height must be positive.")
        bmi = round(weight / (height ** 2), 2)
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obesity"
        return bmi, category
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values.")
        return None, None

def save_bmi(name, weight, height, bmi, category):
    record = {
        "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "name": name or "Unknown",
        "weight": weight,
        "height": height,
        "bmi": bmi,
        "category": category
    }
    df = pd.DataFrame([record])
    if not os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, index=False)
    else:
        df.to_csv(CSV_FILE, mode="a", header=False, index=False)
    messagebox.showinfo("Success", f"BMI record saved for {record['name']}.")

def plot_bmi_trends():
    if not os.path.exists(CSV_FILE):
        messagebox.showerror("No Data", "No BMI records found.")
        return
    df = pd.read_csv(CSV_FILE, encoding="utf-8-sig", header=None,
                     names=["date", "name", "weight", "height", "bmi", "category"])
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    plt.figure(figsize=(8, 5))
    for user in df["name"].unique():
        user_df = df[df["name"] == user].sort_values("date")
        plt.plot(user_df["date"], user_df["bmi"], marker='o', label=user)

    plt.title("BMI Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ---------- GUI ----------
root = tk.Tk()
root.title("Smart BMI Tracker")
root.geometry("400x500")
root.resizable(False, False)

# Modern style
style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TEntry", font=("Segoe UI", 10))

ttk.Label(root, text="Smart BMI Tracker", font=("Segoe UI", 16, "bold")).pack(pady=10)

frame = ttk.Frame(root, padding=20)
frame.pack(fill="x")

def clear_data():
    if not os.path.exists(CSV_FILE):
        messagebox.showinfo("No Data", "No BMI records found to clear.")
        return
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete all BMI records?")
    if confirm:
        try:
            os.remove(CSV_FILE)
            messagebox.showinfo("Cleared", "✅ All BMI data has been cleared.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear data:\n{e}")

# Input fields
labels = ["Name", "Weight (kg)", "Height (m)"]
entries = {}
for label in labels:
    ttk.Label(frame, text=label).pack(anchor="w", pady=5)
    entry = ttk.Entry(frame)
    entry.pack(fill="x", pady=5)
    entries[label] = entry

# Output feedback area
result_label = ttk.Label(root, text="", font=("Segoe UI", 11))
result_label.pack(pady=10)

# Actions
def handle_calculate():
    name = entries["Name"].get()
    weight = entries["Weight (kg)"].get()
    height = entries["Height (m)"].get()
    bmi, category = calculate_bmi(weight, height)
    if bmi:
        result_label.config(text=f"{name or 'Unknown'}'s BMI: {bmi} ({category})", foreground="blue")
        save_bmi(name, weight, height, bmi, category)


ttk.Button(root, text="Calculate & Save", command=handle_calculate).pack(pady=10)
ttk.Button(root, text="View BMI Trends", command=plot_bmi_trends).pack(pady=5)
ttk.Button(root, text="Clear All BMI Data", command=clear_data).pack(pady=5)
# Instructions
ttk.Label(
    root,
    wraplength=350,
    foreground="#555",
    font=("Segoe UI", 9)
).pack(pady=15)

root.mainloop()
