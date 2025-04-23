import tkinter as tk
from tkinter import ttk, messagebox
from db import add_income, get_income, delete_income
from datetime import datetime

class IncomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#d0f0fd")  
        self.controller = controller
        self.user_id = controller.current_user[0]

        self.title_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))

        self.month_var = tk.StringVar(value="All")
        self.year_var = tk.StringVar(value=str(datetime.now().year))

        self.create_widgets()
        self.load_incomes()

    def create_widgets(self):
        tk.Label(
            self, text="💰 Income Tracker",
            font=("Segoe UI", 22, "bold"),
            bg="#d0f0fd", fg="#2c3e50"
        ).pack(pady=(20, 10))

        form_frame = tk.Frame(self, bg="#d0f0fd")
        form_frame.pack(pady=10)

        style = {"bg": "#d0f0fd", "font": ("Segoe UI", 10)}
        entry_style = {"width": 18, "font": ("Segoe UI", 10)}

        tk.Label(form_frame, text="Title:", **style).grid(row=0, column=0, padx=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.title_var, **entry_style).grid(row=0, column=1, padx=5)

        tk.Label(form_frame, text="Amount:", **style).grid(row=0, column=2, padx=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.amount_var, **entry_style).grid(row=0, column=3, padx=5)

        tk.Label(form_frame, text="Category:", **style).grid(row=0, column=4, padx=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.category_var, **entry_style).grid(row=0, column=5, padx=5)

        tk.Label(form_frame, text="Date:", **style).grid(row=0, column=6, padx=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.date_var, **entry_style).grid(row=0, column=7, padx=5)

        tk.Button(
            self,
            text="➕ Add Income",
            command=self.handle_add_income,
            bg="#2ecc71", fg="white", font=("Segoe UI", 10, "bold"),
            width=20
        ).pack(pady=15)

        filter_frame = tk.Frame(self, bg=self["bg"])
        filter_frame.pack(pady=(5, 0))

        months = ["All"] + [str(i) for i in range(1, 13)]
        years = [str(y) for y in range(2020, datetime.now().year + 1)]

        tk.Label(filter_frame, text="Month:", bg=self["bg"]).pack(side="left", padx=5)
        ttk.Combobox(filter_frame, textvariable=self.month_var, values=months, width=6).pack(side="left")

        tk.Label(filter_frame, text="Year:", bg=self["bg"]).pack(side="left", padx=5)
        ttk.Combobox(filter_frame, textvariable=self.year_var, values=years, width=8).pack(side="left")

        tk.Button(filter_frame, text="Apply Filter", command=self.load_incomes).pack(side="left", padx=10)

        self.table = ttk.Treeview(self, columns=("Title", "Amount", "Category", "Date", "ID"), show="headings")
        for col in ("Title", "Amount", "Category", "Date", "ID"):
            self.table.heading(col, text=col)
        self.table.column("ID", width=0, stretch=False)
        self.table.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Button(
            self,
            text="🗑️ Delete Selected",
            command=self.handle_delete_income,
            bg="#e74c3c", fg="white", font=("Segoe UI", 10, "bold"),
            width=20
        ).pack(pady=(10, 20))

    def load_incomes(self):
        for row in self.table.get_children():
            self.table.delete(row)
        incomes = get_income(self.user_id)
        month_filter = self.month_var.get()
        year_filter = self.year_var.get()

        for i in incomes:
            try:
                date_obj = datetime.strptime(i[5], "%Y-%m-%d")
                if (month_filter == "All" or date_obj.month == int(month_filter)) and date_obj.year == int(year_filter):
                    self.table.insert("", "end", values=(i[2], i[3], i[4], i[5], i[0]))
            except Exception:
                continue

    def handle_add_income(self):
        title = self.title_var.get()
        category = self.category_var.get()
        date = self.date_var.get()
        try:
            amount = float(self.amount_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
            return

        if not (title and category and date):
            messagebox.showerror("Error", "All fields are required.")
            return

        add_income(self.user_id, title, amount, category, date)
        self.load_incomes()
        self.title_var.set("")
        self.amount_var.set("")
        self.category_var.set("")
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))

    def handle_delete_income(self):
        selected = self.table.selection()
        if not selected:
            return
        income_id = self.table.item(selected[0])["values"][4]
        delete_income(income_id)
        self.load_incomes()
