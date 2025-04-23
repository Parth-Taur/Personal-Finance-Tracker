import tkinter as tk
from tkinter import ttk, messagebox
from db import add_saving, get_savings, delete_saving
from datetime import datetime

class SavingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0fff0")
        self.controller = controller
        self.user_id = controller.current_user[0]

        self.amount_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))

        self.month_var = tk.StringVar(value="All")
        self.year_var = tk.StringVar(value=str(datetime.now().year))

        self.create_widgets()
        self.load_savings()

    def create_widgets(self):
        tk.Label(self, text="Savings", font=("Arial", 20, "bold"), bg="#f0fff0").pack(pady=10)

        form_frame = tk.Frame(self, bg="#f0fff0")
        form_frame.pack(pady=5)

        tk.Label(form_frame, text="Amount:", bg="#f0fff0").grid(row=0, column=0, sticky="e")
        tk.Entry(form_frame, textvariable=self.amount_var, width=20).grid(row=0, column=1)

        tk.Label(form_frame, text="Date (YYYY-MM-DD):", bg="#f0fff0").grid(row=0, column=2, sticky="e")
        tk.Entry(form_frame, textvariable=self.date_var, width=20).grid(row=0, column=3)

        tk.Button(self, text="Add Saving", command=self.handle_add_saving, bg="#3498db", fg="white", width=20).pack(pady=10)

        filter_frame = tk.Frame(self, bg=self["bg"])
        filter_frame.pack(pady=(5, 0))

        months = ["All"] + [str(i) for i in range(1, 13)]
        years = [str(y) for y in range(2020, datetime.now().year + 1)]

        tk.Label(filter_frame, text="Month:", bg=self["bg"]).pack(side="left", padx=5)
        ttk.Combobox(filter_frame, textvariable=self.month_var, values=months, width=6).pack(side="left")

        tk.Label(filter_frame, text="Year:", bg=self["bg"]).pack(side="left", padx=5)
        ttk.Combobox(filter_frame, textvariable=self.year_var, values=years, width=8).pack(side="left")

        tk.Button(filter_frame, text="Apply Filter", command=self.load_savings).pack(side="left", padx=10)

        self.table = ttk.Treeview(self, columns=("Amount", "Date", "ID"), show="headings")
        self.table.heading("Amount", text="Amount")
        self.table.heading("Date", text="Date")
        self.table.heading("ID", text="ID")
        self.table.column("ID", width=0, stretch=False)
        self.table.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Button(self, text="Delete Selected", command=self.handle_delete_saving, bg="#c0392b", fg="white", width=20).pack(pady=10)

    def load_savings(self):
        for row in self.table.get_children():
            self.table.delete(row)
        savings = get_savings(self.user_id)
        month_filter = self.month_var.get()
        year_filter = self.year_var.get()

        for s in savings:
            try:
                date_obj = datetime.strptime(s[3], "%Y-%m-%d")
                if (month_filter == "All" or date_obj.month == int(month_filter)) and date_obj.year == int(year_filter):
                    self.table.insert("", "end", values=(s[2], s[3], s[0]))
            except Exception:
                continue

    def handle_add_saving(self):
        try:
            amount = float(self.amount_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
            return
        date = self.date_var.get()

        if not date:
            messagebox.showerror("Error", "Date is required.")
            return

        add_saving(self.user_id, amount, date)
        self.load_savings()
        self.amount_var.set("")
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))

    def handle_delete_saving(self):
        selected = self.table.selection()
        if not selected:
            return
        saving_id = self.table.item(selected[0])["values"][2]
        delete_saving(saving_id)
        self.load_savings()
