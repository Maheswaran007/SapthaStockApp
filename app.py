import tkinter as tk
from tkinter import ttk
from modules import database, add_stock, edit_stock, report

# === Initialize DB ===
database.init_db()

class StockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Saptha Printing & Packaging - Stock Manager")
        self.geometry("1000x600")
        self.resizable(False, False)

        self.configure(bg="white")
        self.sidebar = tk.Frame(self, width=200, bg="#2c3e50")
        self.sidebar.pack(side="left", fill="y")

        self.main_area = tk.Frame(self, bg="white")
        self.main_area.pack(side="right", fill="both", expand=True)

        self.create_sidebar()
        self.show_frame("home")

    def create_sidebar(self):
        buttons = [
            ("Home", lambda: self.show_frame("home")),
            ("Add Stock", lambda: self.show_frame("add")),
            ("Edit Stock", lambda: self.show_frame("edit")),
            ("Report", lambda: self.show_frame("report")),
            ("Exit", self.quit)
        ]

        for text, command in buttons:
            b = tk.Button(self.sidebar, text=text, command=command,
                          bg="#34495e", fg="white", relief="flat",
                          padx=10, pady=10, font=("Arial", 12))
            b.pack(fill="x", pady=2)

    def show_frame(self, page):
        for widget in self.main_area.winfo_children():
            widget.destroy()

        if page == "home":
            frame = tk.Frame(self.main_area, bg="white")
            tk.Label(frame, text="Saptha Printing & Packaging",
                     font=("Arial", 24, "bold"), bg="white", fg="#2c3e50").pack(expand=True)
        elif page == "add":
            frame = add_stock.AddStockFrame(self.main_area)
        elif page == "edit":
            frame = edit_stock.EditStockFrame(self.main_area)
        elif page == "report":
            frame = report.ReportFrame(self.main_area)
        else:
            frame = tk.Label(self.main_area, text="Page not found.")

        frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = StockApp()
    app.mainloop()
