import language_dictionary as ld
from tkinter import *
from tkinter import font as tk_font
import initial_load_data as ild
# import controller

class login_manager:
    """ a module created to manage a staffer logging into a specific window
    :param self.root: a reference to the tkinter root screen needed to populate windows and use wait functions
    :type self.root: tk window reference
    :param self.language: the preset language '~101', which corresponds to english
    :type self.language: str
    :param self.home: a reference to the home_screen module used to send info back after a successful login
    :type self.home: module reference
    :param self.window: reference to the corresponding tkinter window that has been created
    :type self.window: tk window
    :param self.medium_font: a generated font used within the display
    :type self.medium_font: tk_Font
    :param self.larger_font: a generated font used within the display
    :type self.larger_font: tk_Font
    :param self.column_padding: value used to space out values placed into a window
    :type self.column_padding: int
    :param self.row_padding: value used to pad rows to make the spacing between them larger
    :type self.row_padding: int
    :param self.row_current: value used to place values in the home screen in the appropriate rows
    :type self.row_current: int
    :param self.task_row: value used to increment the current row placement
    :type self.task_row: int
    """
    def __init__(self, root, language, home, window):
        """The login manager class in in charge of handling the process of logging a staffer in to a window
        :param root: a reference to the tkinter root screen needed to populate windows and use wait functions
        :type root: tk window reference
        :param language: the preset language '~101', which corresponds to english
        :type self.language: str
        :param home: a reference to the home_screen module used to send info back after a successful login
        :type home: module reference
        :param window: reference to the corresponding tkinter window that has been created
        :type window: tk window reference"""
        self.root = root
        self.language = language
        self.home = home
        self.window = window
        self.medium_font = tk_font.Font(root=root.master, family='Helvetica', size=10, weight=tk_font.BOLD)
        self.larger_font = tk_font.Font(root=root.master, family='Helvetica', size=10, weight=tk_font.BOLD)
        self.column_padding = 80
        self.row_padding = 12
        self.row_current = 2
        self.task_row = 0
        self.login_widgets = []

    def add_entry_id(self):
        """This function adds an entry for the users unique id
        """
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, '~42') + ': ', font=self.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W')
        text_entered = StringVar()
        entry_box = Entry(self.window, textvariable=text_entered)
        self.login_widgets.append(('~42', entry_box))
        entry_box.grid(row=self.task_row, column=1, sticky='W')
        self.task_row += 1

    def add_entry_password(self):
        """This function adds an entry for the users password this is only diplayed as '*' on the UI side
        """
        lbl = Label(self.window, text=ld.get_text_from_dict(self.language, '~43') + ': ', font=self.medium_font)
        lbl.grid(row=self.task_row, column=0, ipady=self.row_padding, sticky='W')
        text_entered = StringVar()
        entry_box = Entry(self.window, textvariable=text_entered)
        entry_box.config(show="*")
        self.login_widgets.append(('~42', entry_box))
        entry_box.grid(row=self.task_row, column=1, sticky='W')
        self.task_row += 1

    def login_button(self):
        """This function creates a login button that allows the user to submit their login information"""
        btn_submit = Button(self.window, text=ld.get_text_from_dict(self.language, '~20'),
                            command=self.login_button_listener,
                            fg="black", bg="gray", height=1, width=10)
        self.window.bind('<Return>', lambda event: self.login_button_listener())
        btn_submit.grid(row=self.task_row, column=0, sticky='S')

    def login_button_listener(self): #checks should be moved somehwere else
        """This function process the data in the login screen to make sure that appropriate login credentials are given"""
        login_info = []
        for entry in self.login_widgets:
            login_info.append(entry[1].get())
        try:
            if ild.staffer_login_info.get(login_info[0])[0] == login_info[1]:
                if not ild.staffer_login_info.get(login_info[0])[1]:
                    self.successful_login(login_info[0])
                else:
                    self.unsuccessful_login("USER LOGGED IN ALREADY")
            else:
                self.unsuccessful_login("INVALID PASSWORD")
        except:
            self.unsuccessful_login("INVALID LOGIN")

    def unsuccessful_login(self, error):
        """If a login is unsuccessful, this function displays the appropriate error and refreshes the login page"""
        Label(self.window, text=error, font=self.larger_font).grid(row=self.task_row + 1, column=1)
        self.root.after(1000, self.reset_login)

    def reset_login(self):
        """This function is in charge of the actual refresh of the login page by clearing all data and
        repopulating all of the widgets"""
        self.login_widgets.clear()
        self.clear_window()
        self.add_entry_id()
        self.add_entry_password()
        self.login_button()

    def successful_login(self, staffer_id):
        """Once a user has entered the correct login data, a call to home_screen.login_success() is made that
        creates and fills the staffers home screen with their corresponding tasks.
        :param staffer_id: the unique id of the staffer that is used and linked to the screen created
        :type staffer_id: str"""
        ild.staffer_login_info.get(staffer_id).__setitem__(1, True)
        self.home.login_success(staffer_id, self.window)

    def clear_window(self):
        """This function clears the window that it is given allowing it to be a blank canvas before the window
        is populated with new data
        """
        for widget in self.window.winfo_children():
            widget.destroy()
