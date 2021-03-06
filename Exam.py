import tkinter
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
        self.admin_menu.add_command(label="Create Exam", command=self.create_exam)

    def exit(self):
        self.quit()

    def list_users(self):
        self.hide_frames()
        self.user_strs = StringVar(value=self.DB.get_users())
        self.users_frame = Frame(self, style="BW.TFrame")
        self.view_users_list = Listbox(self.users_frame, listvariable=self.user_strs, height=15)
        self.select_user_btn = Button(self.users_frame, style="BW.TButton", command=self.view_exams, text="View my test")
        self.users_frame.grid()
        self.view_users_list.grid(row=1, column=1, columnspan=2)
        self.select_user_btn.grid(row=2, column=2, columnspan=1)

    def view_exams(self):
        self.hide_frames()
        self.exams_frame = Frame(self, style="BW.TFrame")
        exam_list_str = StringVar(value=self.DB.get_exams_list())
        self.view_exams_list = Listbox(self.exams_frame, listvariable=exam_list_str, height=15)
        self.select_exam_btn = Button(self.exams_frame, style="BW.TButton", command=self.take_exam, text="Take Exam")
        self.exams_frame.grid()
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

    def remove_user(self):
        selection = self.admin_user_list.curselection()
        index = selection[0]
        value = self.admin_user_list.get(index)
        print("The item being removed is: " + value[0] + ' ' + value[1])
        self.DB.remove_user(value[0], value[1])
        if self.admin_user_list.winfo_exists():
            self.admin_user_list.destroy()
            self.admin_str_users = StringVar(value=self.DB.get_users())
            self.admin_user_list = Listbox(self.admin_frame, listvariable=self.admin_str_users, height=15)
            self.admin_user_list.grid(row=1, rowspan=4, column=1, columnspan=2)

    def take_exam(self):
        self.current_exam = self.DB.get_single_exam(self.view_exams_list.get(self.view_exams_list.curselection())[0])
        self.hide_frames()
        self.take_exam_frame = Frame(self, style="BW.TFrame")
        self.take_exam_frame.pack()
        self.take_exam_title = Label(self.take_exam_frame, style="BW.TLabel", text="Test: " + self.current_exam[0][-2])
        self.take_exam_title.grid(row=1, column=1, columnspan=2)
        self.present_questions()

    def present_questions(self):
        row_place, col_place = 2, 1
        self.questions_lbls, self.ans_str_entry_vars, self.ans_entries, self.ans_str_radio_vars =\
            [], [], [], []
        self.exam_questions = []
        self.ans_radios = []
        mc_ans_var_present = True
        mc_ques_count, mc_ans_end, mc_ans_begin = 0, 0, 0
        for i in range(len(self.current_exam)):
            current_question = self.current_exam.pop()
            if current_question[0] + current_question[1] == 'examtitle':
                break
            self.exam_questions.append(current_question)
            if current_question[0] + current_question[1] == 'MCquestion':
                mc_ans_var_present = True
                self.questions_lbls.append(Label(self.take_exam_frame, style="BW.TLabel",
                                                 text="Question: " + current_question[3]))
                self.questions_lbls[-1].grid(row=row_place, column=col_place)
                row_place +=1
                for j in range(len(self.ans_radios[mc_ans_begin:])):
                    self.ans_radios[mc_ans_begin+j].grid(row=row_place, column=col_place)
                    row_place += 1
                mc_ans_begin = mc_ans_end
            if current_question[0] + current_question[1] == 'MCanswer':
                if mc_ans_var_present:
                    self.ans_str_radio_vars.append(StringVar())
                    mc_ans_var_present = False
                # Need to add a value parameter assignment so that I can later evaluate question for correct answer
                self.ans_radios.append(Radiobutton(self.take_exam_frame, variable=self.ans_str_radio_vars[-1],
                                                   text=current_question[3][8:], value=mc_ans_end))
                mc_ans_end += 1
            if current_question[0] + current_question[1] == 'TFquestion':
                self.questions_lbls.append(Label(self.take_exam_frame, style="BW.TLabel",
                                                 text="Question: " + current_question[3]))
                self.ans_str_radio_vars.append(StringVar())
                self.ans_radios.append(Radiobutton(self.take_exam_frame, variable=self.ans_str_radio_vars[-1],
                                                   text="False", value="false"))
                self.ans_radios.append(Radiobutton(self.take_exam_frame, variable=self.ans_str_radio_vars[-1],
                                                   text="True", value="true"))
                mc_ans_end += 2
                self.questions_lbls[-1].grid(row=row_place, column=col_place)
                row_place += 1
                self.ans_radios[-1].grid(row=row_place, column=col_place)
                row_place += 1
                self.ans_radios[-2].grid(row=row_place, column=col_place)
                row_place += 1
                mc_ans_begin = mc_ans_end
            if current_question[0] + current_question[1] == 'FIBquestion':
                self.questions_lbls.append(Label(self.take_exam_frame, style="BW.TLabel",
                                                 text="Question: " + current_question[3]))
                self.ans_str_entry_vars.append(StringVar())
                self.ans_entries.append(Entry(self.take_exam_frame, textvariable=self.ans_str_entry_vars[-1]))
                self.questions_lbls[-1].grid(row=row_place, column=col_place)
                row_place += 1
                self.ans_entries[-1].grid(row=row_place, column=col_place)
                row_place += 1


    def create_exam(self):
        self.hide_frames()
        self.ques_count = 1
        self.new_exam_frame = Frame(self, style="BW.TFrame")
        self.exam = ['exam title '], []
        self.exam_name_str = StringVar()
        self.exam_name_label = Label(self.new_exam_frame, style="BW.TLabel", text="Please enter name of the exam.")
        self.exam_name = Entry(self.new_exam_frame, textvariable=self.exam_name_str)
        self.exam_users = []
        self.ques_count_lbl = Label(self.new_exam_frame, style="BW.TLabel", text="Question #: " +
                                                                                 str(self.ques_count + 1))
        self.q_label = Label(self.new_exam_frame, style="BW.TLabel", text="Please enter question text:")
        self.q_str = StringVar()
        self.q_input = Entry(self.new_exam_frame, textvariable=self.q_str, width=20)
        self.q_radio_str = IntVar()
        self.q_radio_str.set(2)
        self.q_radio = {}
        self.q_radio[0] = Radiobutton(self.new_exam_frame, text="True/False", variable=self.q_radio_str,
                                      value=0, command=self.new_exam_tf)
        self.q_radio[1] = Radiobutton(self.new_exam_frame, text="Multiple Choice", variable=self.q_radio_str,
                                      value=1, command=self.new_exam_MC)
        self.q_radio[2] = Radiobutton(self.new_exam_frame, text="Fill in the Blank", variable=self.q_radio_str,
                                      value=2, command=self.new_exam_FIB)
        self.finished = Button(self.new_exam_frame, style="BW.TButton", text="Finished", command=self.exam_to_db)
        self.users_strs = StringVar(value=self.DB.get_users())
        self.view_users_lst = Listbox(self.new_exam_frame, listvariable=self.users_strs, selectmode=tkinter.MULTIPLE, height=10)
        self.user_instructions = Label(self.new_exam_frame, style="BW.TLabel", text="Select the user(s) who this exam"
                                                                 "\nshould be assigned to.")
        self.new_exam_frame.grid(row=1, column=1)
        self.exam_name_label.grid(row=1, column=1, rowspan=1, columnspan=2)
        self.exam_name.grid(row=2, column=1, columnspan=2)
        self.ques_count_lbl.grid(row=3, column=1)
        self.q_label.grid(row=4, rowspan=1, column=1, columnspan=2)
        self.q_input.grid(row=5, column=1, columnspan=2)
        self.q_radio[0].grid(row=1, column=3)
        self.q_radio[1].grid(row=1, column=4)
        self.q_radio[2].grid(row=1, column=5)
        self.finished.grid(row=6, column=5)
        self.view_users_lst.grid(row=1, rowspan=6, column=6)
        self.user_instructions.grid(row=7, column=6, rowspan=2)
        self.new_exam_FIB()

    def draw_exam_current_questions(self, exam_frame):
        self.current_quests = Canvas(exam_frame, background="#ffffff")
        self.current_quests.grid(row=1, column=7, rowspan=7)
        self.quests_scroll = Scrollbar(exam_frame, orient=VERTICAL, command=self.current_quests.yview)
        self.quests_scroll.grid(row=1, column=8, rowspan=7, sticky=(N,S))
        self.current_quests.configure(yscrollcommand=self.quests_scroll.set)
        self.current_quests.bind('<Configure>', lambda e: self.current_quests.configure(scrollregion=self.current_quests
                                                                                        .bbox('all')))
        self.current_quests_inner = Frame(self.current_quests)
        self.current_quests.create_window((0,0), window=self.current_quests_inner, anchor="nw")
        #for i in range(35):
            #Label(self.current_quests_inner, text="This is test label #: " + str(i)).grid(row=i, column=1)
        self.questions_text_radio = []
        self.questions_radio_str = IntVar()
        print("Length of exam questions is: " + str(len(self.exam[1])))
        if len(self.exam[1]) > 1:
            previous_q_count = 0
            #This for loop may need to be amended to account for a out of index/ display exam title as a question
            for i in range(len(self.exam[1])):
                question_text = self.exam[1][i]
                print(question_text[1:9])
                if question_text[1:9] == "question":
                    question_text = question_text[10:]
                    print("2x: " + question_text)
                    self.questions_text_radio.append(Radiobutton(self.current_quests_inner, text=question_text,
                                                             variable=self.questions_radio_str, value=i,
                                                                 command=self.draw_expand_previous_question))
                    self.questions_text_radio[previous_q_count].grid(row=previous_q_count, column=1)
                    previous_q_count += 1
                    print("Question count should be: " + str(previous_q_count ))
            self.delete_question = Button(self.current_quests_inner, text="Delete", command=self.pop_question)
            self.delete_question.grid(row=previous_q_count+1, column=1)
            self.edit_question_btn = Button(self.current_quests_inner, text="Edit", command=self.edit_question)
            self.edit_question_btn.grid(row=previous_q_count+1, column=2)

    def redraw_exam_current_questions(self):
        print("Attempting to redraw the previous questions widget")
        try:
            if self.current_quests.winfo_exists():
                self.current_quests.destroy()
                print("Destroyed previous questions widget")
        except AttributeError: pass
        try:
            if self.quests_scroll.winfo_exists():
                self.quests_scroll.destroy()
        except AttributeError: pass
        self.draw_exam_current_questions(self.new_exam_frame)

    def get_next_quest_index(self):
        for i in self.exam[1][self.questions_radio_str.get()+1:]:
            if i[1:9] == "question":
                print("Next questions index is: " + str(self.exam[1].index(i)))
                print(i)
                return self.exam[1].index(i)

    def pop_question(self):
        self.ques_count -= 1
        for j in self.exam[1]:
            print(j)
        for i in self.exam[0][self.questions_radio_str.get() : self.get_next_quest_index()]:
            print("Deleteing: " + i)
            self.exam[0].pop(self.exam[0].index(i))
        for k in self.exam[1][self.questions_radio_str.get() : self.get_next_quest_index()]:
            print("Deleteing: " + k)
            self.exam[1].pop(self.exam[1].index(k))
        self.redraw_exam_current_questions()

    def draw_expand_previous_question(self):
        for i in range(len(self.exam[1])):
            line = self.exam[1][i]
            if line[1:9] == "question" and self.questions_radio_str.get() == i:
                print("Exam index is: " + str(i))
                for j in self.questions_text_radio:
                    if j.cget("value") == self.questions_radio_str.get():
                        print(j.cget("text"))

    def edit_question(self):
        n = self.questions_radio_str.get()
        if self.exam[0][n][0:2] == 'MC':
            print("This is a multiple choice question")
        elif self.exam[0][n][0:2] == 'TF':
            print(self.exam[1][n+1].split(' ')[-1])
            self.edit_tf(self.exam[1][n][10:], self.exam[1][n+1].split(' ')[-1], self.exam[0][n][-1])

    def edit_tf(self,quest, answ, count):
        self.set_question_count_lbl(count)
        self.hide_ques_input()
        try:
            if self.q_input.winfo_exists():
                self.q_input.destroy()
                self.q_str = StringVar()
                self.q_str.set(quest)
                self.q_input = Entry(self.new_exam_frame, textvariable=self.q_str, width=20)
                self.q_input.grid(row=5, column=1, columnspan=2)
        except AttributeError: pass
        self.TF_str = StringVar()
        self.TF_str.set(answ)
        self.true_radio = Radiobutton(self.new_exam_frame, text="True", variable=self.TF_str, value="true")
        self.false_radio = Radiobutton(self.new_exam_frame, text="False", variable=self.TF_str, value="false")
        self.save_tf = Button(self.new_exam_frame, style="BW.TButton", text="Save", command=self.save_to_exam_tf)
        self.true_radio.grid(row=3, column=3)
        self.false_radio.grid(row=4, column=3)
        self.save_tf.grid(row=7, column=3)
        self.pop_question()

    def hide_ques_input(self):
        try:
            if self.ans_FIB_lbl.winfo_exists():
                self.ans_FIB_lbl.destroy()
        except AttributeError: pass
        try:
            if self.ans_FIB.winfo_exists():
                self.ans_FIB.destroy()
        except AttributeError: pass
        try:
            for i in range(len(self.ques_multic_lbl)):
                if self.ques_multic_lbl[i].winfo_exists():
                    self.ques_multic_lbl[i].destroy()
        except AttributeError: pass
        except IndexError: pass
        try:
            for i in range(len(self.ques_multic_input)):
                if self.ques_multic_input[i].winfo_exists():
                    self.ques_multic_input[i].destroy()
        except AttributeError: pass
        except IndexError: pass
        try:
            if self.ans_limit_lbl.winfo_exists():
                self.ans_limit_lbl.destroy()
        except AttributeError: pass
        try:
            if self.ans_limit_opt.winfo_exists():
                self.ans_limit_opt.destroy()
        except AttributeError: pass
        try:
            if self.save_ques_FIB_btn.winfo_exists():
                self.save_ques_FIB_btn.destroy()
        except AttributeError: pass
        try:
            if self.save_exam_mc.winfo_exists():
                self.save_exam_mc.destroy()
        except AttributeError: pass
        try:
            if self.true_radio.winfo_exists():
                self.true_radio.destroy()
        except AttributeError: pass
        try:
            if self.false_radio.winfo_exists():
                self.false_radio.destroy()
        except AttributeError: pass
        try:
            if self.save_tf.winfo_exists():
                self.save_tf.destroy()
        except AttributeError: pass

    def update_question_count_lbl(self):
        try:
            if self.ques_count_lbl.winfo_exists():
                self.ques_count_lbl.destroy()
                self.ques_count_lbl = Label(self.new_exam_frame, style="BW.TLabel", text="Question #: " +
                                                                                         str(self.ques_count))
                self.ques_count_lbl.grid(row=3, column=1)
        except AttributeError: pass

    def set_question_count_lbl(self, count):
        try:
            if self.ques_count_lbl.winfo_exists():
                self.ques_count_lbl.destroy()
                self.ques_count_lbl = Label(self.new_exam_frame, style="BW.TLabel", text="Question #: " +
                                                                                         str(count))
                self.ques_count_lbl.grid(row=3, column=1)
        except AttributeError:
            pass

    def convert_exam_title(self):
        try:
            if self.exam_name.winfo_exists():
                print("Exam title exists")
                exam_title = self.exam_name.get()
                print("Exam title is " + self.exam_name.get())
                self.exam[1].append(exam_title)
                self.exam_name.destroy()
                print("Exam name entry widget destroyed")
            if self.exam_name_label.winfo_exists():
                self.exam_name_label.destroy()
                self.exam_name_label = Label(self.new_exam_frame, style="BW.TLabel", text="Exam Title: " +
                                             exam_title)
                self.exam_name_label.grid(row=1, column=1, columnspan=2)
            if self.ques_count_lbl.winfo_exists():
                self.ques_count_lbl.destroy()
                self.ques_count_lbl = Label(self.new_exam_frame, style="BW.TLabel", text="Question #: " +
                                                                                         str(self.ques_count + 1))
                self.ques_count_lbl.grid(row=3, column=1)
        except AttributeError as z:
            print(z)

    def new_exam_tf(self):
        self.hide_ques_input()
        self.update_question_count_lbl()
        self.redraw_question()
        self.redraw_exam_current_questions()
        self.TF_str = StringVar()
        self.TF_str.set("true")
        self.true_radio = Radiobutton(self.new_exam_frame, text="True", variable=self.TF_str, value="true")
        self.false_radio = Radiobutton(self.new_exam_frame, text="False", variable=self.TF_str, value="false")
        self.save_tf = Button(self.new_exam_frame, style="BW.TButton", text="Save", command=self.save_to_exam_tf)
        self.true_radio.grid(row=3, column=3)
        self.false_radio.grid(row=4, column=3)
        self.save_tf.grid(row=7, column=3)

    def save_to_exam_tf(self):
        if self.exam_name.winfo_exists():
            self.convert_exam_title()
        self.exam[0].append("TF question " + str(self.ques_count))
        self.exam[1].append(" question " + self.q_input.get())
        self.exam[0].append("TF answer " + str(self.ques_count))
        self.exam[1].append(" answer " + self.TF_str.get())
        self.save_success_tf = tkinter.messagebox.Message(self.new_exam_frame, title="Saved",
                                                          message="Question has been saved!")
        self.save_success_tf.show()
        self.new_exam_tf()
        self.ques_count += 1

    def new_exam_MC(self):
        self.hide_ques_input()
        self.update_question_count_lbl()
        self.redraw_question()
        self.redraw_exam_current_questions()
        self.ques_multic_lbl = {}
        self.ques_multic_input = {}
        self.ques_multic_str = {}
        self.ans_limit_lbl = Label(self.new_exam_frame, style="BW.TLabel", text="Answer count:")
        self.ans_limit_var = [2, 2, 3, 4, 5]
        self.ans_limit = IntVar()
        self.ans_limit.set(3)
        # Option menu only allows positional values, poorly implement, can't specific arguement name
        self.ans_limit_opt = OptionMenu(self.new_exam_frame, self.ans_limit, *self.ans_limit_var,
                                        command=self.update_new_exam_mc)
        self.ans_limit_lbl.grid(row=6, column=1)
        self.ans_limit_opt.grid(row=6, column=2)
        self.save_exam_mc = Button(self.new_exam_frame, text="Save question", command=self.save_to_exam_mc)
        self.save_exam_mc.grid(row=7, column=4)

    def update_new_exam_mc(self, opt=None):
        try:
            for i in range(len(self.ques_multic_lbl)):
                if self.ques_multic_lbl[i].winfo_exists():
                    self.ques_multic_lbl[i].destroy()
        except AttributeError: pass
        except IndexError: pass
        try:
            for i in range(len(self.ques_multic_input)):
                if self.ques_multic_input[i].winfo_exists():
                    self.ques_multic_input[i].destroy()
        except AttributeError: pass
        except IndexError: pass
        try:
            if self.q_input.winfo_exists():
                self.q_input.delete(0, 'end')
        except AttributeError: pass
        self.ques_multic_limit = self.ans_limit.get()
        if self.ques_multic_limit > 0 & self.ques_multic_limit < 10:
            tmp = 0
            while tmp < self.ques_multic_limit:
                self.ques_multic_str[tmp] = StringVar()
                self.ques_multic_lbl[tmp] = Label(self.new_exam_frame, style="BW.TLabel",
                                                  text="Answer number " + str(tmp+1) + ":")
                self.ques_multic_input[tmp] = Entry(self.new_exam_frame, textvariable=self.ques_multic_str[tmp])
                tmp = tmp+1
        for i in range(self.ques_multic_limit):
            print(i)
            self.ques_multic_lbl[i].grid(row=i+2, column=3)
            self.ques_multic_input[i].grid(row=i+2, column=4, columnspan=2)
        self.redraw_question()
        self.redraw_exam_current_questions()

    def save_to_exam_mc(self):
        exam_title = str()
        try:
            if self.exam_name.winfo_exists():
                self.convert_exam_title()
        except AttributeError: pass
        try:
            # add a check to see weather input fields are empty
            self.exam[0].append("MC question " + str(self.ques_count))
            self.exam[1].append(" question " + self.q_str.get())
            for i in self.ques_multic_input:
                print("Appending answer number: " + str(i))
                self.exam[0].append("MC answer " + str(self.ques_count))
                self.exam[1].append(" answer " + str(i) + ' ' + str(self.ques_multic_input[i].get()))
            for j in self.exam[0]:
                print(j)
            for k in self.exam[1]:
                print(k)
            confirmMsg = tkinter.messagebox.Message(self.new_exam_frame, title="Saved", message="Question has been saved")
            confirmMsg.show()
            self.update_new_exam_mc()
            self.ques_count += 1

        except AttributeError as z:
            print(z)

    def new_exam_FIB(self):
        self.hide_ques_input()
        self.update_question_count_lbl()
        self.redraw_question()
        self.redraw_exam_current_questions()
        self.ans_FIB_lbl = Label(self.new_exam_frame, style="BW.TLabel", text="Enter the correct answer")
        self.ans_FIB_str = StringVar()
        self.ans_FIB = Entry(self.new_exam_frame, textvariable=self.ans_FIB_str, width=30)
        self.save_ques_FIB_btn = Button(self.new_exam_frame, style="BW.TButton", text="Add question to exam",
                                        command=self.save_to_exam_fib)
        self.ans_FIB_lbl.grid(row=2, column=3, columnspan=2)
        self.ans_FIB.grid(row=3, column=3, columnspan=2)
        self.save_ques_FIB_btn.grid(row=4, column=4)

    def save_to_exam_fib(self):
        if self.exam_name.winfo_exists():
            self.convert_exam_title()
        self.exam[0].append("FIB question " + str(self.ques_count))
        self.exam[1].append(" question " + self.q_input.get())
        self.exam[0].append("FIB answer " + str(self.ques_count))
        self.exam[1].append(" answer " + self.ans_FIB_str.get())
        self.save_success_tf = tkinter.messagebox.Message(self.new_exam_frame, title="Saved",
                                                          message="Question has been saved!")
        self.save_success_tf.show()
        self.new_exam_FIB()
        self.ques_count += 1

    def exam_to_db(self):
        self.exam_users_ndex = self.view_users_lst.curselection()
        for i in self.exam_users_ndex:
            self.exam_users.append(self.view_users_lst.get(i)[0] + ' ' + self.view_users_lst.get(i)[1])
        for i in self.exam_users:
            print(i)
        self.DB.save_exam(self.exam)

    def redraw_question(self):
        try:
            if self.q_input.winfo_exists():
                self.q_input.destroy()
                self.q_str = StringVar()
                self.q_input = Entry(self.new_exam_frame, textvariable=self.q_str, width=20)
                self.q_input.grid(row=5, column=1, columnspan=2)
        except AttributeError: pass

    def hide_frames(self):
        print("Hiding all frames")
        try:
            if self.users_frame.winfo_exists():
                self.users_frame.destroy()
        except AttributeError: pass
        try:
            if self.exams_frame.winfo_exists():
                self.exams_frame.destroy()
        except AttributeError: pass
        try:
            if self.admin_frame.winfo_exists():
                self.admin_frame.destroy()
        except AttributeError: pass
        try:
            if self.new_exam_frame.winfo_exists():
                self.new_exam_frame.destroy()
                print("Hiding create exam frame")
        except AttributeError: pass
        try:
            if self.take_exam_frame.winfo_exists():
                self.take_exam_frame.destroy()
        except AttributeError: pass

class Question():
    def __init__(self, text, answer, response, type):
        self.text = text
        self.answer = answer
        self.response = response
        self.type = type

