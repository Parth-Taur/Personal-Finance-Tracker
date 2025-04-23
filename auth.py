import tkinter as tk
from tkinter import messagebox
from db import login_user, register_user

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Login", font=("Arial", 24), bg="white").pack(pady=20)

        form = tk.Frame(self, bg="white")
        form.pack()

        tk.Label(form, text="Email", bg="white").grid(row=0, column=0, pady=5, sticky="e")
        tk.Entry(form, textvariable=self.email_var, width=30).grid(row=0, column=1)

        tk.Label(form, text="Password", bg="white").grid(row=1, column=0, pady=5, sticky="e")
        tk.Entry(form, textvariable=self.password_var, show="*", width=30).grid(row=1, column=1)

        tk.Button(self, text="Login", command=self.handle_login, bg="#3498db", fg="white", width=15).pack(pady=10)
        tk.Button(self, text="Sign Up", command=self.show_signup, width=15).pack()

    def handle_login(self):
        email = self.email_var.get()
        password = self.password_var.get()
        user = login_user(email, password)
        if user:
            self.controller.login_success(user)
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")

    def show_signup(self):
        for widget in self.winfo_children():
            widget.destroy()
        SignUpPage(self, self.controller).pack(fill="both", expand=True)

class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        self.username_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Sign Up", font=("Arial", 24), bg="white").pack(pady=20)

        form = tk.Frame(self, bg="white")
        form.pack()

        tk.Label(form, text="Username", bg="white").grid(row=0, column=0, pady=5, sticky="e")
        tk.Entry(form, textvariable=self.username_var, width=30).grid(row=0, column=1)

        tk.Label(form, text="Email", bg="white").grid(row=1, column=0, pady=5, sticky="e")
        tk.Entry(form, textvariable=self.email_var, width=30).grid(row=1, column=1)

        tk.Label(form, text="Password", bg="white").grid(row=2, column=0, pady=5, sticky="e")
        tk.Entry(form, textvariable=self.password_var, show="*", width=30).grid(row=2, column=1)

        tk.Button(self, text="Create Account", command=self.handle_signup, bg="#2ecc71", fg="white", width=15).pack(pady=10)
        tk.Button(self, text="Back to Login", command=self.back_to_login, width=15).pack()

    def handle_signup(self):
        username = self.username_var.get()
        email = self.email_var.get()
        password = self.password_var.get()
        success = register_user(username, email, password)
        if success:
            messagebox.showinfo("Success", "Account created! You can now log in.")
            self.back_to_login()
        else:
            messagebox.showerror("Error", "Email already exists.")

    def back_to_login(self):
        for widget in self.winfo_children():
            widget.destroy()
        LoginPage(self.master, self.controller).pack(fill="both", expand=True)
