"""initial_load_data.py is data to be used in this program
   In the future such data will be loaded from tables, not come from this module.
"""


# PROTOCOL TABLE DATA ###############################################################
# We will be loading from a protocol table, which has these fields
# protocol, step, step_type, description, task, task_type, spec, write, flow
# And and were creating protocol dictionary, which has these fields:
# step_type[0], task[1], task_type[2], spec[3], write[4], flow[5]

p0001 = {      # this is what protocol p0001 with its four steps will look like when loaded from the table
    1: ['st_1', '~34', 'UI', ('PersonHeader', 'TaskHeader',
        ('ModifyEntry', '~16'), ('Button', '~20')), None, ({'call': [['p0001', 2, 3]]})],
    2: ['st_1', '~35', 'UI', ('PersonHeader', 'TaskHeader',
        ('EmptyEntry', '~19', {'vt': 'f', 'range': [0.1, 250], 'units': '~41'}),
        ('DropDown', '~17', 'c117'), ('Button', '~20')), None, ({'call': [['p0001', 3, 3], ['p0001', 7, 3]]})],
    3: ['st_1', 'calc BMI', 'murphy', 'murphy005', None, ({'call': [['p0001', 4, 3]]})],
    4: ['st_1', 'diabetes screen', 'decisioning', 'BMI_d1', None, ({'call': [['p0001', 5, 3]]})],
    5: ['st_1', '~36', 'UI', ('PersonHeader', 'TaskHeader',
        ('Fixed', '~17'), ('DropDown', '~2', 'c102'), ('Button', '~20')), None, ({'call': [['p0001', 6, 3]]})],
    6: ['st_1', '~18', 'UI', ('PersonHeader', 'TaskHeader',
                              ('Fixed', '~2'), ('CheckBoxes', '~18', 'c118'), ('Button', '~20')), None, ({})],
    7: ['st_1', 'calc avg weight', 'murphy_mkv', ['murmkv003', [['a', '~19', [3]]]], None, ({})]
    # Note: three issues remain with step 7:
    # 1. it is returning the average as yet another weight (~19), there is no key for average weight
    # 2. it is not returning the units (~41) - murmkv003 doesn't ever ask, so can't return them
    # and it's not clear today (2/3/21) what the use case is for average, and if we even want to write it pdata/adat
    # but it's an easy to resolve as we continue to build out murphys
    # 3. step 2 is a branch (to steps 3 & 7), but there is no subsequent merge
    # which should be there if branch is within same protocol. But this example is artificial, so leave it for now.
    }

p0002 = {      # this is what protocol p0001 with its four steps will look like when loaded from the table
    1: ['st_1', '~18', 'UI', ('PersonHeader', 'TaskHeader',
        ('Fixed', '~2'), ('CheckBoxes', '~18', 'c119'), ('Button', '~20')), None, ({})]
    }

ip01 = {       # this is what the intake protocol ip-1 with its one step will look like when loaded from the table
    1: ['st_1', '~ip01_task', '~ip01_task_type', None, None, ({'call': [['p0001', 1, 3]]})]
    }

protocols = {      # here we create the protocols dictionary and load the two protocols into it.
    'p0001': p0001,
    'p0002': p0002,
    'ip01': ip01
    }

choices = {    # What to display in UI as choices. True appears in short list, False only in the complete list.
    'c117': [['~28', True], ['~29', True]],
    'c102': [['~5', True], ['~30', True], ['~37', False], ['~38', False], ['~39', False]],
    'c118': [['~31', True], ['~32', True]],
    'c119': [['~44', True]]
    }

# STAFFING RELATED TABLE DATA ###############################################################
p0001_staff = {     # assigning a staff type to each step in protocol p0001
    1: '~24', 2: '~25', 5: '~26', 6: '~27'
    }

p0002_staff = {     # assigning a staff type to each step in protocol p0001
    1: '~27'
    }

protostep_staff = {     # putting the staff type assignments for protocol p0001 into the protostep_staff  dictionary
    'p0001': p0001_staff,
    'p0002': p0002_staff
    }

staffers = {                # a primitive dictionary for staffers that will do for now
    's001': {'~1': 'Joe Montana', '~23': '~24', '~100': '~101'},
    's002': {'~1': 'Jose Cuervo', '~23': '~25', '~100': '~102'},
    's003': {'~1': 'Maria Espanosa', '~23': '~26', '~100': '~101'},
    's004': {'~1': 'Mary Magdolin', '~23': '~27', '~100': '~102'},
    's005': {'~1': 'Ally Smith', '~23': '~24', '~100': '~102'},
    's006': {'~1': 'Mack DeMarco', '~23': '~25', '~100': '~101'},
    's007': {'~1': 'Natasha Bettingfield', '~23': '~26', '~100': '~102'},
    's008': {'~1': 'Doreen Gray', '~23': '~27', '~100': '~101'},
    's009': {'~1': 'Thomas T. Tank Engine', '~23': '~24', '~100': '~101'},
    's010': {'~1': 'Lauren Boebert', '~23': '~25', '~100': '~102'},
    's011': {'~1': 'Dennis Dennington', '~23': '~26', '~100': '~101'},
    's012': {'~1': 'Rachel Maddow', '~23': '~27', '~100': '~102'}
    }

# these next two rows to be dynamically generated when we have staff login in place.
staff_device = {}

device_staff = {}

staffer_login_info = {'s001': ['pass', False], 's002': ['pass', False],
                      's003': ['pass', False], 's004': ['pass', False],
                      's005': ['pass', False], 's006': ['pass', False],
                      's007': ['pass', False], 's008': ['pass', False],
                      's009': ['pass', False], 's010': ['pass', False],
                      's011': ['pass', False], 's012': ['pass', False]
                      }

# PERSON RELATED DATA ###############################################################
entrants = [['07:20', 'pers101'],  ['07:25', 'pers102'],  ['07:50', 'pers103'],   # what time they enter the clinic
            ['08:00', 'pers104'],  ['08:15', 'pers105'],  ['08:30', 'pers106']]