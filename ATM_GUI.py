import tkinter as tk
import ttkbootstrap as ttk
from ATM_DB_Manager import ATM_Manager as ATM_DB

class ATM_GUI(ttk.Window):
    def __init__(self, title, size, theme):
        super().__init__(title=title, size=size, themename=theme)
        atm_db = ATM_DB()

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


        return title_frame

class infoFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=1, column=0, sticky="ew",)

        # Widgets
        self.create_welcome().pack(side="top",padx=20,pady=10, anchor='w')
        self.create_balance().pack(side="top",padx=20,pady=10, anchor='w')
        self.create_acc_type().pack(side="top",padx=20,pady=10, anchor='w')
    
    def create_welcome(self):
        welcome_frame = ttk.Frame(self)
        welcome_label = ttk.Label(welcome_frame, text="Welcome", font=("Arial", 15), bootstyle='primary')
        welcome_label.pack(side="top",anchor='w')

        self.user_var = tk.StringVar(value="User")
        user_label = ttk.Label(welcome_frame, text=self.user_var.get(), font=("Berlin Sans FB Demi", 20, 'bold'))
        user_label.pack(side="top",anchor='w')

        return welcome_frame
    
    def create_balance(self):
        balance_frame = ttk.Frame(self)
        balance_label = ttk.Label(balance_frame, text="Balance", font=("Arial", 15), bootstyle='primary') 
        balance_label.pack(side="top",anchor='w')

        self.balance_var = tk.StringVar(value="0.00")
        balance_label = ttk.Label(balance_frame, text=f"\u20b1{self.balance_var.get()}", font=("Berlin Sans FB Demi", 20, 'bold'))
        balance_label.pack(side="top",anchor='w')

        return balance_frame
    
    def create_acc_type(self):
        acc_type_frame = ttk.Frame(self)
        acc_type_label = ttk.Label(acc_type_frame, text="Account Type", font=("Arial", 15), bootstyle='primary')
        acc_type_label.pack(side="top",anchor='w')

        acc_type_var = tk.StringVar(value="None")
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
            command=lambda : print("Deposit Clicked"),
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
            command=lambda : print("Logout Clicked"),
            width=10
            )
        self.logout_button.grid(row=1, column=1, sticky="nsew", padx=10, pady=10,ipady=10)



if __name__ == "__main__":
    ATM_GUI("ATM", (720, 470), "atm_theme")
