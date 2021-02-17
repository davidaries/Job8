"""The primary responability of this class is to setup the main window for the UI, which contains various functionality
including interactions with the sumlation time clock as well as the creation of login windows and the ability to log
in all available staffers simultaniously.  Log window has been left in this module in case we have a need in the
future to add data to a UI log window but is not being used at this time"""

from tkinter import *
import language_dictionary as ld
from sim_staff_window_manager import sim_staff_window_manager
import simulation_time
import tools



def setup_ui():
    """the function called to set up the UI main screen with the system time and login features"""
    base_language = '~101'

    root = Tk()

    root.title(ld.get_text_from_dict(base_language, '~11'))  # title for window
    root.geometry('430x100+0+0')  # main window geometry
    time_lbl = Label(root, text="test", font='Helvetica 18 bold')
    time_lbl.grid(row=0, column=1)

    # create Log Window
    log_window = Toplevel(root)
    log_window.title(ld.get_text_from_dict(base_language, '~13'))
    log_window.geometry("600x300+0+500")
    log_window.withdraw()
    staffers_home = sim_staff_window_manager(root, log_window)
    staffers_home.add_home(staffers_home)

    simulation_time.set_ui_tools(root, time_lbl)

    btn_pause = Button(root, text=ld.get_text_from_dict('~101', '~6'), fg="black", bg="gray",
                       command=lambda: simulation_time.set_clock_running(True),
                       height=1, width=13)
    btn_unpause = Button(root, text=ld.get_text_from_dict('~101', '~7'), fg="black", bg="gray",
                         command=lambda: simulation_time.set_clock_running(False), height=1, width=13)
    btn_sum = Button(root, text='Current Status', fg="black", bg="gray",
                     command=tools.summary, height=1, width=13)
    btn_login_page = Button(root, text='login', fg="black", bg="gray",
                            command=staffers_home.login_screen, height=1, width=13)
    test = Button(root, text='test', fg="black", bg="gray",
                  command=staffers_home.login_all, height=1, width=13)
    btn_pause.grid(column=0, row=1)
    btn_sum.grid(column=1, row=1)
    btn_unpause.grid(column=2, row=1)
    btn_login_page.grid(column=0, row=2)
    test.grid(column=2, row=2)