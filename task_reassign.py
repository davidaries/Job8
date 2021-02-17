import tkinter as tk
from tkinter import *
import language_dictionary as ld
from icecream import ic
import communicator


class task_reassign:
    """The task_reassign class handles the reassignment of tasks, as well as the user's interaction with the commenting
    portion of the log.  This class is called to create buttons with the various reassignment options for the staffer
    displayed at the bottom of their task screen.  When a user selects an option, their screen refreshes with a text box
    for adding comments and other necessary widgets
    :param self.language: the language preference of the device
    :type self.language: str (~vocab)
    :param self.window: the window being used to display the buttons and the log interaction interface
    :type self.window: TK Window
    :param self.home: a reference to the sim_staff_window_manager used to refresh the device screen
    :type self.home: TK Window
    :param self.device_id: the unique device id of the staffer
    :type self.device_id: str
    :param self.alternate_staff: a field used to the name of the alternate staffer when a task is being reassigned
    :type self.alternate_staff: StringVar
    :param self.staff_change: a flag used to check if there is a staff change requested by the task reassign
    :type self.staff_change: bool
    :param self.priority: the priority level of the task being processed
    :type self.priority: int
    :param self.width: a value used for setting the sizes of the buttons
    :type self.width: int
    :param self.xpad: a value used for adding padding to various buttons
    :type self.xpad: int"""

    def __init__(self, language, window, home, device_id):
        """Used to set up various variables used for program execution as described above
        :param language: the language of the staffer
        :type language: str (~vocab)
        :param window: reference to the window where the various widgets are being written
        :type window: TK Window
        :param home: a reference to the sim_staff_window_manager used to refresh the device screen
        :type home: TK Window
        :param device_id: the unique device id of the staffer's device
        :type device_id: str
        """
        self.language = language
        self.window = window
        self.home = home
        self.device_id = device_id
        self.alternate_staff = None
        self.staff_change = False
        self.priority = None
        self.width = 14
        self.xpad = 3

    def create_buttons(self, row, token, priority):
        """create_buttons is in charge of setting up the buttons found at the bottom of the task screen.  It also
        creates links to the various button listeners used to execute the tasks described by the buttons
        :param row: the starting row for the button placement in the windows grid
        :type row: int
        :param token: the unique token id of the task
        :type token: int
        :param priority: the priority level of the incoming task
        :type priority: int
        """
        self.priority = priority
        for _ in range(2):  # space buttons need to figure out a better way to do this
            row += 1
            Label(self.window, text=' ').grid(row=row, column=0)
        btn_pause = Button(self.window, text=ld.get_text_from_dict(self.language, '~6'),
                           command=lambda: self.pause_btn_listener(token),
                           fg="green", bg="light gray", height=1, width=self.width)
        btn_pause.grid(row=row, column=0, sticky=E)
        btn_forward = Button(self.window, text=ld.get_text_from_dict(self.language, '~50'),
                             command=lambda: self.forward_btn_listener(token),
                             fg="blue", bg="light gray", height=1, width=self.width)
        btn_forward.grid(row=row, column=1, sticky=S)
        btn_skip = Button(self.window, text=ld.get_text_from_dict(self.language, '~52'),
                          command=lambda: self.skip_btn_listener(token),
                          fg="red", bg="light gray", height=1, width=self.width)
        btn_skip.grid(row=row, column=2, ipadx=self.xpad, sticky=W)

        row += 1
        btn_return = Button(self.window, text=ld.get_text_from_dict(self.language, '~8'),
                            command=lambda: self.return_btn_listener(token),
                            fg="green", bg="light gray", height=1, width=self.width)
        btn_return.grid(row=row, column=0, sticky=E)
        btn_reassign = Button(self.window, text=ld.get_text_from_dict(self.language, '~51'),
                              command=lambda: self.reassign_btn_listener(token),
                              fg="blue", bg="light gray", height=1, width=self.width)
        btn_reassign.grid(row=row, column=1, sticky=S)
        btn_drop = Button(self.window, text=ld.get_text_from_dict(self.language, '~53'),
                          command=lambda: self.drop_btn_listener(token),
                          fg="red", bg="light gray", height=1, width=self.width)
        btn_drop.grid(row=row, column=2, ipadx=self.xpad, sticky=W)

        ### FUNCTIONALITY to enable/ diable buttons
        # btn_drop.config(state = tk.DISABLED)

    def pause_btn_listener(self, token):
        """pause_btn_listener handles the pause action when that option is selected.  It indicates
        that there is not a necessary staff change (used later when resetting the window), marks 'N/A' for comments
        and then calls for the logging setting of the screen
        :param token: the unique token id of the task
        :type token: int"""
        self.staff_change = False
        log_input = 'N/A'
        self.log_and_reset('~6', log_input, token)

    def forward_btn_listener(self, token):
        """forward_btn_listener handles the forward action when that option is selected.  It indicates
        that there is a necessary staff (used later when resetting the window), calls for a textbox to be created for
        staffer comments.  It then retrieves a list of possible staffers and calls for that list to be displayed as a
        drop down menu at the bottom of the screen.
        :param token: the unique token id of the task
        :type token: int"""
        self.staff_change = True
        self.log_textbox('~50', token)
        choices = communicator.get_possible_staff(self.device_id, True)
        self.drop_down(choices)

    def reassign_btn_listener(self, token):
        """reassign_btn_listener handles the reassign action when that option is selected.  It indicates
        that there is a necessary staff (used later when resetting the window), calls for a textbox to be created for
        staffer comments.  It then retrieves and sets an alternate staffer.
        :param token: the unique token id of the task
        :type token: int"""
        self.staff_change = True
        self.log_textbox('~51', token)
        self.alternate_staff = communicator.get_possible_staff(self.device_id, False)

    def return_btn_listener(self, token):
        """return_btn_listener handles the return action when that option is selected.  It indicates that there is not a
        necessary staff change, updates the flow info for the token, then calls for a textbox to be created for
        staffer comments.
        :param token: the unique token id of the task
        :type token: int"""
        self.staff_change = False
        communicator.add_flow_info(token, '~8')
        self.log_textbox('~8', token)

    def skip_btn_listener(self, token):
        """skip_btn_listener handles the skip action when that option is selected.  It indicates that there is not a
        necessary staff change, updates the flow info for the token, then calls for a textbox to be created for
        staffer comments.
        :param token: the unique token id of the task
        :type token: int"""
        self.staff_change = False
        communicator.add_flow_info(token, '~52')
        self.log_textbox('~52', token)

    def drop_btn_listener(self, token):
        """drop_btn_listener handles the drop action when that option is selected.  It indicates that there is not a
        necessary staff change, updates the flow info for the token, then calls for a textbox to be created for
        staffer comments.
        :param token: the unique token id of the task
        :type token: int"""
        self.staff_change = False
        communicator.add_flow_info(token, '~53')
        self.log_textbox('~53', token)

    def log_textbox(self, status, token):
        """log_textbox displays a text box allowing the user to write comments for the task that is being reassigned.
        It also creates a submit button that processes the log and resets the screen.
        :param status: the status of the token as described by the buttons
        :type status: str (~vocab)
        :param token: the unique token id of the task
        :type token: int"""
        self.clear_window()
        log_input = tk.Text(self.window, height=10, width=55)
        log_input.pack(side=TOP)
        Button(self.window, text='Submit',
               command=lambda: self.log_and_reset(status, log_input, token)).pack(side=BOTTOM)

    def log_and_reset(self, status, log_input, token):
        """log_and_reset handles the sending of the required information to the communicator and resetting the window
        back to the staffers home screen
        :param status: the status of the token as described by the buttons
        :type status: str (~vocab)
        :param log_input: the data from the
        :param token: the unique token id of the task
        :type token: int"""
        try:  # when log_input comes from the text box
            comments = log_input.get(1.0, "end-1c")
        except:  # when log_input comes from a string
            comments = log_input
        communicator.update_log(token, self.device_id, status, comments, self.priority.get())
        if self.staff_change:
            communicator.change_staffer(token, self.device_id, self.alternate_staff, status)
            self.home.reset_window(self.device_id, token, True)
        else:
            if status == '~6':
                communicator.pause_tasks(self.device_id, token, '~6')
                self.home.reset_window(self.device_id, token, False)
            elif status == '~8':  # for returned tasks
                communicator.return_data(token, None)
                self.home.partial_complete(self.device_id, token, True)
            elif status == '~52':  # for skipped tasks
                communicator.return_data(token, None)
                self.home.partial_complete(self.device_id, token, True)
            elif status == '~53':  # for dropped tasks
                communicator.return_data(token, None)
                self.home.partial_complete(self.device_id, token, True)

    def drop_down(self, choices):
        """drop_down displays the available options for staff reassignment to the staffer after selecting
        the forward button
        :param choices: a list of choices of different possible staffers
        :type choices: list"""
        Label(self.window, text=ld.get_text_from_dict(self.language, '~56') + ': ').pack(side=LEFT, anchor=N)
        option = StringVar(self.window)
        choices_formatted = []
        for choice in choices:
            choices_formatted.append(communicator.name_from_staff_id(choice))
        communicator.staff_id_from_name(choices_formatted[0])
        option.set(choices_formatted[0])
        drop_down = OptionMenu(self.window, option, *choices_formatted)
        self.alternate_staff = option
        drop_down.pack(side=LEFT, anchor=N)

    def clear_window(self):
        """This function clears the window that it is given allowing it to be a blank canvas before the window
        is repopulated with different widgets
        """
        for widget in self.window.winfo_children():
            widget.destroy()
