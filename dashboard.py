import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
from db import get_income, get_expenses, get_savings
from utils import format_currency

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#e8f5e9")  # Soft green background
        self.controller = controller
        self.user_id = controller.current_user[0]

        self.now = datetime.now()
        self.current_year = self.now.year
        self.current_month = self.now.month

        self.bg_canvas = tk.Canvas(self, width=1000, height=600, bg="#e8f5e9", highlightthickness=0)
        self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.load_background_image()
        self.create_sidebar()
        self.create_widgets()
        self.animate_title()

    def load_background_image(self):
        try:
            bg_image = Image.open("finance_tracker.png").resize((300, 300))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            self.bg_canvas.create_image(600, 150, anchor="center", image=self.bg_image)
        except Exception as e:
            print("Background image load failed:", e)

    def animate_title(self):
        # Floating animation for dashboard title
        def float_text():
            nonlocal dy, y_pos
            y_pos += dy
            if y_pos > 85 or y_pos < 75:
                dy *= -1
            self.bg_canvas.coords(self.title_id, 180, y_pos)
            self.after(50, float_text)

        y_pos = 80
        dy = 1
        self.title_id = self.bg_canvas.create_text(
            180, y_pos,
            text="📊 Dashboard",
            font=("Segoe UI", 26, "bold"),
            fill="#1b5e20"
        )
        float_text()

    def create_sidebar(self):
        if hasattr(self.controller, 'sidebar'):
            self.controller.sidebar.configure(bg="#2e7d32")  # Dark green
            for child in self.controller.sidebar.winfo_children():
                try:
                    child.configure(bg="#2e7d32", fg="white")
                except:
                    pass

    def create_widgets(self):
        cards_frame = tk.Frame(self.bg_canvas, bg="#e8f5e9")
        cards_frame.place(x=50, y=150)

        income = get_income(self.user_id)
        expenses = get_expenses(self.user_id)
        savings = get_savings(self.user_id)

        total_income = sum(i[3] for i in income if self.in_current_month(i[5]))
        total_expense = sum(e[3] for e in expenses if self.in_current_month(e[5]))
        total_saving = sum(s[2] for s in savings if self.in_current_month(s[3]))
        remaining = total_income - total_expense - total_saving

        card_data = [
            ("Income", format_currency(total_income), "#81c784"),   # light green
            ("Expenses", format_currency(total_expense), "#e57373"), # red
            ("Savings", format_currency(total_saving), "#64b5f6"),   # blue
            ("Remaining", format_currency(remaining), "#ffd54f")     # yellow
        ]

        for idx, (title, value, color) in enumerate(card_data):
            self.create_rectangle_card(cards_frame, title, value, color, idx)

    def create_rectangle_card(self, parent, title, value, color, col):
        canvas = tk.Canvas(parent, width=200, height=120, bg="#e8f5e9", highlightthickness=0)
        canvas.grid(row=0, column=col, padx=20, pady=20)

        rect = canvas.create_rectangle(10, 10, 190, 110, fill=color, outline=color, width=2)
        canvas.create_text(100, 45, text=title, font=("Segoe UI", 14, "bold"), fill="white")
        canvas.create_text(100, 80, text=value, font=("Segoe UI", 16, "bold"), fill="white")

        def on_enter(event):
            canvas.itemconfig(rect, fill=self.shade_color(color, 0.9), outline=self.shade_color(color, 0.9))
        def on_leave(event):
            canvas.itemconfig(rect, fill=color, outline=color)

        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)

    def in_current_month(self, date_str):
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            return date.year == self.current_year and date.month == self.current_month
        except:
            return False

    def shade_color(self, color, factor):
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        lighter = tuple(min(255, int(c + (255 - c) * (1 - factor))) for c in rgb)
        return '#%02x%02x%02x' % lighter
