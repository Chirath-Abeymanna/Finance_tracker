import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *


# Creating a global dictionary to store transactions
transaction = {}

#NOTE: There are 3 global variables used in this system
        #Transaction : This variable is global dictionary that'll used to store all the transactions inside the application
        #temp_transaction : This is a copy of the transaction variable
        #view_transaction : This is the treeview table tha't the main table used to display transaction in the application

#file handling functions
class FileHandling():

    #Creating a function to load the transactions from the Json file
    @staticmethod
    def load_transaction():
        
        #Making the working_directory into a global variable
        global working_directory

        #changing the working directory
        working_directory = Path(__file__).absolute().parent
        try: 
            with open (working_directory /"data/transaction.json",'r') as file:
                json.load(file)
                return True
        except FileNotFoundError:
            messagebox.showerror("Error","The Json file is not found !!!!")
            
        except Exception as e:
            messagebox.showerror("Error",f"The following error occured {e}")

    #creating a function to save the transactions to the Json file
    @staticmethod
    def save_transaction():
        new_data = {}
        for key, values in transaction.items():
            transaction_type = values['type']
            transaction_data = {
                "Category": values['category'],
                "Date": values['date'],
                "Amount": values['amount'],
                "id": key
            }
            if transaction_type in new_data:
                new_data[transaction_type].append(transaction_data)
            else:
                new_data[transaction_type] = [transaction_data]

        with open(working_directory /"data/transaction.json", 'w') as file:
            json.dump(new_data, file)

    #Reading the json file line by line
    @staticmethod
    def bulk_reading(filename):

        #making global variables
        global transaction, temp_transaction

        temp_transaction = transaction
        
        with open (filename,'r') as file:
                for line in file:
                    data = json.loads(line)

                    for key, values in data.items():
        
                        for item in values:
                            if isinstance(item, dict):  # Check if item is a dictionary

                                # Extracting necessary information from the JSON data
                                t_type = key
                                t_category = item["Category"]
                                t_date = item["Date"]
                                t_amount = item["Amount"]
                                t_id = item['id']

                                #Adding each values to the transaction dictionary
                                transaction_details ={'category':t_category,'type':t_type,'date':t_date,'amount':t_amount}
                                transaction[t_id] = transaction_details

                            elif isinstance(item, list):  # Check if item is a list
                                for sub_item in item:

                                    # Extracting necessary information from the JSON data
                                    t_type = key
                                    t_category = sub_item["Category"]
                                    t_date = sub_item["Date"]
                                    t_amount = sub_item["amount"]
                                    t_id = item['id'] 

                                    #Adding each values to the transaction dictionary
                                    transaction_details ={'category':t_category,'type':t_type,'date':t_date,'amount':t_amount}
                                    transaction[t_id] = transaction_details

        #sorting the transaction dictionary according to the id numbers
        s_transaction = dict(sorted(transaction.items()))
        transaction = s_transaction

#main class
class FinanceTrackerGUI(tk.Tk):
    def __init__(self):

        super().__init__()

        
        # Creating the window main properties
        self.title("Personal Finance Tracker")
        try:
                self.iconbitmap(working_directory /"ico/title.ico")
        except:
            messagebox.showerror("Icon error","Neccessary Icon wasn't loaded successfully")
        
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.geometry(f"{screen_width}x{screen_height}+0+0")

        #create style widgets
        self.style()

        # Widgets
        self.upper = UpperMenuFrame(self)
        self.view = ViewTransactionFrame(self)
        self.menu = LowerMenuFrame(self)
        self.summary = ViewSummaryFrame(self)
        

        # Run the program
        self.mainloop()
    
    def style(self):
        # Create style widgets
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure('TFrame', background='white', borderwidth=0)

        #create a style for sort by button
        self.style.configure('sort.TMenubutton',
                     menu="sort.TMenu",  # Set the menu style 
                     foreground="white",
                     background="#004aad",
                     font=("Helvetica", 10),
                     padding=(10, 10),
                     borderwidth=0,
                     highlightthickness=0,
                     width = 20,
                     relief = 'flat'
                     
                     )
        self.style.map("sort.TMenubutton", background=[('active', '#2a53db')])

        #create a style for date-month
        self.style.configure('category.TMenubutton',
                     menu="sort.TMenu",  # Set the menu style 
                     foreground="white",
                     background="#0927eb",
                     font=("Helvetica", 10),
                     padding=(10, 4),
                     width = 9,
                     relief = 'flat'
                     
                     )
        self.style.map("category.TMenubutton", background=[('active', '#2a53db')])

        #Create a style for main buttons
        self.style.configure('blue.TButton',
                             foreground="white",
                             background="#004aad",
                             font=("Helvetica", 10),
                             padding=(10, 10, 10, 10),
                             borderwidth=0,
                             width = 19
                             )
        
        #Create a style for search button
        self.style.configure('search.TButton',
                             foreground="white",
                             background="#004aad",
                             font=("Helvetica", 10),
                             padding=(10, 10, 10, 10),
                             borderwidth=0,
                             width = 12
                             )
        self.style.map("blue.TButton", background=[('active', '#0927eb')])
        self.style.map("search.TButton", background=[('active', '#0927eb')])

        #Styling the labels
        self.style.configure("menu.TLabel",
                            background="#5271ff",
                            foreground="white",
                            font=("Helvetica", 15),
                            width=10,
                            anchor='center',
                            bordercolor = "grey",
                            borderwidth = 1,
                            relief = "solid"
                            )

        self.style.configure("normal.TLabel",
                            background="white",
                            foreground="black",
                            font=("Helvetica", 11),
                            padding=(3, 3),
                            width=10,
                            anchor='center',
                            bordercolor = "grey",
                            borderwidth = 1,
                            relief = "solid"
                            )
        
        self.style.configure("border.TLabel",
                            background="white",
                            foreground="white",
                            font=("Helvetica", 11),
                            padding=(3, 67),
                            width=10,
                            anchor='center',
                            bordercolor = "grey",
                            borderwidth = 1,
                            relief = "solid"
                            )
        
        #Create a style for delete button
        self.style.configure('delete.TButton',
                             foreground="white",
                             background="#e60505",
                             font=("Helvetica", 10),
                             padding=(10, 10, 10, 10),
                             borderwidth=0,
                             highlightthickness=0,
                             width = 19
                             )
        self.style.map("delete.TButton", background=[('active', '#f80707')])
        
        #Creating style to the view trancaction table
        self.style.configure("view.Treeview",
                             foreground = "black",
                             background = "white",
                             rowheight = 30,
                             fieldbackground = "white",
                             font =("Helvetica", 11),
                             borderwidth = 1,
                             )
        
        self.style.configure("view.Treeview.Heading",
                             foreground = 'white',
                             background = "#5271ff",
                             font =("Helvetica", 12,"bold"),
                             borderwidth = 1,
                             bordercolor ="black",
                             highlightthickness=0,
                             relief = 'flat'

                             )
        self.style.configure("view.Treeview.Cell",
                             borderwidth=1,
                             font =("Helvetica", 15)
                             )
        self.style.map("view.Treeview.Heading", background=[('active', '#1a42f8')])

        self.style.map("view.Treeview",background =[('selected','#3257fc')])

        self.style.configure("Vertical.TScrollbar",
                                gripcount=0,
                                background="lightgrey",
                                darkcolor="lightgrey",
                                lightcolor="lightgrey",
                                troughcolor="white",
                                bordercolor="white",
                                highlightbackground="white",  # Set to match the troughcolor
                                highlightcolor="white",
                                relief = "flat"
                            )
        self.style.map("Vertical.TScrollbar",background =[('active','grey')])


class UpperMenuFrame(ttk.Frame):

    def __init__(self,parent):
        super().__init__(parent)

        # Apply the custom style to the frame
        self.configure(style='SearchFrame.TFrame')

        #Calling function class
        self.func = Functions(self)

        #puting widegets
        self.main_widgets()


        #Create a table for transactions using tree view       

        self.place(x=0, rely=0, relwidth=1, relheight=0.10)
    
    def main_widgets(self):

        # Create a sorting button
        clicked = tk.StringVar()

        #Creating a list for sorting item menu
        self.sort =["Sort by ","Date added accending", "Date added decending"]

        # Create the OptionMenu widget with the StringVar
        sort_btn = ttk.OptionMenu(self, clicked,*self.sort,command=self.sort_by)

        clicked.set("Sort by ")  # Setting a default value 

        sort_btn.config( style="sort.TMenubutton")
        sort_btn['menu'].config(
                        foreground="white",
                        background="#004aad",
                        font=("Helvetica", 9),
                        borderwidth= 0,
                        activeborderwidth =5,                 
                        )
        
        #Create a search bar label
        search_by = ["Search by","Date","Amount","Category","Type of transaction"]

        search_bar = ttk.Entry(self,text="",width=20,font=("Helvetica", 15))
        selected = tk.StringVar()
        search_btn = ttk.OptionMenu(self,selected,*search_by,command=lambda event: self.func.search_by(event,selected,search_bar,self))
        search_btn.config( style="sort.TMenubutton",width=16)
        search_btn['menu'].config(
                        foreground="white",
                        background="#004aad",
                        font=("Helvetica", 9),
                        borderwidth= 0,
                        activeborderwidth =5,
                        
                        )
        selected.set("Search by")

        search_bar.bind("<KeyRelease>", lambda event: self.func.search_by(event,selected,search_bar,self))
        
        #Create grid configuration 
        self.grid_columnconfigure((0,1),weight=1)
        self.grid_rowconfigure((0),weight=1)

        # Place & bind the search button
        search_bar.grid(row=0,column=0,sticky='nw',padx=(170,0),pady=(35,2))
        search_btn.grid(row=0,column=0,sticky='nw',padx=(20,0),pady=(30,0))
        search_btn.bind("<Enter>", Functions.on_enter)
        search_btn.bind("<Leave>", Functions.on_leave)

        #Placing & binding the sort button
        sort_btn.grid(row=0,column=1,sticky="se",padx=(0,20),pady=(0,15))
        sort_btn.bind("<Enter>", Functions.on_enter)
        sort_btn.bind("<Leave>", Functions.on_leave)

    def sort_by(self,sort):

        global transaction

        # "Date added", "Date accending", "Incomes","Expenses"
        
        if sort == "Date added decending":

            # Sort the table by date added and in decending order
            sorted_data = dict(sorted(transaction.items(), key=lambda x: x[0], reverse=True))
            transaction = sorted_data
            self.func.show_view_frame(self)
        
        elif sort == "Date added accending":
        
            #sorting the data according to the date added
            sorted_data = dict(sorted(transaction.items()))
            transaction = sorted_data
            self.func.show_view_frame(self)


class ViewTransactionFrame(ttk.Frame):

    def __init__(self,parent):
        super().__init__(parent)

        self.func = Functions(self)

        #Creating sub frames
        self.frame = ttk.Frame()
        self.frame.pack()

        #Create a table for transactions using tree view       
        self.tree_view_widget()

        self.place(x=0, rely=0.10, relwidth=1, relheight=0.60)

#Creating a transaction table 
    def tree_view_widget(self):

        global view_transactions

        self.tree_scroll = ttk.Scrollbar(self)

        self.view_transactions = ttk.Treeview(self,style="view.Treeview",yscrollcommand=self.tree_scroll.set)

        #Define the coloumns
        self.view_transactions['columns'] = ("Date","Amount","Category","Transaction type")

        #format the columns
        self.view_transactions.column("#0",width=0,stretch=NO)
        self.view_transactions.column("Date",anchor=CENTER,width=40)
        self.view_transactions.column("Amount",anchor=CENTER,width=80)
        self.view_transactions.column("Category",anchor=CENTER,width=120)
        self.view_transactions.column("Transaction type",anchor=W,width=120)

        #adding headings
        self.view_transactions.heading("#0",text="",anchor=CENTER,command=lambda: self.func.sort_by("Type",self.sort_order,self.view_transactions))
        self.view_transactions.heading("Date",text="Date",anchor=CENTER,command=lambda: self.func.sort_by("Date",self.sort_order,self.view_transactions))
        self.view_transactions.heading("Amount",text="Amount (Rs.)",anchor=CENTER,command=lambda: self.func.sort_by("Amount",self.sort_order,self.view_transactions))
        self.view_transactions.heading("Category",text= "Category",anchor=CENTER,command=lambda: self.func.sort_by("Category",self.sort_order,self.view_transactions))
        self.view_transactions.heading("Transaction type",text="Type of transaction",anchor=W,command=lambda: self.func.sort_by("Transaction type",self.sort_order,self.view_transactions))

        # Initialize sorting order for each column
        self.sort_order = {column: "asc" for column in self.view_transactions['columns']}

        #creating a variable to globalize
        view_transactions = self.view_transactions

        #Binding keyboard keys for various functions
        self.view_transactions.bind('<Delete>',lambda event: self.func.delete_selected_transactions(event,self))

        #adding data to transaction
        self.add_data(self.view_transactions)

        #Creating striped rows
        self.view_transactions.tag_configure("odd row",background = "#bff6ff")
        self.view_transactions.tag_configure("even row",background = "white")


        self.tree_scroll.config(command=self.view_transactions.yview,style="Vertical.TScrollbar")
        self.tree_scroll.pack(side=RIGHT , fill=Y,padx=(0,20),pady=(10,85))

        #Making the cursor change the icon into a different one when hovering over the headings
        self.view_transactions.bind("<Enter>", Functions.on_enter)
        self.view_transactions.bind("<Leave>", Functions.on_leave)

        # Place the Treeview widget
        self.view_transactions.pack(fill=tk.BOTH, expand=True,padx=(20,0), pady=(10,85))

#Adding the transactions into the table      
    def add_data(self,view_transactions):

        #add data to the treeview table
        count = 1
        for key,value in transaction.items():
            #formatting the amount so it would be displayed with two decimals
            number = value['amount']
            if isinstance(number,float):
                formatted_amount = "{:.2f}".format(value['amount'])
            
            if count % 2 == 0:
                view_transactions.insert(parent="",index="end",iid=key,values=(value['date'],formatted_amount,value['category'],value['type']),tags =("even row",))
            else:
                view_transactions.insert(parent="",index="end",iid=key,values=(value['date'],formatted_amount,value['category'],value['type']),tags =("odd row",))
            
            count += 1


class LowerMenuFrame(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        #Calling function class
        self.func = Functions(self)

        #Creating components
        self.main_widgets()

        self.place(x=0, rely=0.60, relwidth=1, relheight=0.10)

    def main_widgets(self):

        #creating none variable
        event=None

        # Creating buttons to add ,update and delete selected items and  delete all items functions
        add_transaction_btn = ttk.Button(self, text="Add a new transaction", style="blue.TButton", command=self.add_transactions_widgets)
        update_transaction_btn = ttk.Button(self, text="Update selected transaction", style="blue.TButton", command=self.update_transaction_widgets,width = 24)
        del_selected_transactions_btn = ttk.Button(self, text="Delete selected transactions", style="delete.TButton", command=lambda : self.func.delete_selected_transactions(event,self),width = 24)
        del_transaction_btn = ttk.Button(self, text="Delete all transaction", style="delete.TButton", command=lambda: self.func.delete_all_transactions(self))
        

        #Create grid configuration 
        self.grid_columnconfigure((0),weight=1)
        self.grid_rowconfigure((0,1),weight=1)
        
        add_transaction_btn.grid(row=0,column=0,sticky='nw',padx=(20,0),pady=20)
        add_transaction_btn.bind("<Enter>", Functions.on_enter)
        add_transaction_btn.bind("<Leave>", Functions.on_leave)

        update_transaction_btn.grid(row=0,column=0,sticky='nw',padx=(200,0),pady=20)
        update_transaction_btn.bind("<Enter>", Functions.on_enter)
        update_transaction_btn.bind("<Leave>", Functions.on_leave)

        del_selected_transactions_btn.grid(row=0,column=0,sticky='ne',padx=(0,200),pady=20)
        del_selected_transactions_btn.bind("<Enter>", Functions.on_enter)
        del_selected_transactions_btn.bind("<Leave>", Functions.on_leave)

        del_transaction_btn.grid(row=0,column=0,sticky='ne',padx=(0,20),pady=20)
        del_transaction_btn.bind("<Enter>", Functions.on_enter)
        del_transaction_btn.bind("<Leave>", Functions.on_leave)

    def add_transactions_widgets(self):

        func = Functions(self)

        #create a new window to add treansaction
        self.add= Toplevel(self.master)
        self.add.title("Add new transaction")
        try:
            self.add.iconbitmap(working_directory/"ico/add.ico")
        except:
            messagebox.showerror("Icon error","Neccessary Icon wasn't loaded successfully")
        self.add.geometry('500x400')
        self.add.resizable(False,False)
        self.add.config(background='white')
        
        #creating widgets

        #Date -date entry
        date = ttk.Label(self.add,text="Date :",foreground="#004aad",background="white",font=("Helvetica", 15,"bold"))

        dd = ttk.Label(self.add,text="DD :",foreground="#b7c4ff",background="white",font=("Helvetica", 11))
        self.date_d = ttk.Entry(self.add,width="5",foreground='grey',font=("Helvetica", 15))
        self.date_d.insert(0,"DD")
        self.date_d.bind('<FocusIn>', lambda event: func.Date_D_FI(event,self.date_d))
        self.date_d.bind('<FocusOut>', lambda event: self.func.validate_entries(event.widget,self.date_d,self.date_M,self.date_y,self.amount))
        
        #Date - Month entry
        mm = ttk.Label(self.add,text="MM :",foreground="#b7c4ff",background="white",font=("Helvetica", 11))
        self.date_M = ttk.Entry(self.add,width="6",foreground='grey',font=("Helvetica", 15))
        self.date_M.insert(0,"MM")
        self.date_M.bind('<FocusIn>', lambda event: func.Date_M_FI(event,self.date_M))
        self.date_M.bind('<FocusOut>', lambda event: self.func.validate_entries(event.widget,self.date_d,self.date_M,self.date_y,self.amount))
        
        #Adding a entry for year
        yy = ttk.Label(self.add,text="YYYY :",foreground="#b7c4ff",background="white",font=("Helvetica", 11))
        self.date_y = ttk.Entry(self.add,width="6",foreground='grey',font=("Helvetica", 15,))
        self.date_y.insert(0,"YYYY")
        self.date_y.bind('<FocusIn>', lambda event: func.Date_Y_FI(event,self.date_y))
        self.date_y.bind('<FocusOut>', lambda event: self.func.validate_entries(event.widget,self.date_d,self.date_M,self.date_y,self.amount))

        #Adding amount widget
        self.amount_l = ttk.Label(self.add,text="Amount :",foreground="#004aad",background="white",font=("Helvetica", 15,"bold"))
        self.amount = ttk.Entry(self.add,width="12",foreground='black',font=("Helvetica", 15,))
        self.amount.bind('<FocusOut>', lambda event: self.func.validate_entries(event.widget,self.date_d,self.date_M,self.date_y,self.amount))

        #Adding category widget
        content= ["Income","Income","Expense"]
        self.category_1 = ttk.Label(self.add,text="Category :",foreground="#004aad",background="white",font=("Helvetica", 15,"bold"))
        self.selected = StringVar()
        self.category = ttk.OptionMenu(self.add,self.selected, *content,)
        self.category.config(style=("category.TMenubutton"))
        self.category['menu'].config(
                        foreground="white",
                        background="#004aad",
                        font=("Helvetica", 9),
                        borderwidth= 0,
                        activeborderwidth =5,  
                        )

        #Adding the type of transaction wdiget
        self.type_1 = ttk.Label(self.add,text="Transaction Type :",foreground="#004aad",background="white",font=("Helvetica", 15,"bold"),width=20)
        self.type = ttk.Entry(self.add,width="12",foreground='black',font=("Helvetica", 15,))

        #Adding the add button
        self.add_btn = ttk.Button(self.add, text="+ Add", style="blue.TButton", command=lambda: self.func.add_func(self.date_d,self.date_M,self.date_y,self.amount,self.selected,self.type,self.add,self))

        #adding widgets to the window
        date.grid(row=0,column=0,sticky='w',padx=(10,0),pady=(2,0))
        dd.grid(row=0,column=0,sticky='w',padx=(10,0),pady=(50,0))       
        self.date_d.grid(row=0,column=0,sticky='w',padx=(10,0),pady=(100,0))

        mm.grid(row=0,column=0,sticky='w',padx=(80,0),pady=(50,0))
        self.date_M.grid(row=0,column=0,sticky='w',padx=(80,0),pady=(100,0))

        yy.grid(row=0,column=0,sticky='w',padx=(165,0),pady=(50,0))
        self.date_y.grid(row=0,column=0,sticky='w',padx=(165,0),pady=(100,0))

        self.amount_l.grid(row=1,column=0,sticky='nw',padx=(10,0),ipady=(30))
        self.amount.grid(row=1,column=0,sticky='w',padx=(120,0),pady=(0,0))

        self.category_1.grid(row=2,column=0,sticky='nw',padx=(10,0),pady = (0,250))
        self.category.grid(row=2,column=0,sticky='w',padx=(120,0),pady=(0,250))

        self.type_1.grid(row=2,column=0,sticky='nw',padx=(10,0),pady = (50,0))
        self.type.grid(row=2,column=0,sticky='w',padx=(200,0),pady=(0,150))

        self.add_btn.grid(row=2,column=1,sticky='se',padx=(0,0),pady = (0,110))
        self.add_btn.bind("<Enter>", Functions.on_enter)
        self.add_btn.bind("<Leave>", Functions.on_leave)

        #creating a warning message asking user to  confirm is closing the window
        self.add.protocol("WM_DELETE_WINDOW", lambda: self.func.on_closing(self.date_d,self.date_M,self.date_y,self.amount,self.selected,self.type,self.add))

    def update_transaction_widgets(self):

        selected_transaction_list = view_transactions.selection()
        l_list = len(selected_transaction_list)

        if l_list == 1 or l_list == 0:

            try:

                selected_item = view_transactions.selection()[0]

                values = view_transactions.item(selected_item,'values')

                #create a new window to add treansaction
                self.up= Toplevel(self.master)
                self.up.title("Update the selected transaction")
                try:
                    self.up.iconbitmap(working_directory /"ico/edit.ico")
                except:
                    messagebox.showerror("Icon error","Neccessary Icon wasn't loaded successfully")
                self.up.geometry('600x500')
                self.up.resizable(False,False)
                self.up.config(background='white')
                
                #creating widgets

                #Creating a labels to show the selected coloumn
                text_label = ttk.Label(self.up,text ="This coloumn wil be updated:",foreground="#004aad",background="white",font=("Helvetica", 15,"bold"))

                date_label = ttk.Label(self.up,text ="Date",style = "menu.TLabel",width=10)
                amount_label = ttk.Label(self.up,text ="Amount",style = "menu.TLabel",width=10)
                category_label = ttk.Label(self.up,text ="Category",style = "menu.TLabel",width=10)
                type_label = ttk.Label(self.up,text ="Type of transaction",style = "menu.TLabel",width=20)


                #Inserting the selected row
                value_1 = ttk.Label(self.up,text =f"{values[0]}",style="normal.TLabel",width=15,anchor="center")
                value_2 = ttk.Label(self.up,text =f"{values[1]}",style="normal.TLabel",width=15)
                value_3 = ttk.Label(self.up,text =f"{values[2]}",style="normal.TLabel",width=15)
                value_4 = ttk.Label(self.up,text =f"{values[3]}",style="normal.TLabel",width=27)
                

                #Date -date entry
                date = ttk.Label(self.up,text="Date :",foreground="#004aad",background="white",font=("Helvetica", 15,"bold"))

                dd = ttk.Label(self.up,text="DD :",foreground="#b7c4ff",background="white",font=("Helvetica", 11))
                self.up_date_d = ttk.Entry(self.up,width="5",foreground='grey',font=("Helvetica", 15))
                self.up_date_d.insert(0,"DD")
                self.up_date_d.bind('<FocusIn>', lambda event: self.func.Date_D_FI(event,self.up_date_d))
                self.up_date_d.bind('<FocusOut>', lambda event: self.func.validate_entries(event.widget,self.up_date_d,self.up_date_M,self.up_date_y,self.up_amount))
                
                #Date - Month entry
                mm = ttk.Label(self.up,text="MM :",foreground="#b7c4ff",background="white",font=("Helvetica", 11))
                self.up_date_M = ttk.Entry(self.up,width="6",foreground='grey',font=("Helvetica", 15))
                self.up_date_M.insert(0,"MM")
                self.up_date_M.bind('<FocusIn>', lambda event: self.func.Date_M_FI(event,self.up_date_M))
                self.up_date_M.bind('<FocusOut>', lambda event: self.func.validate_entries(event.widget,self.up_date_d,self.up_date_M,self.up_date_y,self.up_amount))
                
                #Adding a entry for year
                yy = ttk.Label(self.up,text="YYYY :",foreground="#b7c4ff",background="white",font=("Helvetica", 11))
                self.up_date_y = ttk.Entry(self.up,width="6",foreground='grey',font=("Helvetica", 15,))
                self.up_date_y.insert(0,"YYYY")
                self.up_date_y.bind('<FocusIn>', lambda event: self.func.Date_Y_FI(event,self.up_date_y))
                self.up_date_y.bind('<FocusOut>', lambda event: self.func.validate_entries(event.widget,self.up_date_d,self.up_date_M,self.up_date_y,self.up_amount))

                #Adding amount widget
                self.up_amount_l = ttk.Label(self.up,text="Amount :",foreground="#004aad",background="white",font=("Helvetica", 15,"bold"))
                self.up_amount = ttk.Entry(self.up,width="12",foreground='black',font=("Helvetica", 15,))
                self.up_amount.bind('<FocusOut>', lambda event: self.func.validate_entries(event.widget,self.up_date_d,self.up_date_M,self.up_date_y,self.up_amount))

                #Adding category widget
                content= ["select","Income","Expense"]
                self.up_category_1 = ttk.Label(self.up,text="Category :",foreground="#004aad",background="white",font=("Helvetica", 15,"bold"))
                self.up_selected = StringVar()
                self.up_category = ttk.OptionMenu(self.up,self.up_selected, *content,)
                self.up_selected.set("select")
                self.up_category.config(style=("category.TMenubutton"))
                self.up_category['menu'].config(
                                foreground="white",
                                background="#004aad",
                                font=("Helvetica", 9),
                                borderwidth= 0,
                                activeborderwidth =5,  
                                )

                #Adding the type of transaction wdiget
                self.up_type_1 = ttk.Label(self.up,text="Transaction Type :",foreground="#004aad",background="white",font=("Helvetica", 15,"bold"),width=20)
                self.up_type = ttk.Entry(self.up,width="12",foreground='black',font=("Helvetica", 15,))

                #Adding the add button
                self.update_btn = ttk.Button(self.up, text="Update", style="blue.TButton", command=lambda: self.func.update_row(self.up_date_d, self.up_date_M, self.up_date_y, self.up_amount, self.up_selected, self.up_type,int(selected_item),values[0], self.up,self))

                #adding widgets to the window
                text_label.grid(row=0,column=0,sticky='nw',padx=(10,0),pady=(10,0))
                date_label.grid(row=0,column=0,sticky='nw',padx=(40,0),pady=(50,0))
                amount_label.grid(row=0,column=0,sticky='nw',padx=(150,0),pady=(50,0))
                category_label.grid(row=0,column=0,sticky='nw',padx=(255,0),pady=(50,0))
                type_label.grid(row=0,column=0,sticky='nw',padx=(365,0),pady=(50,0))

                value_1.grid(row=0,column=0,sticky='nw',padx=(40,0),pady=(76,0))
                value_2.grid(row=0,column=0,sticky='nw',padx=(150,0),pady=(76,0))
                value_3.grid(row=0,column=0,sticky='nw',padx=(255,0),pady=(76,0))
                value_4.grid(row=0,column=0,sticky='nw',padx=(365,0),pady=(76,0))

                date.grid(row=1,column=0,sticky='w',padx=(10,0),pady=(2,0))
                dd.grid(row=1,column=0,sticky='w',padx=(10,0),pady=(50,0))       
                self.up_date_d.grid(row=1,column=0,sticky='w',padx=(10,0),pady=(100,0))

                mm.grid(row=1,column=0,sticky='w',padx=(80,0),pady=(50,0))
                self.up_date_M.grid(row=1,column=0,sticky='w',padx=(80,0),pady=(100,0))

                yy.grid(row=1,column=0,sticky='w',padx=(165,0),pady=(50,0))
                self.up_date_y.grid(row=1,column=0,sticky='w',padx=(165,0),pady=(100,0))

                self.up_amount_l.grid(row=2,column=0,sticky='nw',padx=(10,0),ipady=(30))
                self.up_amount.grid(row=2,column=0,sticky='w',padx=(120,0),pady=(0,0))

                self.up_category_1.grid(row=3,column=0,sticky='nw',padx=(10,0),pady = (0,120))
                self.up_category.grid(row=3,column=0,sticky='w',padx=(120,0),pady=(0,180))

                self.up_type_1.grid(row=3,column=0,sticky='nw',padx=(10,0),pady = (50,0))
                self.up_type.grid(row=3,column=0,sticky='nw',padx=(200,0),pady=(50,0))

                self.update_btn.grid(row=3,column=0,sticky='se',padx=(0,0),pady = (0,40))
                self.update_btn.bind("<Enter>", Functions.on_enter)
                self.update_btn.bind("<Leave>", Functions.on_leave)

                #creating a warning message asking user to  confirm is closing the window
                #self.up.protocol("WM_DELETE_WINDOW", lambda: self.func.on_closing(self.up_date_d, self.up_date_M, self.up_date_y, self.up_amount, self.up_selected, self.up_type, self.up))

            except IndexError:
                messagebox.showerror("Row selection","No row is selected")
        else:
            messagebox.showwarning("Update error","You cannot update multiple columns at the same time")


class ViewSummaryFrame(ttk.Frame):

    def __init__(self,parent):
        super().__init__(parent)

        #Calling summary table
        self.summary_table()

        self.place(x=0, rely=0.7, relwidth=1, relheight=0.30)
    
    def summary_table(self):

        func = Functions(self)
        net_balance , total_expense, total_income = func.summary_data()
        
        border_label = ttk.Label(self,text="",style="border.TLabel",width=80,)
        title_label = ttk.Label(self,text="Title",style="menu.TLabel",borderwidth=0,font =("Helvetica", 15,"bold"),width=33,padding=(0,6))
        amount_label = ttk.Label(self,text="Amount (Rs.)",style="menu.TLabel",borderwidth=0,font =("Helvetica", 15,"bold"),width=26,padding=(0,6))

        income_label =ttk.Label(self,text="Incomes",style="normal.TLabel",borderwidth=0,background="#e6e6e6",width=40,font =("Helvetica", 12),padding=(0,10))
        income_a_label =ttk.Label(self,text=f"{total_income}",style="normal.TLabel",borderwidth=0,background="#e6e6e6",width=32,font =("Helvetica", 12),padding=(0,10))

        expense_label = ttk.Label(self,text="Expenses",style="normal.TLabel",borderwidth=0,width=40,font =("Helvetica", 12),padding=(0,10))
        expense_a_label =ttk.Label(self,text=f"- {total_expense}",style="normal.TLabel",borderwidth=0,width=32,font =("Helvetica", 12),padding=(0,10))
        
        net_balance_label =ttk.Label(self,text="Net balance",style="normal.TLabel",borderwidth=0,background="#e6e6e6",width=40,font =("Helvetica", 12),padding=(0,10))
        net_balance_a_label =ttk.Label(self,text=f"{net_balance}",style="normal.TLabel",borderwidth=0,background="#e6e6e6",width=32,font =("Helvetica", 12),padding=(0,10))

        border_label.grid(row=0,column=0,sticky="n",padx=(400,0),pady=(0,0))
        title_label.grid(row=0,column=0,sticky="n",padx=(135,20),pady=(2,0))
        amount_label.grid(row=0,column=0,sticky="n",padx=(780,20),pady=(2,0))

        income_label.grid(row=0,column=0,sticky="n",padx=(136,20),pady=(38,0))
        income_a_label.grid(row=0,column=0,sticky="n",padx=(777,20),pady=(38,0))

        expense_label.grid(row=0,column=0,sticky="n",padx=(136,20),pady=(76,0))
        expense_a_label.grid(row=0,column=0,sticky="n",padx=(777,20),pady=(76,0))

        net_balance_label.grid(row=0,column=0,sticky="n",padx=(136,20),pady=(114,0))
        net_balance_a_label.grid(row=0,column=0,sticky="n",padx=(777,20),pady=(114,0))

class Functions():

    def __init__(self,parent):       
        self.parent = parent

        #Getting necessary classes
        self.menu = LowerMenuFrame

    #Placeholder logic
    def Date_D_FI(self,event,date):
        print(date)
        if date.get() == 'DD':
            date.delete(0, tk.END)
            date.config(foreground='black')
            date.focus()
    
    #Placeholder logic
    def Date_Y_FI(self,event,date):
        if date.get() == 'YYYY':
            date.delete(0, tk.END)
            date.config(foreground='black')
            date.focus()
    
    #Placeholder logic
    def Date_M_FI(self,event,date):
        if date.get() == 'MM':
            date.delete(0, tk.END)
            date.config(foreground='black')
            date.focus()

    #creating summary function
    def summary_data(self):

        #creating necessary variables in order to calculate net balance and show other necessary details
        income = 0
        expense = 0
        self.total_income =0
        self.total_expense = 0
        self.net_balance = 0
        
        for key,values in transaction.items():
            category = values['category']
            category_low = category.lower()
            if category_low == "income":
                income = values['amount']
                self.net_balance += income
                self.total_income += income

            elif category_low == "expense":
                expense = values['amount']
                self.net_balance -= expense
                self.total_expense += expense
        
        #Making total income shows to the two decimal points
        inc = self.total_income
        if isinstance(inc,float):
            formatted_income = "{:.2f}".format(self.total_income)
        else:
            formatted_income = str(self.total_income)
        
        #Making total expense shows to the two decimal points
        exp = self.total_expense
        if isinstance(exp,float):
            formatted_expense = "{:.2f}".format(self.total_expense)
        else:
            formatted_expense = str(self.total_expense)
        
        #Making net balance shows to the two decimal points
        net = self.net_balance
        if isinstance(net,float):
            formatted_net_balance = "{:.2f}".format(self.net_balance)
        else:
            formatted_net_balance = str(self.net_balance)
                
        return formatted_net_balance,formatted_expense,formatted_income

    #Getting sort by function
    def sort_by(self, column,sort,view_transactions):

        # Toggle sorting order
        current_order = sort[column]
        new_order = "asc" if current_order == "desc" else "desc"
        sort[column] = new_order

        # Determine sorting order
        reverse = False if new_order == "asc" else True

        # Sort Treeview based on the selected column
        if column == "Amount":
            items = view_transactions.get_children("")
            sorted_items = sorted(items, key=lambda x: float(view_transactions.set(x, column)), reverse=reverse)
            for item in sorted_items:
                view_transactions.move(item, "", "end")
        else:
            items = view_transactions.get_children("")
            sorted_items = sorted(items, key=lambda x: view_transactions.set(x, column), reverse=reverse)
            for item in sorted_items:
                view_transactions.move(item, "", "end")
        
        self.update_striped_rows(view_transactions)
    
    def update_striped_rows(self, treeview):
        
        # Re-apply tags based on the current row order
        for i, item in enumerate(treeview.get_children()):
            tags = ("odd row" if i % 2 == 0 else "even row",)
            treeview.item(item, tags=tags)

    #Updating the transaction
    def update_row(self,day,month,year,amount,category,t_type,selected_item,date_object,second_window,frame):


                #Getting the values from the entries
                v_day = day.get()
                v_month = month.get()
                v_year = year.get()
                v_amount = amount.get()
                v_category = category.get()
                v_type = t_type.get()

                split_date = date_object.split("-")
                        
                for key,values in transaction.items():

                    if key == selected_item:

                        #Formatting the date field
                        if day.get() != "" and day.get() !="DD":
                            l_day = len(v_day)
                            if l_day == 1:
                                format_day = "0" + str(v_day)
                            else:
                                format_day = v_day
                        
                        #formating the month field
                        if month.get() != "" and month.get() != "MM":
                            l_month = len(v_month)
                            if l_month == 1:
                                format_month = "0" + v_month
                            else:
                                format_month = v_month
                        
                        #formating the year field
                        if year.get() != "" and year.get() != "YYYY":
                            format_year = str(v_year)

                        #Entering the date according to the input criteria
                        if day.get() != "" and day.get() !="DD" and month.get() != "" and month.get() != "MM" and year.get() != "" and year.get() != "YYYY":

                            date= (f"{format_year}-{format_month}-{format_day}")
                            values['date'] = date
                        
                        elif day.get() != "" and day.get() !="DD" and month.get() != "" and month.get() != "MM":

                            date= (f"{split_date[0]}-{format_month}-{format_day}")
                            values['date'] = date
                        
                        elif day.get() != "" and day.get() !="DD" and year.get() != "" and year.get() != "YYYY":

                            date= (f"{format_year}-{split_date[1]}-{format_day}")
                            values['date'] = date
                        
                        elif month.get() != "" and month.get() != "MM" and year.get() != "" and year.get() != "YYYY":

                            date= (f"{format_year}-{format_month}-{split_date[2]}")
                            values['date'] = date
                        
                        elif day.get() != "" and day.get() !="DD":

                            date= (f"{split_date[0]}-{split_date[1]}-{format_day}")
                            values['date'] = date
                        
                        elif month.get() != "" and month.get() != "MM":

                            date= (f"{split_date[0]}-{format_month}-{split_date[2]}")
                            values['date'] = date
                        
                        elif year.get() != "" and year.get() != "YYYY":

                            date= (f"{format_year}-{split_date[1]}-{split_date[2]}")
                            values['date'] = date


                        if amount.get() !="":
                            f_amount = float(v_amount)
                            values['amount'] = f_amount
                        
                        if category.get() !="select":
                            f_category = str.upper(v_category)
                            values['category'] = f_category
                        
                        if t_type.get() !="":
                            f_type = str.title(v_type)
                            values['type'] = f_type

                        self.show_view_frame(frame)
                        FileHandling.save_transaction()
                        second_window.destroy()
                        messagebox.showinfo("Update status","Transaction updated successfully !")

    #Adding the transaction to the json file
    def add_func(self,d_day,d_month,d_year,a_amount,c_category,t_type,second_window,frame):

        #checking whether the Input fields are not empty 

        if d_day.get() == "DD" or d_day.get() == "" :
            messagebox.showwarning("Empty input field", "The date field can not be empty")
            d_day.focus()

        elif d_month.get() == "" or d_month.get() == "MM":
            messagebox.showwarning("Empty input field", "The month field can not be empty")
            d_month.focus()
        
        elif d_year.get() == "" or d_year.get() == "YYYY":
            messagebox.showwarning("Empty input field", "The year field can not be empty")
            d_year.focus()
        
        elif a_amount.get() == "":
            messagebox.showwarning("Empty input field", "The amount field can not be empty")
            a_amount.focus()
        
        elif t_type.get() == "":
            messagebox.showwarning("Empty input field", "The transaction type field can not be empty")
            t_type.focus()
        
        #Adding the new data into transaction dictionary
        else:

            #getting the data from widgets
            day = d_day.get()
            month = d_month.get()
            year = d_year.get()
            amount = a_amount.get()
            category = c_category.get()
            type = t_type.get()

            #creating the date input
            l_day = len(day)
            if l_day == 1:
                format_day = "0" + str(day)
            else:
                format_day = day
            
            l_month = len(month)
            if l_month == 1:
                format_month = "0" + month
            else:
                format_month = month
                
            format_year = str(year)
            date = (f"{format_year}-{format_month}-{format_day}")

            #Changing the format of category, type of transaction and amount
            f_type = str.title(type)
            f_category = str.upper(category)
            f_amount = float(amount)
            
            #Adding the date to transaction
            no_key = max(transaction.keys())
            transaction[no_key+1] = {'category': f_category, 'type': f_type, 'date': date , 'amount': f_amount}
            messagebox.showinfo("Info","Transaction has successfully added !!")
            FileHandling.save_transaction()

            self.show_view_frame(frame)
            second_window.destroy()

    #Validate the neccessary data entries
    def validate_entries(self,widget,day,month,year,amount):

            #Validate the day field in date field
        def Date_d_validate(date):

            if date.isdigit():
                num = int(date)
                if 1 <= num <= 31:
                    return True
                else:
                    return False

        #Validate the month field in date field
        def Date_m_validate(date):

            if date.isdigit():
                num = int(date)
                if 1 <= num <= 12:
                    return True
                else:
                    return False

        #Validate the year field in date field       
        def Date_y_validate(date):

            if date.isdigit():
                num = int(date)
                if 1700 <= num <= 2030:
                    return True
                else:
                    return False

        #Validate the amount field
        def amount_validate_func(number):
                try:
                    #Making the amount entered is within the range of currency
                    convert_amount = float(number)
                    r_amount = round(convert_amount,2)
                    if r_amount == convert_amount:
                        return True
                    else:
                        raise ValueError
                except ValueError:
                        return False

        # Validate Date - Date entry
        if day.get() and widget == day and not Date_d_validate(day.get()):
            response = messagebox.showwarning("Invalid Date", "The Day should be between 1-31")
            if response == "ok":
                day.delete(0, tk.END)
                day.focus()
                return False

        # Validate Date - Month entry
        if month.get() and widget == month and not Date_m_validate(month.get()):
            response = messagebox.showwarning("Invalid Month", "The Month should be between 1-12")
            if response == "ok":
                month.delete(0, tk.END)
                month.focus()
                return False

        # Validate Date - Year entry
        if year.get() and widget == year and not Date_y_validate(year.get()):
            response = messagebox.showwarning("Invalid Year", "Enter a valid year")
            if response == "ok":
                year.delete(0, tk.END)
                year.focus()
                return False

        # Validate amount entry
        if amount.get() and widget == amount and not amount_validate_func(amount.get()):
            response = messagebox.showwarning("Invalid amount", "Enter a valid amount")
            if response == "ok":
                amount.delete(0, tk.END)
                amount.focus()
                return False

        return True

    #Deleting all transactions from the application
    def delete_all_transactions(self,frame):
        global transaction
        response = messagebox.askokcancel("Deleting all transaction ", "This will delete all the transactions do you wish to continue ?")
        if response == True:
            transaction = {}
            self.show_view_frame(frame)
            FileHandling.save_transaction()
            messagebox.showinfo("Delete status","All the transactions deleted successfully")
    
    #Deleting selected transactions from the application
    def delete_selected_transactions(self,event,frame):
        
        selected_transaction_list = view_transactions.selection()
        l_list = len(selected_transaction_list)

        if l_list == 0:
            messagebox.showerror("Error","No row been selected")

        #Deleting 1 row
        elif l_list == 1:
            response = messagebox.askokcancel("Delete transactions","The selected transaction will be deleted Do you wish to continue ?")
            number = int(selected_transaction_list[0])
            if response == True:
                for key in transaction.keys():
                    if number == key:
                        del transaction[key]
                        messagebox.showinfo("Success status","Selected Transaction deleted successfully !")
                        self.show_view_frame(frame)
                        FileHandling.save_transaction()
                        break

        #Deleting several rows
        else:
            response = messagebox.askokcancel("Delete transactions","The selected transactions will be deleted Do you wish to continue ?")
            number = []
            count = 0
            if response == True:
                for items in selected_transaction_list:
                    number.append(int(items))

                for key in temp_transaction.keys():
                    for num in number:
                        if num == key:
                            del transaction[key]
                            self.show_view_frame(frame)
                            FileHandling.save_transaction()
                            break
                messagebox.showinfo("Success status","Selected Transactions deleted successfully !")

    #Asking a confirmation when closing a secondary window
    def on_closing(self,date,month,year,amount,category,t_type,frame):
        empty_entries = self.get_empty_entries(date,month,year,amount,category,t_type)
        if empty_entries:

            response = messagebox.askyesno("Empty Entries", "Some fields are empty. Do you want to close the window?")
            if response == True:
                frame.destroy()
            else:
                frame.focus()
        else:
            frame.destroy()

    #Getting empty entries in the secondary windows
    def get_empty_entries(self,date,month,year,amount,category,t_type):
        entries = [date, month, year, amount, t_type]
        empty_entries = [entry for entry in entries if entry.get().strip() == ""]
        return empty_entries         

    #Search by buttons logic
    def search_by(self,event,selected,search,frame):

        global transaction

        search_query = search.get()
        matching_transactions = {}
        select = selected.get()

        if search_query == "":

            #sorting the data according to the date added
            sorted_data = dict(sorted(temp_transaction.items()))
            transaction = sorted_data
            self.show_view_frame(frame)
        
        else:                  
            if select == "Type of transaction":
                for key,values in temp_transaction.items():

                    if search_query in values['type'].lower():  

                        matching_transactions[key] =values
                        transaction =matching_transactions
                        self.show_search_table(frame)
            
            elif select == "Date":
                for key,values in temp_transaction.items():

                    if search_query in values['date']: 

                        matching_transactions[key] =values
                        transaction =matching_transactions
                        self.show_search_table(frame)
            
            elif select == "Amount":
                for key,values in temp_transaction.items():

                    amount = str(values['amount'])
                    if search_query in amount: 

                        matching_transactions[key] =values
                        transaction =matching_transactions
                        self.show_search_table(frame)
            
            elif select == "Category":
                for key,values in temp_transaction.items():

                    if search_query in values['category'].lower():  

                        matching_transactions[key] =values
                        transaction =matching_transactions
                        self.show_search_table(frame)


    def show_view_frame(self,frame):
        # Destroy the existing ViewFrame instance if it exists
        if hasattr(frame, "view_frame"):
            frame.view_frame.destroy()
        
        # Create new instances of ViewTransactionFrame and ViewSummaryFrame
        self.view_frame = ViewTransactionFrame(frame.master)
        self.main_func = LowerMenuFrame(frame.master)
        self.view_summary = ViewSummaryFrame(frame.master)

    def show_search_table(self,frame):
        # Destroy the existing ViewFrame instance if it exists
        if hasattr(frame, "view_frame"):
            frame.view_frame.destroy()
        
        # Create new instances of ViewTransactionFrame and ViewSummaryFrame
        self.view_frame = ViewTransactionFrame(frame.master)
        self.main_func = LowerMenuFrame(frame.master)

    # Create cursor changes to hand when entering inside a button
    @staticmethod
    def on_enter(event):
        event.widget.config(cursor="hand2")

    @staticmethod
    def on_leave(event):
        event.widget.config(cursor="")


if __name__== "__main__":
    if FileHandling.load_transaction():
        FileHandling.bulk_reading(working_directory /"data/transaction.json")
        FinanceTrackerGUI()