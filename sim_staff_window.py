from datetime import datetime
from tkinter import *
import language_dictionary as ld
import query
from sim_staff_widgets import widgets as wd
import working_data
import simulation_time as sim_time
import task_reassign
from icecream import ic
from ui_data import ui_data
import communicator


class manage_window:
    """The manage window class i
    :param self.root: a reference to the root window for the UI
    :type self.root: Tkinter window
    :param self.home: reference to the sim_staff_window_manager.py module so functions can be called within manage_window
    :type self.home: module reference
    :param self.log_window: a reference to the log window used for displaying data received from task window
    :type self.log_window: Tkinter window
    :param self.window: the window of this specific staffer
    :type: self.window: Tkinter window
    :param self.working_token: use to reference the token value of a task being worked on by the staffer
    :type self.working_token: int
    :param self.sim_time: a reference to the system_time module
    :type self.sim_time: Module reference
    :param self.staff_name: the name of the staff member who owns the window
    :type self.staff_name: str
    :param self.staff_id: and identification of the staffers role
    :type self.staff_id: str
    :param self.language: the language preferences of the staff member
    :type self.language: str
    :param self.device_id: the unique identification of the staff member's screen
    :type self.device_id: int
    :param self.column_padding: a column padding length for spacing widgets in the staffers screen
    :type self.column_padding: int
    :param self.width: a preset width used for sizing widgets
    :type self.width: int
    :param self.row_padding: a row padding length for spacing widgets in the staffers screen
    :type self.row_padding: int
    :param self.row_current: value used for managing placement to the grid layout of the home screen
    :type self.row_current: int
    :param self.task_row: value used for managing the placement of widgets in the task window
    :type self.task_row: int
    :param self.value_holder: a list created to store the values of widget items once they have been processed
    :type self.value_holder: list
    :param self.widgets: a list created to store the appropriate values for the widgets added to the task screen
    :type self.widgets: list
    :param self.token_list: storage of the current list of tokens TO BE USED FOR TIMED POLL OF PEO_Q
    :type self.token_list: list
    :param self.token_start_time: a dictionary associating the token value with the time arrived
    :type self.token_start_time: dictionary
    :param self.token_time_label: a dictionary where the token value is used to determine the label associated with a token
    :type self.token_time_label: dictionary
    :param self.tokens_completed: the tokens, which correspond to tasks, completed by the staffer
    :type self.tokens_completed: list
    :param self.at_home: a value to store whether the user is currently in the home screen or not FOR POLLING EVERY 10 seconds
    :type self.at_home: bool
    :param self.widget_creator: a reference for the module used to create the widgets displayed on the UI
    :type self.widget_creator: module
    """

    def __init__(self, window, staffer, device_id, root, home):
        """The basic constructor for the manage_window module
        :param window: the window of this specific staffer
        :type: window: Tkinter window
        :param staffer: the information about the staffer who has logged into this window
        :type staffer: list
        :param device_id: the unique id number of the device that is logged into a window
        :type device_id: int
        :param root: a reference to the root window for the UI
        :type root: Tkinter window
        :param home: reference to the sim_staff_window_manager.py module so functions can be called within manage_window
        :type home: module reference"""
        self.root = root
        self.home = home
        self.window = window
        self.window.unbind('<Return>')
        self.working_token = None
        self.staff_name = staffer.get('~1')
        self.staff_job = staffer.get('~23')
        self.language = staffer.get('~100')
        self.man_lang = '~101'
        self.device_id = device_id
        self.column_padding = 80
        self.width = 14
        self.row_current = 0
        self.task_row = 0
        self.value_holder = []
        self.widgets = []
        self.at_home = True
        self.dat = ui_data()
        self.widget_creator = wd(root, self.language, self.window)
        self.task_re = task_reassign.task_reassign(self.language, self.window, self.home, self.device_id)

    def get_device_id(self):
        """Returns the device id of a staffers screen"""
        return self.device_id

    def poll_controller(self):
        """This function checks for new tasks (based on the device_id of the staffer) every second to see if the
        staffer has any new tasks to complete and populates those tasks to their home screen."""
        tasks = communicator.get_tasks(self.device_id)
        if tasks:
            for task in tasks:
                if self.dat.should_display(task, tasks) and self.at_home:
                    # self.send_data(task, tasks.get(task))
                    # self.add_column_headers()
                    self.refresh_home()
                self.dat.should_update_time(task, self.at_home)

        self.root.after(1000, self.poll_controller)

    def refresh_home(self):
        """This function simply refreshes the staffers home screen after completing a task"""
        tasks = communicator.get_tasks(self.device_id)
        self.at_home = True
        self.clear_window()
        self.set_home()
        if tasks:
            self.dat.token_time_label.clear()
            self.dat.name_row.clear()
            tokens = self.dat.organize_tasks(tasks, self.device_id)
            ic(tokens)
            for token in tokens:
                self.send_data(token, tasks.get(token))

    def send_data(self, token, raw_data):
        """This function sends a token and the necessary data for a task to a task screen to be completed by the staffer
        :param token: randomly generated value used to distinguish the task
        :type token: int
        :param raw_data: the data needed for creating the task screen of the user processed by the function
        :type raw_data: list"""
        if self.at_home:
            task_id = raw_data[3]
            person_id = raw_data[0]
            task_window_info = raw_data[5]
            priority = raw_data[2]
            status = raw_data[8]
            self.populate_task(task_id, person_id, task_window_info, token, priority, status)
            self.row_current += 1

    def populate_task(self, task_id, person_id, task_window_info, token, priority, status):
        """This function adds the buttons for the staffer's task to the task window.
        :param task_id: the value that corresponds to the task that the staffer needs to complete
        :type task_id: str
        :param person_id: the unique identification number of the person being processed by the staff member
        :type person_id: str
        :param task_window_info: contains a list of widget elements to be added to the task window for the staff member
        :type task_window_info: list
        :param token: the unique token id for the information handled by the staff member
        :type token: int
        :param priority: the current priority of a task
        :type priority: int
        :param status: the current status of the task being processed
        :type status: str (~vocab)
        """
        name = query.adat_person_key(person_id, '~1')[1]  # maybe list handling should be done in query.py
        if not self.dat.check_in_display(name):
            label_name = Label(self.window, text=name, font=self.widget_creator.medium_font)
            label_name.grid(column=0, row=self.row_current, columnspan=3, sticky=W)
        self.row_current += 1
        btn_process: Button = Button(self.window, text='=>',
                                     command=lambda: self.write_task_screen(task_window_info, person_id, token,
                                                                            task_id, priority),
                                     fg="black", bg="gray", width=self.width - 10)
        btn_process.grid(column=4, row=self.row_current, sticky=E)

        self.dat.add_token_row_name(self.row_current, name)
        btn_log: Button = Button(self.window, text=ld.get_text_from_dict(self.language, '~13'), width=self.width,
                                 command=lambda: self.view_log_data(token), fg="black", bg="gray")
        btn_log.grid(column=0, row=self.row_current)

        self.add_person_to_tasks(priority, token, status)

    def view_log_data(self, token):
        """creates the a window where the user is able to view the information in the log
        :param token: the unique token id for the information handled by the staff member
        :type token: int
        """

        def close():
            """destroy the log window after it has close button has been selected"""
            log_screen.destroy()

        # create the log viewer screen directly above the current window
        log_screen = Toplevel(self.root)
        log_screen.geometry(self.window.geometry())
        log_row = 1
        self.widget_creator.log_window_header(log_screen)
        try:  # attempt to display the log data
            for data in working_data.log_dict.get(token):
                self.widget_creator.display_log_info(log_screen, data, log_row)
                log_row += 1
        except:  # if there is no data disply no log data
            for widget in log_screen.winfo_children():
                widget.destroy()
            Label(log_screen, text='NO LOG DATA', font=self.widget_creator.larger_font).grid(row=0, column=0)
        Button(log_screen, text=ld.get_text_from_dict(self.language, '~54'), command=close,
               fg="black", bg="gray", height=1, width=10
               ).grid(sticky=S)

    def set_home(self):
        """This function sets up the home screen for the staffer creating the windows title and adding the column
        headers."""
        spacer = ' ' * (53 - len(self.staff_name + '' + ld.get_text_from_dict(self.language, self.staff_job)))
        self.window.title(self.staff_name + spacer + ld.get_text_from_dict(self.man_lang, self.staff_job))
        self.add_column_headers()

    def add_column_headers(self):
        """This function adds the headers for the tasks in the home screen"""
        label_priority = Label(self.window, text='', width=self.width, borderwidth=3)
        label_priority.grid(column=0, row=self.row_current, sticky=W)
        label_priority = Label(self.window, text=ld.get_text_from_dict(self.language, '~49')[0:3] + '  ',
                               font=self.widget_creator.medium_font, width=self.width - 10, borderwidth=3,
                               relief=GROOVE)
        label_priority.grid(column=1, row=self.row_current, sticky=W)
        label_status = Label(self.window, text=ld.get_text_from_dict(self.language, '~48') + '  ',
                             font=self.widget_creator.medium_font, width=self.width, borderwidth=3, relief=GROOVE)
        label_status.grid(column=2, row=self.row_current, sticky=W)
        label_time = Label(self.window, text=ld.get_text_from_dict(self.language, '~10') + '  ',
                           font=self.widget_creator.medium_font, width=self.width, borderwidth=3, relief=GROOVE)
        label_time.grid(column=3, row=self.row_current, sticky=W)
        self.row_current += 1

    def add_person_to_tasks(self, priority, token, status):
        """This function adds the name of a person who needs to be processed by the staffer
        :param priority: the priority level of a task
        :type priority: int
        :param token: the token value of the task in question
        :type token: int
        :param status: the current status of the task being processed
        :type status: str (~vocab)"""

        priority_color = {1: "red", 2: "blue", 3: "black"}

        label_priority = Label(self.window, text=priority, font=self.widget_creator.medium_font, width=self.width - 10,
                               fg=priority_color.get(priority), borderwidth=3, relief=GROOVE)
        label_priority.grid(column=1, row=self.row_current)
        label_status = Label(self.window, text=ld.get_text_from_dict(self.language, status), width=self.width,
                             font=self.widget_creator.medium_font, borderwidth=3, relief=GROOVE)
        label_status.grid(column=2, row=self.row_current)
        label_time = Label(self.window, text=self.dat.time_diff_start_time(token), width=self.width,
                           font=self.widget_creator.medium_font, borderwidth=3, relief=GROOVE)
        label_time.grid(column=3, row=self.row_current)

        self.dat.add_start_time_label(token, label_time)
        self.dat.update_repost_time(token)

    def write_task_screen(self, task_window_info, person_id, token, task_id, priority):
        """This function makes calls to widgets module to display widgets in the UI
        :param task_window_info: list of task widgets that need to be added to the task screen
        :type task_window_info: list
        :param person_id: the unique identity number of the person being processed
        :type person_id: str
        :param token: unique token id for the given task
        :type token: int
        :param task_id: ~vocab reference to the task that needs to be completed by the staffer
        :type task_id: str
        :param priority: the current priority of a task
        :type priority: int
        """
        self.at_home = False
        self.clear_window()
        self.working_token = token
        for item in task_window_info:
            if item[0] == 'Fixed':
                self.widget_creator.add_label(item[1], person_id)
            elif item == 'PersonHeader':
                self.widget_creator.add_person_header(person_id)
            elif item == 'TaskHeader':
                self.widget_creator.add_task_header(task_id)
            elif item[0] == 'ModifyEntry':
                self.widget_creator.add_entry_with_text(item[1], person_id)
            elif item[0] == 'EmptyEntry':
                self.widget_creator.add_entry(item[1:])
            elif item[0] == 'DropDown':
                self.widget_creator.add_drop_down(item[1:])
            elif item[0] == 'CheckBoxes':
                self.widget_creator.add_check_boxes(item[1:])
            elif item[0] == 'Button':
                self.add_button_submit(item[1])
        self.widget_creator.priority_radio_buttons(priority)
        self.task_re.create_buttons(self.widget_creator.task_row, token, self.widget_creator.get_priority())

    def clear_window(self):
        """This function clears the window that it is given allowing it to be a blank canvas before the window
        is repopulated with different widgets
        """
        for widget in self.window.winfo_children():
            widget.destroy()

    def add_button_submit(self, value):
        """this method adds a submit button to a given window
        :param value: a dictionary reference to a value that needs to be written in the form a label to the screen
        :type value: str (~vocab)

        """
        btn_submit = Button(self.window, text=ld.get_text_from_dict(self.language, value),
                            command=lambda: self.submit_btn_listener(),
                            fg="black", bg="light gray", height=1, width=10)
        btn_submit.grid(row=self.widget_creator.task_row, column=1, sticky=E, columnspan=3)
        self.task_row += 1

    def return_home(self):
        """This function returns the staffer to their home screen without completing the job so the person in question
        will remain in their task screen"""
        self.at_home = True
        self.value_holder.clear()
        self.widget_creator.clear_widget_data()
        self.refresh_home()

    def submit_btn_listener(self):
        """an action listener for the submit button.  It is in charge of sending data back to the controller to be
        that is later processed by the protocol engine.  Because of this I have implemented a simple check to
        make sure that the data being given back has appropriate values that can be processed by the PE.
        After a task has been successfully completed the appropriate data is sent back to the controller.  If it
        is not completed successfully, the staffer returns to their task screen after receiving a error on screen
        """
        self.manage_widgets()
        data_return = self.add_to_log()
        self.widgets.clear()
        self.clear_window()
        if data_return == 'NO DATA GIVEN':
            self.clear_window()
            Label(self.window, text="INCORRECT DATA", font='Helvetica 24 bold').pack()
            self.root.after(1000, self.return_home)

        else:
            self.at_home = True
            communicator.return_data(self.working_token, data_return)
            self.dat.clear_token(self.working_token)
            self.dat.tokens_completed.append(self.working_token)
            self.working_token = None
            self.widget_creator.clear_widget_data()
            self.task_row = 0
            self.set_home()
            self.refresh_home()

    def add_to_log(self):
        """This function adds the data that will be sent back to the protocol manager to the log window
        print statement is so you can see how the actual value looks in the program not just the log printed version"""
        if len(self.value_holder) == len(self.widgets) and len(self.value_holder) > 0:
            return_data = []
            for _ in range(len(self.value_holder)):
                return_data.append(self.value_holder.pop())
            return return_data
        else:
            return 'NO DATA GIVEN'

    def add_value(self, key, value, units=None):
        """This function adds a key value pair to the stored information retrieved from the widgets in the task screen
        :param key: the key corresponding to a dictionary reference in language_dictionary
        :type key: str
        :param value: the value retrieved from the widget in the task screen
        :type value: int or str"""
        try:
            if float(value):
                self.value_holder.append({'k': key, 'v': float(value), 'vt': 'f', 'units': units})
                # check for expected value
            elif bool(value):
                self.value_holder.append({'k': key, 'v': value, 'vt': 'b', 'units': units})
        except:
            if value[0] == '~':
                self.value_holder.append({'k': key, 'v': value, 'vt': '~', 'units': units})
            else:
                self.value_holder.append({'k': key, 'v': value, 'vt': 's', 'units': units})

    def manage_widgets(self):
        """This function loops through the widgets stored in the task screen for the staffer.  It's job is to retrieve
        the data from the widgets so they can be passed back to the protocol manage and currently prints to the log
        window.  Added exceptions for when there are no values given so empty lists are not added or displayed"""
        widgets = self.widget_creator.return_widget_data()
        for widget in widgets:
            self.widgets.append(widget)
            if widget[0] == '~19':
                try:
                    range = widget[2].get('range')
                    if range[0] <= float(widget[1].get()) <= range[1]:
                        if widget[2].get('vt') == 'f' and float(widget[1].get()):
                            self.add_value(widget[0], widget[1].get(), widget[2].get('units'))
                except:
                    self.clear_window()
                    Label(self.window, text="INCORRECT WEIGHT", font='Helvetica 24 bold').pack()
                    self.root.after(1000, self.return_home)
            elif len(widget) == 3:
                if len(widget[1].get()) > 0:
                    self.add_value(widget[0], widget[2].get(widget[1].get()))
            elif widget[0][0] == '~18':  # if it is a checkbox input
                if widget[1][0].get() == 1:
                    self.add_value(widget[0][0], widget[1][1])
                else:
                    self.widgets.pop()

            else:
                if len(widget[1].get()) > 0:
                    self.add_value(widget[0], widget[1].get())

    def clear_widgets(self):
        """call to clear all of the widgets in the widget creator used by the staffer"""
        self.widget_creator.clear_widget_data()

    def partial_complete(self, token):
        """handles partial completions (namely the pause functionality where a task will be sent back to the staffers
        screen without updating the PE)"""
        self.dat.tokens_completed.append(token)  # MAYBE RETHINK THIS ONE TOO
