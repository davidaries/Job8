"""The communicator modules is used to allow the UI to interact with the data stored by the simulation.  It allows
the UI to receive data from their corresponding pe_outs table (stored in working data) and return data to pe_ins to
then be processed by PE.  In addition to these tasks, the communicator module interacts with and writes to log data.
It also handles the passing of tasks to other staffers and retrieves other possible staffers who can process said tasks.
"""
import initial_load_data as ild
import simulation_time
import working_data as wd
import get_responsible_staff as grs
from icecream import ic


def update_log(token, device_id, status, comments, priority):
    """Appends additional log information to the task in question (with token being the key for the log data
    :param token: the unique token associated with the task at hand
    :type token: str
    :param device_id: the unique device id of a staffer
    :type device_id: str
    :param status: a dictionary reference to the status of the token in question
    :type status: str (~vocab)
    :param comments: the comments associated with the log update information
    :type comments: str
    :param priority: the priority level of the token in question (1= highest priority, 3 = lowest priority
    :type priority: int"""
    time = simulation_time.get_time_stamp()
    user = ild.device_staff.get(device_id)
    wd.pe_outs.get(str(device_id))[token][2] = priority
    log_data = {'user': user, 'time': time, 'status': status, 'priority': priority, 'comments': comments}
    if token in wd.log_dict:
        wd.log_dict.get(token).append(log_data)
    else:
        wd.log_dict[token] = [log_data]
    wd.token_status_dict[token] = status


def change_staffer(token, current_staffer, alternate_staffer, status):
    """Handles the actual change in staffer for a given task (defined by its token)
    :param token: the unique token associated with the task at hand
    :type token: str
    :param current_staffer: the device ID of the staffer that is currently responsible for the task
    :type current_staffer: str
    :param alternate_staffer: the device ID of the staffer that will be receiving this task
    :type alternate_staffer: str
    :param status: the status of the task being given to the alternate staffer
    :type: str (~vocab)"""
    new_staff_device = None
    try:
        if alternate_staffer[0] == 's':
            new_staff_device = ild.staff_device.get(alternate_staffer)
    except:
        name = alternate_staffer.get()
        new_staff_device = ild.staff_device.get(staff_id_from_name(name))

    wd.pe_waits.get(token)[0] = str(new_staff_device)  # may change with dict implementation
    pe_out = wd.pe_outs[str(current_staffer)].pop(token)
    pe_out[8] = status #update status with forward or reassign
    wd.pe_outs.get(str(new_staff_device))[token] = pe_out


def return_data(token, data_return):
    """This function sends the appropriate data for the token in question to be processed by the controller
    :param token: unique token id used for tasks
    :type token: int
    :param data_return: list of the corresponding data for the token
    :type data_return: list"""
    flow_info = None
    if token in wd.flow_data:
        flow_info = wd.flow_data.get(token)
    wd.pe_ins_sol.append([token, simulation_time.get_time_stamp(),
                          {'data': data_return, 'log': wd.log_dict.get(token), 'flow': flow_info}])


def get_tasks(device_id):
    """This function returns the current list of tasks for a staffer based on their device_id
    :param device_id: a unique id for the staffers device
    :type device_id: str"""
    return wd.pe_outs.get(str(device_id))


def add_flow_info(token, flow):
    """updates the flow data for a task (identified by its token)
    :param token: unique token id used for tasks
    :type token: int
    :param flow: the flow type for this task that is being updated
    :type flow: str (~vocab)"""
    wd.flow_data[token] = flow


def get_possible_staff(id_current_staff, is_list):
    """Returns the possible staffers who are able to take on the task that the current staffer has been assigned
    :param id_current_staff: the unique id of the current staffer
    :type id_current_staff: str
    :param is_list: a variable that dictates whether a list of staffers is requested or just a single possible staff memeber
    :type is_list: bool
    :return: staffer (or staffers) capable of taking the task
    :rtype: list or str"""
    current_staffer = ild.device_staff.get(id_current_staff)
    staff_type = ild.staffers.get(str(current_staffer)).get('~23')
    return grs.get_other_staffers(staff_type, current_staffer, is_list)


def staff_id_from_name(name):
    """return a staffers id given their name
    :param name: name of the staffer
    :type name: str
    :return: staffer id
    :rtype: str"""
    for staff in ild.staffers:
        if ild.staffers.get(staff).get('~1') == name:
            return staff


def name_from_staff_id(staff_id):
    """return a staffers name based on their id_number
    :param staff_id: the unique id of the staffer
    :type staff_id: str
    :return: id of the staffer
    :rtype: str"""
    return ild.staffers.get(staff_id).get('~1')


def pause_tasks(staff_id, token, status):
    """converts the status of a token to pause so the status will be displayed as paused in the UI
    :param staff_id: the unique id of the staffer
    :type staff_id: str
    :param token: unique token of the task
    :type token: int
    :param status: the dictionary reference to the status of the of the task
    :type status: str (~vocab)"""
    wd.pe_outs.get(str(staff_id)).get(token)[8] = status
