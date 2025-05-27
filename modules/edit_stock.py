import tkinter as tk
from tkinter import ttk, messagebox
from modules import database

class EditStockFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.selected_item = None
        self.selected_item_id = None
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

        # Edit section
        self.edit_frame = tk.Frame(self)
        self.edit_frame.pack(pady=10)

        self.entries = {}
        labels = ["Item", "Size", "GSM", "BF", "Reels", "Weight"]
        for i, label in enumerate(labels):
            tk.Label(self.edit_frame, text=label + ":", font=("Arial", 11)).grid(row=0, column=i*2)
            entry = tk.Entry(self.edit_frame, width=10, font=("Arial", 11))
            entry.grid(row=0, column=i*2+1, padx=5)
            self.entries[label.lower()] = entry

        tk.Button(self.edit_frame, text="Save Changes", command=self.save_changes, bg="#4CAF50", fg="white").grid(row=1, column=0, columnspan=3, pady=10)
        tk.Button(self.edit_frame, text="Delete", command=self.delete_stock, bg="red", fg="white").grid(row=1, column=3, columnspan=3, pady=10)

    def populate_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.stock_data = database.get_all_stock_with_ids()
        for row in self.stock_data:
            stock_id = row[0]
            values = row[1:]
            self.tree.insert("", "end", iid=str(stock_id), values=values)

    def on_select(self, event):
        selected = self.tree.focus()
        if selected:
            self.selected_item_id = int(selected)
            self.selected_item = self.tree.item(selected)["values"]
            keys = ["item", "size", "gsm", "bf", "reels", "weight"]
            for i, key in enumerate(keys):
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, str(self.selected_item[i]))

    def save_changes(self):
        if not self.selected_item_id:
            messagebox.showwarning("No Selection", "Select a stock entry to edit.")
            return
        try:
            item_name = self.entries["item"].get()
            size = float(self.entries["size"].get())
            gsm = float(self.entries["gsm"].get())
            bf = float(self.entries["bf"].get())
            reels = int(self.entries["reels"].get())
            weight = float(self.entries["weight"].get())

            database.update_stock_by_id(self.selected_item_id, item_name, size, gsm, bf, reels, weight)
            messagebox.showinfo("Updated", "Stock entry updated successfully.")
            self.populate_table()
            self.clear_edit_fields()
            self.selected_item_id = None
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def delete_stock(self):
        if self.selected_item_id is None:
            messagebox.showwarning("No Selection", "Select a stock item to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this stock entry?")
        if confirm:
            database.delete_stock(self.selected_item_id)
            messagebox.showinfo("Deleted", "Stock entry deleted.")
            self.populate_table()
            self.clear_edit_fields()

    def clear_edit_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
