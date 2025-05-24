import tkinter as tk
from tkinter import messagebox
from modules import database

class AddStockFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.build_form()

    def build_form(self):
        fields = ["Item Name", "Size", "GSM", "BF", "No. of Reels", "Weight"]
        self.entries = {}

        for i, label in enumerate(fields):
            tk.Label(self, text=label, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=8, sticky='e')
            entry = tk.Entry(self, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=8, sticky='w')
            self.entries[label] = entry

        tk.Button(self, text="Save", font=("Arial", 12), width=20,
                  command=self.save_stock).grid(row=len(fields), columnspan=2, pady=20)

    def save_stock(self):
        try:
            vals = {label: self.entries[label].get() for label in self.entries}
            database.add_stock(
                vals["Item Name"],
                float(vals["Size"]),
                int(vals["GSM"]),
                int(vals["BF"]),
                int(vals["No. of Reels"]),
                float(vals["Weight"])
            )
            messagebox.showinfo("Success", "Stock added successfully.")
            for entry in self.entries.values():
                entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
