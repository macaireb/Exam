from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import DB_interface

class ExamApp(Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.style = Style()
        self.style.configure("BW.TFrame", foreground="black", background="white")
        self.style.configure("BW.TButton", foreground="black", background="white")
        self.style.configure("BW.TLabel", foreground="black", background="white")
        self.DB = DB_interface.DB_interface()
        # Vertical Menu
        self.option_add('*tearOff', False)
        self.my_menu = Menu(self)
        self.file_menu = Menu(self.my_menu)
        self.admin_menu = Menu(self.my_menu)
        self.config(menu=self.my_menu)
        self.my_menu.add_cascade(label="File", menu=self.file_menu)
        self.my_menu.add_cascade(label="Administrator", menu=self.admin_menu)
        self.file_menu.add_command(label="View Users", command=self.list_users)
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.admin_menu.add_command(label="Add/Edit/Remove User", command=self.admin_users)

    def exit(self):
        self.quit()

    def list_users(self):
        self.hide_frames()
        self.user_strs = StringVar(value=self.DB.get_users())
        self.users_frame = Frame(self, style="BW.TFrame")
        self.view_users_list = Listbox(self.users_frame, listvariable=self.user_strs, height=15)
        self.select_user_btn = Button(self.users_frame, style="BW.TButton", command=self.view_exams, text="Select User")
        self.users_frame.pack()
        self.view_users_list.grid(row=1, column=1, columnspan=2)
        self.select_user_btn.grid(row=2, column=2, columnspan=1)

    def view_exams(self):
        self.hide_frames()
        self.exams_frame = Frame(self, style="BW.TFrame")
        self.view_exams_list = Listbox(self.exams_frame, height=15)
        self.select_exam_btn = Button(self.exams_frame, style="BW.TButton", command=self.take_exam, text="Take Exam")
        self.exams_frame.pack()
        self.view_exams_list.grid(row=1, column=1, columnspan=2)
        self.select_exam_btn.grid(row=2, column=2, columnspan=1)

    def admin_users(self):
        self.hide_frames()
        self.admin_str_users = StringVar(value=self.DB.get_users())
        self.admin_frame = Frame(self, style="BW.TFrame")
        self.admin_frame.columnconfigure(0, weight=2)
        self.admin_frame.columnconfigure(1, weight=1)
        self.admin_frame.rowconfigure(0, weight=1)
        self.admin_frame.rowconfigure(1, weight=1)
        self.admin_frame.rowconfigure(2, weight=1)
        self.admin_frame.rowconfigure(3, weight=1)
        self.admin_user_list = Listbox(self.admin_frame, listvariable=self.admin_str_users, height=15)
        self.fname_lbl = Label(self.admin_frame, style="BW.TLabel", text="First Name")
        self.fname = StringVar()
        self.fname_input = Entry(self.admin_frame, textvariable=self.fname)
        self.lname_lbl = Label(self.admin_frame, style="BW.TLabel", text="Last Name")
        self.lname = StringVar()
        self.lname_input = Entry(self.admin_frame, textvariable=self.lname)
        self.add_user = Button(self.admin_frame, style="BW.TButton", text="Add User", command=self.add_user)
        self.remove_user = Button(self.admin_frame, style="BW.TButton", text="Remove User", command=self.remove_user)
        self.admin_frame.pack()
        self.admin_user_list.grid(row=1, rowspan=4, column=1, columnspan=2)
        self.fname_lbl.grid(row=1, rowspan=1, column=3)
        self.fname_input.grid(row=2, column=3)
        self.lname_lbl.grid(row=1, rowspan=1, column=4)
        self.lname_input.grid(row=2, column=4)
        self.add_user.grid(row=3, column=3, columnspan=2)
        self.remove_user.grid(row=4, column=3, columnspan=2)

    def add_user(self):
        valid = [False, False]
        if self.fname.get().isalpha():
            valid[0] = True
        else:
            fname_msg = tkinter.messagebox.Message(self, title="Invalid",
                                                   message="Only letters are allowed, please correct First name")
            fname_msg.show()
        if self.lname.get().isalpha():
            valid[1] = True
        else:
            lname_msg = tkinter.messagebox.Message(self, title="Success",
                                                   message="Only letters are allowed, please correct Last name")
            lname_msg.show()
        if valid[0] & valid[1]:
            self.DB.add_user(self.fname.get(), self.lname.get())
            self.fname_input.delete(0, 'end')
            self.lname_input.delete(0, 'end')
            if self.admin_user_list.winfo_exists():
                self.admin_user_list.destroy()
                self.admin_str_users = StringVar(value=self.DB.get_users())
                self.admin_user_list = Listbox(self.admin_frame, listvariable=self.admin_str_users, height=15)
                self.admin_user_list.grid(row=1, rowspan=4, column=1, columnspan=2)

    def remove_user(self): pass

    def take_exam(self): pass

    def hide_frames(self):
        try:
            if self.users_frame.winfo_exists():
                self.users_frame.pack_forget()
        except AttributeError: pass
        try:
            if self.exams_frame.winfo_exists():
                self.exams_frame.pack_forget()
        except AttributeError: pass
        try:
            if self.admin_frame.winfo_exists():
                self.admin_frame.pack_forget()
        except AttributeError: pass