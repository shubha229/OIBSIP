# bmi_plot.py
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

CSV_FILE = os.path.join(os.path.dirname(__file__), "bmi_history.csv")

def load_history():
    if not os.path.exists(CSV_FILE):
        print("No history file found:", CSV_FILE)
        return None

    # Try reading with utf-8-sig to handle hidden BOM issues
    df = pd.read_csv(
        CSV_FILE,
        encoding="utf-8-sig",
        header=None,
        names=["date", "name", "weight", "height", "bmi", "category"]
    )


    # Clean up column names (strip spaces, hidden chars)
    df.columns = df.columns.str.strip()

    # Debugging line to see what pandas detects
    print("Columns detected:", df.columns.tolist())

    if "date" not in df.columns:
        print("CSV exists but 'date' column is missing.")
        return None

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def plot_bmi_trends():
    df = load_history()
    if df is None or df.empty:
        print("No BMI records to plot.")
        return
    # group by name (if multiple users) or overall
    users = df["name"].unique()
    plt.figure(figsize=(10, 5))
    for user in users:
        user_df = df[df["name"] == user].sort_values("date")
        plt.plot(user_df["date"], user_df["bmi"].astype(float), marker='o', label=str(user))
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.title("BMI Trend Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_bmi_trends()
