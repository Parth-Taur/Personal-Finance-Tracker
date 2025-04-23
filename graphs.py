import tkinter as tk
from tkinter import ttk
from db import get_expenses, get_savings
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict

class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller
        self.user_id = controller.current_user[0]

        self.year_var = tk.StringVar(value=str(datetime.now().year))
        self.month_var = tk.StringVar(value="All")

        self.create_widgets()
        self.draw_graph()

    def create_widgets(self):
        filter_frame = tk.Frame(self, bg="#ffffff")
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Year:", bg="#ffffff").grid(row=0, column=0)
        tk.Entry(filter_frame, textvariable=self.year_var, width=10).grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Month:", bg="#ffffff").grid(row=0, column=2)
        month_options = ["All"] + [str(m) for m in range(1, 13)]
        ttk.Combobox(filter_frame, textvariable=self.month_var, values=month_options, width=10).grid(row=0, column=3, padx=5)

        tk.Button(filter_frame, text="Update Graph", command=self.draw_graph, bg="#2c3e50", fg="white").grid(row=0, column=4, padx=10)

        self.graph_frame = tk.Frame(self, bg="#ffffff")
        self.graph_frame.pack(fill="both", expand=True)

    def draw_graph(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        year = int(self.year_var.get())
        month_filter = self.month_var.get()

        expenses = get_expenses(self.user_id)
        savings = get_savings(self.user_id)

        monthly_data = defaultdict(lambda: {"expenses": 0, "savings": 0})

        for e in expenses:
            date = datetime.strptime(e[5], "%Y-%m-%d")
            if date.year == year and (month_filter == "All" or date.month == int(month_filter)):
                key = f"{date.month}/{date.year}"
                monthly_data[key]["expenses"] += e[3]

        for s in savings:
            date = datetime.strptime(s[3], "%Y-%m-%d")
            if date.year == year and (month_filter == "All" or date.month == int(month_filter)):
                key = f"{date.month}/{date.year}"
                monthly_data[key]["savings"] += s[2]

        months = sorted(monthly_data.keys(), key=lambda d: datetime.strptime(d, "%m/%Y"))
        expenses_vals = [monthly_data[m]["expenses"] for m in months]
        savings_vals = [monthly_data[m]["savings"] for m in months]

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(months, expenses_vals, label="Expenses", color="#e74c3c", marker='o')
        ax.plot(months, savings_vals, label="Savings", color="#27ae60", marker='o')

        ax.set_title("Monthly Expenses vs Savings")
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
