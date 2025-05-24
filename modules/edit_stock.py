import tkinter as tk
from tkinter import ttk, messagebox
from modules import database

class EditStockFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.selected_item = None
        self.build_ui()
        self.populate_table()

    def build_ui(self):
        columns = ["Item", "Size", "GSM", "BF", "Reels", "Weight"]
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill="x", padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Input area
        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Weight:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        self.weight_entry = tk.Entry(frame, width=10, font=("Arial", 12))
        self.weight_entry.grid(row=0, column=1, padx=5)

        tk.Button(frame, text="Add", width=12, command=self.add_weight).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Consume", width=12, command=self.consume_weight).grid(row=0, column=3, padx=5)

    def populate_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in database.get_all_stock():
            self.tree.insert("", "end", values=row)

    def on_select(self, event):
        selected = self.tree.focus()
        if selected:
            self.selected_item = self.tree.item(selected)["values"]

    def add_weight(self):
        self.update_stock(multiplier=1)

    def consume_weight(self):
        self.update_stock(multiplier=-1)

    def update_stock(self, multiplier=1):
        if not self.selected_item:
            messagebox.showwarning("No Selection", "Select a stock item first.")
            return
        try:
            weight = float(self.weight_entry.get()) * multiplier
            reels = 0  # Do not change reels
            item_name, size, gsm, bf, *_ = self.selected_item
            database.add_stock(item_name, size, gsm, bf, reels, weight)
            messagebox.showinfo("Success", "Stock updated.")
            self.weight_entry.delete(0, tk.END)
            self.populate_table()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
