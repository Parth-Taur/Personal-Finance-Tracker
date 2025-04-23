import tkinter as tk
from auth import LoginPage
from dashboard import DashboardPage
from income import IncomePage
from expenses import ExpensesPage
from savings import SavingsPage
from graphs import GraphPage
from profile import ProfilePage
from db import init_db

class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance Tracker")
        self.geometry("1200x700")
        self.resizable(True, True)
        self.current_user = None

        self.sidebar_frame = None
        self.main_frame = None

        self.create_widgets()

    def create_widgets(self):
        self.sidebar_frame = tk.Frame(self, bg="#2c3e50", width=200)
        self.sidebar_frame.pack(side="left", fill="y")

        self.main_frame = tk.Frame(self, bg="#ecf0f1")
        self.main_frame.pack(side="right", fill="both", expand=True)

        self.show_login()

    def show_login(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        LoginPage(self.main_frame, self).pack(fill="both", expand=True)

    def login_success(self, user_data):
        self.current_user = user_data
        self.build_sidebar()
        self.show_dashboard()

    def logout(self):
        self.current_user = None
        self.sidebar_frame.destroy()
        self.sidebar_frame = tk.Frame(self, bg="#2c3e50", width=200)
        self.sidebar_frame.pack(side="left", fill="y")
        self.show_login()

    def build_sidebar(self):
        for widget in self.sidebar_frame.winfo_children():
            widget.destroy()

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Income", self.show_income),
            ("Expenses", self.show_expenses),
            ("Savings", self.show_savings),
            ("Graphs", self.show_graphs),
            ("Profile", self.show_profile),
            ("Log Out", self.logout),
        ]

        for text, command in buttons:
            btn = tk.Button(
                self.sidebar_frame, text=text, bg="#34495e", fg="white",
                font=("Arial", 12), relief="flat", height=2, command=command
            )
            btn.pack(fill="x", pady=2)

    def show_dashboard(self):
        self.load_page(DashboardPage)

    def show_income(self):
        self.load_page(IncomePage)

    def show_expenses(self):
        self.load_page(ExpensesPage)

    def show_savings(self):
        self.load_page(SavingsPage)

    def show_profile(self):
        self.load_page(ProfilePage)

    def show_graphs(self):
        self.load_page(GraphPage)

    def load_page(self, PageClass):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        page = PageClass(self.main_frame, self)
        page.pack(fill="both", expand=True)

if __name__ == "__main__":
    init_db()
    app = FinanceApp()
    app.mainloop()
