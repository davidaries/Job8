import random
from tkinter import *
from sim_staff_window import manage_window
import initial_load_data as ild
from sim_login_window import login_manager as lm
import communicator
import simulation_time
import working_data
from icecream import ic


class sim_staff_window_manager:
    """The home_screen class is in charge of creating and managing the home screens for the various staffers
    based on the different kinds of staff windows, the handling of the person populated on their task list
    will be done based on their job type in manage_window module
    :param self.controller: a reference to the controller module
    :type self.controller: module
    :param self.sim_time: a reference to the system_time module used to manage the timing of the simulation
    :type self.sim_time: module
    :param self.root: reference to the main tk program used for the creation of additional windows
    :type self.root: tk class reference
    :param self.log_window_pointer: pointer to reference the log window which is needed to write data to the log window
    :type self.log_window_pointer: tk module
    :param self.horizontal_spacing: value used to space the windows horizontally across the screen
    :type self.horizontal_spacing: int
    :param self.column_padding: value used to space out values placed into a window
    :type self.column_padding: int
    :param self.row_padding: value used to pad rows to make the spacing between them larger
    :type self.row_padding: int
    :param self.row_current: value used to place values in the home screen in the appropriate rows
    :type self.row_current: int
    :param self.task_row: value used to increment the current row placement
    :type self.task_row: int
    :param self.staff_dict: stores the tk window of a staffer where the dict key is their staff_id
    :type self.staff_dict: dict
    :param self.staff_login: is
    :param self.home: a reference to the home_screen module created in sim_main_window.py given to children windows so data
    can be returned in teh future
    :type self.home: module reference"""

    def __init__(self, master, log_window):
        """Sets up the home_screen module
        :param master: a reference to the master window for the UI
        :type master: tk window reference
        :param log_window: no longer in use but kept around incase it might be useful in the future.  This is a
        reference to the log window information can be displayed
        :type log_window: tk window
        """
        self.root = master
        self.log_window_pointer = log_window
        self.horizontal_spacing = 0
        self.vertical_spacing = -250
        self.column_padding = 80
        self.row_padding = 12
        self.row_current = 2
        self.window_count = 0
        self.task_row = 0
        self.staff_dict = {}
        self.home = None

    def create_home_screen(self):
        """In charge of the creation of a new window to be displayed on the screen
        :return: a reference to a window so it can be edited in the future
        :rtype: Window"""
        if self.window_count % 4 == 0:
            self.vertical_spacing += 400
            self.horizontal_spacing = 0
        screen = Toplevel(self.root)
        screen.geometry("475x350+" + str(self.horizontal_spacing) + '+' + str(self.vertical_spacing))
        self.horizontal_spacing += 500
        return screen

    def login_screen(self):
        """This function creates the login screen for the various staffer by making calls to the login_manager
        module"""
        window = self.create_home_screen()
        login_manager = lm(self.root, '~101', self.home, window)
        login_manager.add_entry_id()
        login_manager.add_entry_password()
        login_manager.login_button()
        self.window_count += 1

    def login_all(self):
        """This function creates a window for all available staff members and bypasses the login screen for all of
        those staff members"""
        for staff in ild.staffers:
            window = self.create_home_screen()
            ild.staffer_login_info.get(staff).__setitem__(1, True)
            self.login_success(staff, window)
            self.window_count += 1

    def login_success(self, staffer_id, window):
        """After a successful login from a staffer, this function creates a home screen for them with their
        corresponding tasks.
        :param staffer_id: the unique id of a staffer
        :type staffer_id: str
        :param window: a reference to the associated tkinter window
        :type window: tk window"""
        device_id = communicator.give_device_id(staffer_id)
        staff_info = ild.staffers.get(staffer_id)
        self.staff_dict[device_id] = manage_window(window, staff_info,
                                                   device_id, self.root, self.home)

        self.staff_dict[device_id].clear_window()
        self.staff_dict[device_id].set_home()
        self.staff_dict[device_id].poll_controller()
        ic(working_data.pe_outs)

    def add_home(self, home):
        """Sets a reference to home_screen that is later passed to the staffer windows so data can be sent back to
        home_screen module, which has a connection with the controller module
        :param home: reference to the home_screen module
        :type home: class reference
        """
        self.home = home

    def reset_window(self, device_id, token, clear_token):
        self.staff_dict.get(device_id).clear_widgets()
        if clear_token:
            self.staff_dict.get(device_id).dat.clear_token(token)
        self.staff_dict.get(device_id).refresh_home()

    def partial_complete(self, device_id, token, clear_token):
        self.staff_dict.get(device_id).partial_complete(token)
        self.reset_window(device_id, token, clear_token)
