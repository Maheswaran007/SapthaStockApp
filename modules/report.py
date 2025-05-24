import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from openpyxl import Workbook
from modules import database

class ReportFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.data = []
        self.build_ui()
        self.load_data()

    def build_ui(self):
        columns = ["Item", "Size", "GSM", "BF", "Reels", "Weight"]
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill="x", padx=10, pady=10)

        tk.Button(self, text="Export to Excel", command=self.export_to_excel).pack(pady=10)

    def load_data(self):
        self.data = database.get_today_stock()
        for row in self.data:
            self.tree.insert("", "end", values=row)

    def export_to_excel(self):
        if not self.data:
            messagebox.showinfo("No Data", "No stock data to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            initialdir=os.path.abspath("exports"),
            title="Save Excel File"
        )
        if not file_path:
            return

        wb = Workbook()
        ws = wb.active
        ws.title = "TodayStock"

        headers = ["Item Name", "Size", "GSM", "BF", "No. of Reels", "Weight"]
        ws.append(headers)

        for row in self.data:
            ws.append(row)

        wb.save(file_path)
        messagebox.showinfo("Exported", f"Stock exported to:\n{file_path}")
