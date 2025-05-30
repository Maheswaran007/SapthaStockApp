import tkinter as tk
from tkinter import ttk, messagebox
from modules import database

class AddConsumeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.selected_item = None
        self.build_ui()
        self.populate_table()

    def build_ui(self):
        columns = ["ID", "Item", "Size", "GSM", "BF", "Reels", "Weight"]
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill="x", padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Weight:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        self.weight_entry = tk.Entry(frame, width=10, font=("Arial", 12))
        self.weight_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Reels:", font=("Arial", 12)).grid(row=0, column=2, padx=5)
        self.reels_entry = tk.Entry(frame, width=10, font=("Arial", 12))
        self.reels_entry.grid(row=0, column=3, padx=5)

        tk.Button(frame, text="Add", width=12, command=self.add_quantity).grid(row=0, column=4, padx=5)
        tk.Button(frame, text="Consume", width=12, command=self.consume_quantity).grid(row=0, column=5, padx=5)

    def populate_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        rows = database.get_all_stock_with_ids()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def on_select(self, event):
        selected = self.tree.focus()
        if selected:
            self.selected_item = self.tree.item(selected)["values"]

    def add_quantity(self):
        self.update_stock(multiplier=1)

    def consume_quantity(self):
        self.update_stock(multiplier=-1)

    def update_stock(self, multiplier=1):
        if not self.selected_item:
            messagebox.showwarning("No Selection", "Please select a stock item first.")
            return
        try:
            qty = float(self.weight_entry.get() or 0) * multiplier
            reels = int(self.reels_entry.get() or 0) * multiplier

            if qty == 0 and reels == 0:
                raise ValueError("Both Weight and Reels are empty or zero.")

            stock_id = self.selected_item[0]
            database.update_stock_quantity(stock_id, qty, reels)

            messagebox.showinfo("Success", "Stock updated successfully.")
            self.weight_entry.delete(0, tk.END)
            self.reels_entry.delete(0, tk.END)
            self.populate_table()
            self.selected_item = None

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
