import tkinter as tk
import ttkbootstrap as ttk
from ATM_DB_Manager import ATM_Manager as ATM_DB
from tkinter import messagebox as msg

class ATM_GUI(ttk.Window):
    def __init__(self, title, size, theme, acc_no):
        super().__init__(title=title, size=size, themename=theme)
        self.atm_db = ATM_DB()
        self.acc_no = acc_no
        self.userID = self.atm_db.view_account(self.acc_no)[2]
        
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 15, 'bold'))
        self.resizable(False, False)

        # Configure 2x2 grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)

        self.create_title_banner()
        self.info_frame = infoFrame(self)
        self.options_frame = OptionsFrame(self)

        self.mainloop()

    
    def create_title_banner(self):
        """Creates the image banner at the top of the window"""
        # Image
        logo_frame = ttk.Frame(self)
        logo_image = tk.PhotoImage(file="Media/Lion_Icon.png")
        # Resize
        logo_image = logo_image.subsample(2,2)
        logo_label = ttk.Label(logo_frame, image=logo_image)
        logo_label.image = logo_image
        logo_label.pack(side="top", anchor='center')
        logo_frame.grid(row=0, column=0, sticky="ew")
        

        # Image
        title_frame = ttk.Frame(self)
        title_image = tk.PhotoImage(file="Media/Golden_Mane_Title.png")
        # Resize
        title_image = title_image.subsample(2,2)
        title_label = ttk.Label(title_frame, image=title_image)
        title_label.image = title_image
        title_label.pack(side="top", anchor='center')
        title_frame.grid(row=0, column=1, sticky="ew")


class infoFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=1, column=0, sticky="ew",)

        self.balance_var = tk.StringVar(value=f"\u20b1{self.master.atm_db.view_balance(self.master.acc_no)}")

        # Widgets
        self.create_welcome().pack(side="top",padx=20,pady=10, anchor='w')
        self.create_balance().pack(side="top",padx=20,pady=10, anchor='w')
        self.create_acc_type().pack(side="top",padx=20,pady=10, anchor='w')
        self.refresh_button = ttk.Button(self,text="Refresh", command=self.refresh).pack(side="top",padx=20,pady=10, anchor='w')

    def refresh(self):
        self.balance_var.set(f"\u20b1{self.master.atm_db.view_balance(self.master.acc_no)}")

    def create_welcome(self):
        welcome_frame = ttk.Frame(self)
        welcome_label = ttk.Label(welcome_frame, text="Welcome", font=("Arial", 15), bootstyle='primary')
        welcome_label.pack(side="top",anchor='w')

        self.user_var = tk.StringVar(value=self.master.atm_db.view_user(f'"{self.master.userID}"')[2])
        user_label = ttk.Label(welcome_frame, text=self.user_var.get(), font=("Berlin Sans FB Demi", 20, 'bold'))
        user_label.pack(side="top",anchor='w')

        return welcome_frame
    
    def create_balance(self):
        balance_frame = ttk.Frame(self)
        balance_labels = ttk.Label(balance_frame, text="Balance", font=("Arial", 15), bootstyle='primary') 
        balance_labels.pack(side="top",anchor='w')

        self.balance_label = ttk.Label(balance_frame, font=("Berlin Sans FB Demi", 20, 'bold'),textvariable=self.balance_var)
        self.balance_label.pack(side="top",anchor='w')

        return balance_frame
    
    def create_acc_type(self):
        acc_type_frame = ttk.Frame(self)
        acc_type_label = ttk.Label(acc_type_frame, text="Account Type", font=("Arial", 15), bootstyle='primary')
        acc_type_label.pack(side="top",anchor='w')

        acc_type_var = tk.StringVar(value=self.master.atm_db.view_account(self.master.acc_no)[1])
        acc_type_label = ttk.Label(acc_type_frame, text=acc_type_var.get(), font=("Berlin Sans FB Demi", 20, 'bold'))
        acc_type_label.pack(side="top",anchor='w')

        return acc_type_frame


class OptionsFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=1, column=1, sticky="nsew", padx=20)

        # Configure a 2x2 grid
        self.frame = ttk.Frame(self,)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.pack(side="top", padx=10, pady=10, anchor='center', fill='x', expand=True)


        # Buttons - Deposit, Withdraw, View Transactions, Logout
        self.deposit_button = ttk.Button(
            self.frame, text="Deposit",
            bootstyle="primary",
            command= lambda: Deposit_Window(master=self.master),
            width=10,
            )
        self.deposit_button.grid(row=0, column=0, sticky="nsew", padx=10, pady=10,ipady=20)

        self.withdraw_button = ttk.Button(
            self.frame, text="Withdraw",
            bootstyle="primary",
            command=lambda : print("Withdraw Clicked"),
            width=10,
            )
        self.withdraw_button.grid(row=0, column=1, sticky="nsew", padx=10, pady=10,ipady=20)

        self.transactions_button = ttk.Button(
            self.frame, text="View Transactions",
            bootstyle="primary",
            command=lambda : print("View Transactions Clicked"),
            width=10
            )
        self.transactions_button.grid(row=1, column=0, sticky="nsew", padx=10, pady=10,ipady=20)
        
        self.logout_button = ttk.Button(
            self.frame, text="Logout",
            bootstyle="danger",
            command= self.master.destroy,
            width=10
            )
        self.logout_button.grid(row=1, column=1, sticky="nsew", padx=10, pady=10,ipady=10)


class Deposit_Window(ttk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Deposit")
        self.geometry("300x500")
        self.resizable(False, False)

        # Title label
        self.label = ttk.Label(
            self,
            text="Enter Amount to Deposit",
            font=("Arial", 15, 'bold'),
            bootstyle='primary'
            )
        self.label.pack(side="top", padx=10, pady=10, anchor='center')

        # Create frame
        self.frame = ttk.Frame(self)
        self.frame.pack(side="top", padx=10, anchor='center', fill='both', expand=True)

        # Configure a 3x5 grid
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.rowconfigure(0, weight=2)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.rowconfigure(4, weight=1)

        # Create widgets
        self.create_widgets()

        # loop
        self.mainloop()
    
    def create_widgets(self):
        # entry widget and variable
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(
            self.frame,
            textvariable=self.entry_var,
            font=("Berlin Sans FB Demi", 15, 'bold'),
            justify="center"
            )
        self.entry.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10,ipady=10)

        # number buttons
        self.num_1 = ttk.Button(
            self.frame, text="1",
            bootstyle="primary",
            command=lambda : self.entry_var.set(self.entry_var.get() + "1"),
            width=10,
            )
        self.num_1.grid(row=1, column=0, sticky="nsew", padx=10, pady=10,ipady=10)

        self.num_2 = ttk.Button(
            self.frame, text="2",
            bootstyle="primary",
            command=lambda : self.entry_var.set(self.entry_var.get() + "2"),
            width=10,
            )
        self.num_2.grid(row=1, column=1, sticky="nsew", padx=10, pady=10,ipady=10)

        self.num_3 = ttk.Button(
            self.frame, text="3",
            bootstyle="primary",
            command=lambda : self.entry_var.set(self.entry_var.get() + "3"),
            width=10,
            )
        self.num_3.grid(row=1, column=2, sticky="nsew", padx=10, pady=10,ipady=10)

        self.num_4 = ttk.Button(
            self.frame, text="4",
            bootstyle="primary",
            command=lambda : self.entry_var.set(self.entry_var.get() + "4"),
            width=10,
            )
        self.num_4.grid(row=2, column=0, sticky="nsew", padx=10, pady=10,ipady=10)

        self.num_5 = ttk.Button(
            self.frame, text="5",
            bootstyle="primary",
            command=lambda : self.entry_var.set(self.entry_var.get() + "5"),
            width=10,
            )
        self.num_5.grid(row=2, column=1, sticky="nsew", padx=10, pady=10,ipady=10)

        self.num_6 = ttk.Button(
            self.frame, text="6",
            bootstyle="primary",
            command=lambda : self.entry_var.set(self.entry_var.get() + "6"),
            width=10,
            )
        self.num_6.grid(row=2, column=2, sticky="nsew", padx=10, pady=10,ipady=10)

        self.num_7 = ttk.Button(
            self.frame, text="7",
            bootstyle="primary",
            command=lambda : self.entry_var.set(self.entry_var.get() + "7"),
            width=10,
            )
        self.num_7.grid(row=3, column=0, sticky="nsew", padx=10, pady=10,ipady=10)

        self.num_8 = ttk.Button(
            self.frame, text="8",
            bootstyle="primary",
            command=lambda : self.entry_var.set(self.entry_var.get() + "8"),
            width=10,
            )
        self.num_8.grid(row=3, column=1, sticky="nsew", padx=10, pady=10,ipady=10)

        self.num_9 = ttk.Button(
            self.frame, text="9",
            bootstyle="primary",
            command=lambda : self.entry_var.set(self.entry_var.get() + "9"),
            width=10,
            )
        self.num_9.grid(row=3, column=2, sticky="nsew", padx=10, pady=10,ipady=10)

        self.num_0 = ttk.Button(
            self.frame, text="0",
            bootstyle="primary",
            command=lambda : self.entry_var.set(self.entry_var.get() + "0"),
            width=10,
            )
        self.num_0.grid(row=4, column=1, sticky="nsew", padx=10, pady=10,ipady=10)

        # submit button
        self.submit = ttk.Button(
            self.frame, text="\u2713",
            bootstyle="success",
            command= lambda: self.submit_func(self.master.acc_no, self.entry_var.get()),
            width=10,
            )
        self.submit.grid(row=4, column=0, sticky="nsew", padx=10, pady=10,ipady=10)

        # cancel button
        self.cancel = ttk.Button(
            self.frame, text="X",
            bootstyle="danger",
            command=lambda: self.destroy(),
            width=10,
            )
        self.cancel.grid(row=4, column=2, sticky="nsew", padx=10, pady=10,ipady=10)

    def submit_func(self, account_number, amount):
        # Call the deposit method of the atm_db
        self.master.atm_db.deposit(account_number, amount)
        
        # Clear the entry widget
        self.entry_var.set("")

        # create an ok message box
        msg.showinfo("Deposit Successful", f"Your new balance is:\n\u20b1{self.master.atm_db.view_balance(account_number)}")

        # change the balance in the ATM_GUI
        self.master.info_frame.create_balance()

        
if __name__ == "__main__":
    ATM_GUI("ATM", (720, 500), "atm_theme", "1")
