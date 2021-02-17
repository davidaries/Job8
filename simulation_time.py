""" simulation_time module is in charge of managing and interacting with the time used by the simulation
    contains functions for finding the difference between times, returning time values, stopping and resuming the clock, as
    well as updating the time at the speed of 60 seconds per second
"""

import datetime
import time
from icecream import ic

time_label = None
root = None
opening_time = datetime.datetime(2021, 1, 9, 7, 0, 0)
is_paused = False
current_time = opening_time
pause_time = opening_time


def set_clock_running(val):
    """toggles whether the simulation clock is running or not
    :param val: a value that updates whether the system time is paused or not
    :type val: bool"""
    global is_paused, pause_time
    is_paused = val
    pause_time = time.perf_counter()


def get_time_stamp():
    """returns the a time stamp of the current simulation time
    :return: the current simulation timestamp
    :rtype: float"""
    return time.mktime(current_time.timetuple())


def get_formatted_time():
    """returns the formatted time in the format used by datetime.datetime for easy display
    :return: the formatted current time
    :rtype: datetime"""
    return current_time


def get_time_difference(t):
    """Calculates and returns the difference between two a given time and the current time.  Currently subtracts 120
     seconds to make up for a latency between the controller and the UI
     :param t: the given time
     :type t: int
     :return: the formatted time difference
     :rtype: str"""
    return convert_time(get_time_stamp() - (t - 120))


def convert_time(seconds):
    """converts the given time in seconds to the format of (HH:MM)
    :param seconds: the number of seconds to be converted into this format
    :type seconds: float
    :return: the formatted time
    :rtype: str"""
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    minutes = seconds // 60 - (hour * 60)
    seconds %= 60
    return "%d:%02d" % (hour, minutes)


def clock():
    """clock is a function that recursively calls itself once every second to update the simulation time and reconfigure
    the time label with the updated time"""
    global current_time, root, time_label
    if not is_paused:
        current_time += datetime.timedelta(seconds=60)
        time_label.config(text=str(current_time))
    root.after(1000, clock)


def pause():
    """returns the value of whether the simulation_time is paused or not
    :return: the boolean value that says whether the system time is paused or not
    :rtype: bool"""
    return is_paused


def set_ui_tools(rt, timelbl):
    """sets up reference to the root and the time label used for managing the updating of the clock every second
    :param rt: reference to the root of the UI system
    :type rt: tk window
    :param timelbl: a reference to the time label on the main window
    :type timelbl: Label"""
    global root, time_label
    root = rt
    time_label = timelbl
