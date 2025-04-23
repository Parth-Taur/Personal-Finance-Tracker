import tkinter as tk
from tkinter import messagebox
from db import update_profile, delete_user

class ProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f7")
        self.controller = controller
        self.user_id = controller.current_user[0]

        self.username_var = tk.StringVar(value=controller.current_user[1])
        self.email_var = tk.StringVar(value=controller.current_user[2])
        self.password_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Profile", font=("Arial", 20, "bold"), bg="#f4f6f7").pack(pady=10)

        form_frame = tk.Frame(self, bg="#f4f6f7")
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Username:", bg="#f4f6f7").grid(row=0, column=0, sticky="e", pady=5)
        tk.Entry(form_frame, textvariable=self.username_var, width=30).grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Email:", bg="#f4f6f7").grid(row=1, column=0, sticky="e", pady=5)
        tk.Entry(form_frame, textvariable=self.email_var, width=30).grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="New Password:", bg="#f4f6f7").grid(row=2, column=0, sticky="e", pady=5)
        tk.Entry(form_frame, textvariable=self.password_var, width=30, show="*").grid(row=2, column=1, pady=5)

        tk.Button(self, text="Update Profile", command=self.update_profile, bg="#2980b9", fg="white", width=20).pack(pady=10)
        tk.Button(self, text="Delete Account", command=self.confirm_delete, bg="#c0392b", fg="white", width=20).pack(pady=5)
        tk.Button(self, text="Log Out", command=self.controller.logout, bg="#7f8c8d", fg="white", width=20).pack(pady=5)

    def update_profile(self):
        username = self.username_var.get()
        email = self.email_var.get()
        password = self.password_var.get()

        if not (username and email):
            messagebox.showerror("Error", "Username and Email are required.")
            return

        update_profile(self.user_id, username, email, password or self.controller.current_user[3])
        self.controller.current_user = (self.user_id, username, email, password or self.controller.current_user[3])
        messagebox.showinfo("Success", "Profile updated!")

    def confirm_delete(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete your account? This cannot be undone."):
            delete_user(self.user_id)
            messagebox.showinfo("Account Deleted", "Your account has been deleted.")
            self.controller.logout()
