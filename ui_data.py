import simulation_time as sim_time
import working_data as wd
from icecream import ic


class ui_data:
    """ui_data class has been created to manage the various pieces of data stored and used by the UI.  This inclues
    references to the time label and storage of the repost times and start times used for the home display for a staffer
    :param self.token_list: list of all of the tokens that belong to a staffer
    :type self.token_list: list
    :param self.name_row: is a dictionary of rows at which various names are being displayed for people in a staffers home screen
    :type self.name_row: dict (key = name, value = row)
    :param self.token_start_time: dictionary with the value of the start time for a specific token
    :type self.token_start_time: dict (key = token, value = start_time)
    :param self.token_time_label: a dictionary that stores a reference to the time label of a specific token
    :type self.token_time_label: dict (key = token, value = time_label)
    :param self.token_repost_time: dictionary with the value of the repost time for a specific token
    :type self.token_repost_time: dict (key = token, value = repost_time)
    :param self.tokens_completed: a list of tokens completed by a staffer
    :type self.tokens_completed: list"""

    def __init__(self):
        self.token_list = []
        self.name_row = {}
        self.token_start_time = {}
        self.token_time_label = {}
        self.token_repost_time = {}
        self.tokens_completed = []

    def should_display(self, task, tasks):
        """Check whether a token should be written and displayed.  To be a valid token the task must not already
        be in the token list and must not be in the list of completed tokens
        :param task: is the token of a task that is being checked
        :type task: int
        :param tasks: the information about the given tasked (used for getting the start time)
        :type tasks: list
        :return: whether or not the given task should be displayed
        :rtype: bool"""
        if task not in self.token_list and task not in self.tokens_completed:
            self.token_start_time[task] = tasks.get(task)[6]
            self.token_list.append(task)
            return True
        return False

    def should_update_time(self, task, at_home):
        """checks whether a task should have it's time updated.  This is based on whether the task has a time label,
        the task is not in the list of completed tokens, and if the staffer is at their home screen.  All must be true
        to update the time.
        :param task: is the token of a task that is being checked
        :type task: int
        :param at_home: whether or not the staffer is in their home screen
        :type at_home: bool
        """
        if task in self.token_time_label and task not in self.tokens_completed and at_home:
            self.update_wait_time(task)

    def update_wait_time(self, token):
        """This function updates the wait time for a person that has arrived in the staffers home screen
        :param token: the unique value used to reference specific tasks
        :type token: int"""
        display_t_diff = sim_time.get_time_difference(self.token_start_time.get(token))
        if self.token_repost_time[token]:
            display_t_diff += '/' + sim_time.get_time_difference(self.token_repost_time.get(token))
        self.token_time_label.get(token).config(text=display_t_diff)

    def clear_token(self, token):  # move to ui_data.py
        """Removes a token from the lists and dictionaries it is active in
        :param token: the unique value used to reference specific tasks
        :type token: int"""
        self.token_list.remove(token)
        self.token_start_time.pop(token)
        self.token_time_label.pop(token)
        self.token_repost_time.pop(token)
        self.name_row.clear()

    def time_diff_start_time(self, token):
        """returns the time that has passed between the the start time of the token and the current sim_time
        :param token: the unique value used to reference specific tasks
        :type token: int"""
        try:
            return sim_time.get_time_difference(self.token_start_time.get(token))
        except:
            return None

    def add_start_time_label(self, token, label_time):
        """Associates a token with a label used to display relevant time information (wait time and repost wait time)
        :param token: the unique value used to reference specific tasks
        :type token: int
        :param label_time: a reference to the label used to display the time for a specific token
        :type label_time: Label
        """
        self.token_time_label[token] = label_time

    def update_repost_time(self, token):
        try:
            self.token_repost_time[token] = int(wd.log_dict.get(token)[-1].get('time'))
        except:
            self.token_repost_time[token] = None

    def add_token_row_name(self, row, name):
        """adds a person to the dictionary associating their name with the current row they are being displayed on
        !!REWORK this as the row is no longer needed with the addition of the organize task function!!
        :param """
        self.name_row[name] = row + 1

    def check_in_display(self, name):
        """Checks to see if a person's name is already being displayed on the staffers screen.  If they are already being
        displayed, the return is true, otherwise the return is false
        :param name: the name of the person being processed by the staffer
        :type name: str
        :return: whether or not the person is already in the display
        :rtype: bool"""
        if name in self.name_row:
            return True
        return False

    def organize_tasks(self, tasks, device_id):
        """Organizes all of the tasks first by priority and time.  It then checks for duplicate names and reorganizes
        this list accordingly
        :param tasks: the task and associated information of the task
        :type tasks: dict
        :param device_id: the id number of the device
        :type device_id: str
        :return: a list of ordered tasks
        :rtype: list"""
        priority_tasks = {}
        person_tasks = {}
        ordered_tokens = []
        ic(tasks)
        ic(device_id)
        try:
            for t in tasks:
                if t not in self.tokens_completed:
                    priority_tasks[t] = tasks.get(t)[2]
            tuple_tasks = sorted(priority_tasks.items(), key=lambda item: item[1])
            ic(tuple_tasks)
            for tup in tuple_tasks:  # create list based on priority
                ordered_tokens.append(tup[0])
            for token in ordered_tokens:  # organize for name
                person_id = wd.pe_outs[str(device_id)].get(token)[0]
                if person_id in person_tasks:
                    person_tasks[person_id].append(token)
                else:
                    person_tasks[person_id] = [token]
            flat_dict = list(person_tasks.values())
            ordered_tokens = [token for subl in flat_dict for token in subl]
            return ordered_tokens
        except:
            print('no tasks')
