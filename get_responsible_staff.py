"""# get_responsible_staff.py
This module has functions to identify a staff member to be responsible for a protocol step.
get_staffer receives from the caller the protocol and step
  it uses get_staff_type to get the role needed to do that step
  and then get_staffer to identify and individual staff with that role
  and finally gets their device id and returns it.

get_other_staffers gets other staffer(s) who can be responsible for the step
"""

import initial_load_data as ild
from icecream import ic


def get_device_out(protocol, step):
    staff_type = get_staff_type(protocol, step)  # get the responsible staff_type
    staffer = get_staffer(staff_type)            # get the responsible staffer based on staff_type
    device_out = ild.staff_device[staffer]       # then get the device_out based on the staffer
    return device_out


def get_staff_type(protocol, step):              # get the staff_type responsible for the step in the protocol
    staffer_type = ild.protostep_staff[protocol][step]
    return staffer_type


def get_staffer(staff_type):  # get a staffer of the staff_type who can be responsible for the step in the protocol
    for s in ild.staffers:    # currently gets the first staffer who matches on staff_type, much more to be done!
        if ild.staffers[s]['~23'] == staff_type:
            return s


def get_other_staffers(staff_type, current_staffer, list):  # get other staffer(s) who can be responsible for the step
    staff_choices = []
    for s in ild.staffers:
        if ild.staffers[s]['~23'] == staff_type and s is not current_staffer:
            if not list:       # if list is false
                return s       # returns the first staffer who meets the criteria
            else:              # if list it true
                staff_choices.append(s)   # appends all staffers who meet the criteria
    return staff_choices                  # and returns the list