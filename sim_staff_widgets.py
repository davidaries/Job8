from datetime import datetime

import language_dictionary as ld
from tkinter import *
from tkinter import font as tk_font
import tkinter as tk
import initial_load_data as ild
import query
from icecream import ic


class widgets:
    """This class manages the various widgets used by the sim_staff_window class.  It contains functions used for
    creating the widgets used in the staffers task screen as well as displaying the log data (when the staffer
    chooses to view the information stored in the log for the task.
    :param self.root: a reference to the tkinter root screen needed to populate windows and use wait functions
    :type self.root: tk window reference
    :param self.language: the preset language '~101', which corresponds to english
    :type self.language: str
    :param self.window: reference to the corresponding tkinter window that has been created used for displaying widgets
    :type self.window: tk window
    :param self.medium_font: a generated font used within the display
    :type self.medium_font: tk_Font
    :param self.larger_font: a generated font used within the display
    :type self.larger_font: tk_Font
    :param self.column_padding: a column padding length for spacing widgets in the staffers screen
    :type self.column_padding: int
    :param self.row_padding: a row padding length for spacing widgets in the staffers screen
    :type self.row_padding: int
    :param self.row_current: value used for managing placement to the grid layout of the home screen
    :type self.row_current: int
    :param self.task_row: value used for managing the placement of widgets in the task window
    :type self.task_row: int
    :param self.width: a preset width used for sizing widgets
    :type self.width: int
    :param self.widgets: a list created to store the appropriate values for the widgets added to the task screen
    :type self.widgets: list
    :param self.priority: the priority of a given token
    :type self.priority: IntVar()
    """
    def __init__(self, root, language, window=None):
        """Sets up the various values needed for sim_staff_widgets to create and format widgets
        :param root: a reference to the tkinter root screen needed to populate windows
        :type root: tk window reference
        :param language: the preset language '~101', which corresponds to english
        :type self.language: str
        :param window: reference to the corresponding tkinter window that has been created
        :type window: tk window reference
        """
        self.root = root
        self.language = language
        self.window = window
        self.medium_font = tk_font.Font(root=root.master, family='Helvetica', size=10, weight=tk_font.BOLD)
        self.larger_font = tk_font.Font(root=root.master, family='Helvetica', size=10, weight=tk_font.BOLD)
        self.column_padding = 80
        self.row_padding = 12
        self.row_current = 2
        self.task_row = 0
        self.width = 14
        self.widgets = []
        self.priority = IntVar()

    def return_widget_data(self):
        """return widget data to be processed
        :return: reference to the widgets created by sim_staff_widgets
        :rtype: list"""
        return self.widgets

    def add_label(self, value, person_id):
        """this function adds a label to a given window
        :param person_id:  identification number of person (11, or 12) for (tina, tony)
        :type person_id: int
        :param value: a dictionary reference to a value that needs to be written in the form a label to the screen
        :type value: str
        """
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, value) + ': ', font=self.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W', columnspan = 2)
        lbl_val = query.adat_person_key(person_id, value)[1]
        lbl_info = Label(self.window, text=ld.get_text_from_dict(self.language, lbl_val), font = self.medium_font)

        lbl_info.grid(row=self.task_row, column=1, ipady=self.row_padding, sticky=S)
        self.task_row += 1

    def add_drop_down(self, value):
        """this function adds a drop down menu to a given window
        :param value: a dictionary reference to a value that needs to be written in the form a label to the screen
        :type value: str
        """
        drop_down_lbl = value[0]
        list_call = value[1]
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, drop_down_lbl) + ': ', font=self.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W')
        choices = ild.choices.get(list_call)
        choices_formatted = []
        choice_dict = {}
        has_long = False
        for choice in choices:  # short list
            if choice[1]:
                choices_formatted.append(ld.get_text_from_dict(self.language, choice[0]))
                choice_dict[ld.get_text_from_dict(self.language, choice[0])] = choice[0]
            else:
                has_long = True
        if has_long:
            choices_formatted.append('_____________')
            for choice in choices:  # long list
                choices_formatted.append(ld.get_text_from_dict(self.language, choice[0]))
                choice_dict[ld.get_text_from_dict(self.language, choice[0])] = choice[0]
        option = StringVar(self.window)
        drop_down = OptionMenu(self.window, option, *choices_formatted)
        drop_down.grid(row=self.task_row, column=1, sticky=W, columnspan = 2)

        self.widgets.append((drop_down_lbl, option, choice_dict))
        self.task_row += 1

    def add_check_boxes(self, value):
        """This function adds a check box to the given window.  As it stands it only places the header for the check
        box but check box functionality will be added in the next update
        :param value: a dictionary reference to a value that needs to be written in the form a label to the screen
        and a str that references the list to be called from data.py
        :type value: list
        """
        cb_label = value[0]
        list_call = value[1]
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, cb_label) + ': ', font=self.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W')
        cb_values = ild.choices.get(list_call)
        for val in cb_values:
            test = ld.get_text_from_dict(self.language, val[0])
            checked = IntVar()
            box = Checkbutton(self.window, text=test, variable=checked,
                              onvalue=1, offvalue=0)
            self.widgets.append((value, [checked, val[0]]))
            box.grid(row=self.task_row, column=1, sticky=W)
            self.task_row += 1
        self.task_row += 1

    def add_entry(self, info):
        """This function adds an entry to the given window.  As it stands it only places the header for the entry box
         but entry box functionality will be added in the next update
        :param info: a dictionary reference to a value that needs to be written in the form a label to the screen
        :type info: str
        """
        value = info[0]
        units = info[1].get('units')
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, value) + ': ', font=self.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W')
        text_entered = Variable
        entry_box = Entry(self.window, textvariable=text_entered)
        self.widgets.append((value, entry_box, info[1]))
        entry_box.grid(row=self.task_row, column=1, sticky='W')
        Label(self.window, text=ld.get_text_from_dict(self.language, units), font = self.medium_font).grid(row=self.task_row, column=2, sticky='W')
        self.task_row += 1

    def add_entry_with_text(self, value, person_id):
        """This function adds an entry with text prefilled to the given window.
         As it stands it only places the header for the entry box
         but entry box functionality will be added in the next update
        :param person_id: identification number of the person in question
        :type person_id: int
        :param value: a dictionary reference to a value that needs to be written in the form a label to the screen
        :type value: str
        """
        phone_number = query.adat_person_key(person_id, '~16')[1]
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, value) + ': ', font=self.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W')
        text_entered = StringVar()
        entry_box = Entry(self.window, textvariable=text_entered)
        entry_box.insert(0, phone_number)
        self.widgets.append((value, entry_box))
        entry_box.grid(row=self.task_row, column=1, sticky='W')
        self.task_row += 1

    def add_task_header(self, task_id):
        """This function adds the task header of the staffer to the display window. After adding, I'm not sure
        this is something we really need but could be useful in the future
        :param task_id: the ~vocab reference of the task that must be completed by the staffer
        :type task_id: str"""
        task = ld.get_text_from_dict(self.language, task_id)
        task_lbl = Label(self.window, text=task, font=self.medium_font)
        task_lbl.grid(row=self.task_row, column=0, columnspan=2, sticky='W')
        self.task_row += 1

    def add_person_header(self, person_id):
        """This function adds the person header to the given window based on the id number of the person given to the
        function.
        :param person_id: the identification number of the person being processed used to intake their data
        :type person_id: int
        """

        name = query.adat_person_key(person_id, '~1')[1]
        sex = query.adat_person_key(person_id, '~14')[1]
        sex = ld.get_text_from_dict(self.language, sex)
        age = query.adat_person_key(person_id, '~15')[1]
        name_lbl = Label(self.window, text=name, font=self.medium_font)
        sex_lbl = Label(self.window, text=sex, font=self.medium_font, width = self.width)
        age_lbl = Label(self.window, text=age, font=self.medium_font, width = self.width)

        name_lbl.grid(row=self.task_row, column=0, sticky='W', columnspan=2)
        sex_lbl.grid(row=self.task_row, column=2, sticky='W')
        age_lbl.grid(row=self.task_row, column=3, sticky='W')
        self.task_row += 1

    def clear_widget_data(self):
        """This function clears all widgets currently present on the screen"""
        self.widgets.clear()

    def log_window_header(self, window):
        """Sets the headers for the log window
        :param window: reference to the log window
        :type window: tk Window"""
        Label(window, text=ld.get_text_from_dict(self.language, '~57'), font=self.medium_font).grid(row=0, column=0,
                                                                                                    ipadx=15, sticky=W)
        Label(window, text=ld.get_text_from_dict(self.language, '~10'), font=self.medium_font).grid(row=0, column=1,
                                                                                                    ipadx=15, sticky=W)
        Label(window, text=ld.get_text_from_dict(self.language, '~58'), font=self.medium_font).grid(row=0, column=2,
                                                                                                    ipadx=15, sticky=W)
        Label(window, text=ld.get_text_from_dict(self.language, '~49'), font=self.medium_font).grid(row=0, column=3,
                                                                                                    ipadx=15, sticky=W)
        Label(window, text=ld.get_text_from_dict(self.language, '~59'), font=self.medium_font).grid(row=0, column=4,
                                                                                                    ipadx=15, sticky=W)

    def display_log_info(self, window, data, r):
        """writes a row of data from from the log to be displayed on the window
        :param window: reference to the log window
        :type window: tk Window
        :param data: a dictionary of references to points of data to be displayed by the log
        :type data: dict
        :param r: the row that this data needs to be written to
        :type r: int
        """
        user = ild.staffers[data.get('user')].get('~1')
        time = datetime.fromtimestamp(int(data.get('time'))).strftime('%H:%M')
        status = ld.get_text_from_dict(self.language, data.get('status'))
        Label(window, text=user, font=self.medium_font).grid(row=r, column=0)
        Label(window, text=time, font=self.medium_font).grid(row=r, column=1)
        Label(window, text=status, font=self.medium_font).grid(row=r, column=2)
        Label(window, text=data.get('priority'), font=self.medium_font).grid(row=r, column=3)
        Label(window, text=data.get('comments'), font=self.medium_font, justify = LEFT, height=3, wraplength=190).grid(row=r, column=4)

    def priority_radio_buttons(self, priority):
        """creates radio buttons for changing the priority of a given task
        :param priority: the current priority of a task
        :type priority: int"""
        self.task_row+=1
        pri_lbl = Label(self.window, text=ld.get_text_from_dict(self.language, '~49'), font=self.medium_font)
        pri_radio_1 = tk.Radiobutton(self.window, text='1', fg="red", variable=self.priority, value=1)
        pri_radio_2 = tk.Radiobutton(self.window, text='2', fg="blue", variable=self.priority, value=2)
        pri_radio_3 = tk.Radiobutton(self.window, text='3', fg="black", variable=self.priority, value=3)
        pri_lbl.grid(row=self.task_row , column=0,sticky=W)
        pri_radio_1.grid(row=self.task_row , column=0, sticky=E)
        pri_radio_2.grid(row=self.task_row , column=1, sticky=S)
        pri_radio_3.grid(row=self.task_row , column=2, sticky=W)
        if priority == 1:
            pri_radio_1.invoke()
        elif priority == 2:
            pri_radio_2.invoke()
        else:
            pri_radio_3.invoke()

    def get_priority(self):
        """returns the priority of a token that may have been changed in the task screen
        :return: the current priority
        :rtype: IntVar"""
        return self.priority
