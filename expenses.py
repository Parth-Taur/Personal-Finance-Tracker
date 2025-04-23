import tkinter as tk
from tkinter import ttk, messagebox
from db import add_expense, get_expenses, delete_expense
from datetime import datetime

class ExpensesPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fdf6f6")
        self.controller = controller
        self.user_id = controller.current_user[0]

        self.title_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))

        self.month_var = tk.StringVar(value="All")
        self.year_var = tk.StringVar(value=str(datetime.now().year))

        self.create_widgets()
        self.load_expenses()

    def create_widgets(self):
        tk.Label(self, text="Expenses", font=("Arial", 20, "bold"), bg="#fdf6f6").pack(pady=10)

        form_frame = tk.Frame(self, bg="#fdf6f6")
        form_frame.pack(pady=5)

        tk.Label(form_frame, text="Title:", bg="#fdf6f6").grid(row=0, column=0, sticky="e")
        tk.Entry(form_frame, textvariable=self.title_var, width=20).grid(row=0, column=1)

        tk.Label(form_frame, text="Amount:", bg="#fdf6f6").grid(row=0, column=2, sticky="e")
        tk.Entry(form_frame, textvariable=self.amount_var, width=20).grid(row=0, column=3)

        tk.Label(form_frame, text="Category:", bg="#fdf6f6").grid(row=1, column=0, sticky="e")
        tk.Entry(form_frame, textvariable=self.category_var, width=20).grid(row=1, column=1)

        tk.Label(form_frame, text="Date (YYYY-MM-DD):", bg="#fdf6f6").grid(row=1, column=2, sticky="e")
        tk.Entry(form_frame, textvariable=self.date_var, width=20).grid(row=1, column=3)

        tk.Button(self, text="Add Expense", command=self.handle_add_expense, bg="#e67e22", fg="white", width=20).pack(pady=10)

        filter_frame = tk.Frame(self, bg=self["bg"])
        filter_frame.pack(pady=(5, 0))

        months = ["All"] + [str(i) for i in range(1, 13)]
        years = [str(y) for y in range(2020, datetime.now().year + 1)]

        tk.Label(filter_frame, text="Month:", bg=self["bg"]).pack(side="left", padx=5)
        ttk.Combobox(filter_frame, textvariable=self.month_var, values=months, width=6).pack(side="left")

        tk.Label(filter_frame, text="Year:", bg=self["bg"]).pack(side="left", padx=5)
        ttk.Combobox(filter_frame, textvariable=self.year_var, values=years, width=8).pack(side="left")

        tk.Button(filter_frame, text="Apply Filter", command=self.load_expenses).pack(side="left", padx=10)

        # Table
        self.table = ttk.Treeview(self, columns=("Title", "Amount", "Category", "Date", "ID"), show="headings")
        for col in ("Title", "Amount", "Category", "Date", "ID"):
            self.table.heading(col, text=col)
        self.table.column("ID", width=0, stretch=False)
        self.table.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Button(self, text="Delete Selected", command=self.handle_delete_expense, bg="#c0392b", fg="white", width=20).pack(pady=10)

    def load_expenses(self):
        for row in self.table.get_children():
            self.table.delete(row)
        expenses = get_expenses(self.user_id)
        month_filter = self.month_var.get()
        year_filter = self.year_var.get()

        for e in expenses:
            try:
                date_obj = datetime.strptime(e[5], "%Y-%m-%d")
                if (month_filter == "All" or date_obj.month == int(month_filter)) and date_obj.year == int(year_filter):
                    self.table.insert("", "end", values=(e[2], e[3], e[4], e[5], e[0]))
            except Exception:
                continue

    def handle_add_expense(self):
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

        add_expense(self.user_id, title, amount, category, date)
        self.load_expenses()
        self.title_var.set("")
        self.amount_var.set("")
        self.category_var.set("")
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))

    def handle_delete_expense(self):
        selected = self.table.selection()
        if not selected:
            return
        expense_id = self.table.item(selected[0])["values"][4]
        delete_expense(expense_id)
        self.load_expenses()
