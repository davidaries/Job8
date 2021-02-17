""" decisioning.py
    currently has three distinct components
    1. The decision function receives the person and the decision spec from a caller.
        it uses query to get the relevant data for the person (returning missing if the relevant data is not available)
        then for each value to be evaluated, it calls an evaluation function, which return a T or F (for True or False)
        those results are compiled into a composite, which are is then evaluated by the table in the last lines.
    2. An evaluation functions receives the data from the decision function and returns a string which codes for
        which key and which test for that key was tested. An examples:
        - if one variable is passed in and two (mutually exclusive) tests are done on it,
            the strings returned (in list) would be [var11T, var12F] or [var11F, var12T]
    3. Decision Specs are where the criteria for making a decision are coded. Each has two distinct components
        a. specify the criteria for testing each value
        b. specifying what decision to be made based on the composite result. Where a decision is to call none,
            one, or more than one of either:
                step with the current protocol
                a new (different) protocol
    Notes on 1/29/21
    - There is so much more to be built out here in evaluation functions, and the decisioning function
    will doubtless need more attention to support those and be more efficient.
    - decision_specs will need to built using an interface for that purpose, and stored in their own place in the
    database (not in here), hopefully in a common well-structured format, perhaps even in a table
"""

import query


# BEGIN EVALUATION FUNCTIONS ###################################################
def evaluate_1test(value, crit):
    """evaluate_1test is used if only one test is need to categorized (e.g. into one of two mutually exclusive groups)
    currently this is only working if numbers come in as

    :param value: the value to be be tested
    :type value: num (int or float)
    :param crit: the criteria against which to test the value
    :type crit: str
    :returns: 'T' or 'F'
    """
    result = 'T' if eval(str(value[1]) + crit[0] + str(crit[1])) else 'F'
    # print('test = ', (str(value[1]) + crit[0] + str(crit[1])), 'result =', result)
    return result


def evaluate_2tests(value, crit):
    """ # evaluate_2test is used if two tests are need to categorize a value (e.g. within a range)
    currently this is only working if numbers come in as

    :param value: the value to be be tested
    :type value: num (int or float)
    :param crit: the criteria against which to test the value
    :type crit: str
    :returns: 'T' or 'F'
    """
    result = 'T' if (eval(str(value[1]) + crit[0] + str(crit[1])) and
                     eval(str(value[1]) + crit[2] + str(crit[3]))) else 'F'
    # print('test = ', (str(value[1]) + crit[0] + str(crit[1])), 'and', (str(value[1]) + crit[2] + str(crit[3])), 'result =', result)
    return result
# ### END EVALUATION FUNCTIONS ###################################################


# BEGIN DECISIONING FUNCTION ##########################################################
def decision(person, d_spec):
    """ receives the person and the decision spec from a caller, uses query to get the relevant data for the person,
        calls an evaluation function for each value and criteria, codes the results in a composite,
        which are is then evaluated by the table in the last lines.
    :param person: the person for whom the decision is needed
    :type person: str
    :param d_spec: values and criteria by which to evaluate them and what calls (if any) to return based on evals
    :type d_spec: list
    :return: what step(s) or protocol(s) to call
    """
    decision_spec = spec_dict.get(d_spec)
    var_values = []
    missed = 0
    vars_specs = decision_spec[0]
    for var_spec in vars_specs:
        if len(var_spec[0]) == 1:    # if only the most recent value of the key is needed
            value = query.adat_person_key(person, var_spec[0][0][0])   # gather data with this call
        else:                         # if some other criteria to get the value(s)
            value = query.adat_person_key_options(person, var_spec[0][0], var_spec[0][1], var_spec[0][2],
                                                  var_spec[0][3])        # use this one
        if not value:                 # if the query (whichever of the two) doesn't return a value
            value = 'missing'
            missed += 1
        var_values.append([var_spec[0], value])
    if missed > 0:                    # if data for any variable was missing
        return ('missing report', var_values)     # stop here and return a missing report
    # now, since we made it past the above line, relevant data exists we continue and evaluate each
    var_cycles = len(var_values)   # setting up to to cycle through all the variables involved
    var_cycle = 0
    composite = []
    while var_cycle < var_cycles:  # starting the cycle through variables
        crit_cycles = len(decision_spec[0][var_cycle][2])    # setting up to cycle through criteria on that variable
        crit_cycle = 0
        while crit_cycle < crit_cycles:   # starting the cycle through criteria
            ds = decision_spec[0][var_cycle][2][crit_cycle]     # gathering the test criteria to be used
            if len(ds) == 2:       # if there is one test criteria to be used
                result = evaluate_1test(var_values[var_cycle][1], ds)
            elif len(ds) == 4:     # if there are two test criteria to be used
                result = evaluate_2tests(var_values[var_cycle][1], ds)
            else:
                result = None
                print('\n\nERROR LURKING- length of decision criteria not within range\n\n')
            coded_result = ['var' + str(var_cycle + 1) + str(crit_cycle + 1) + result]  # create the coded string
            crit_cycle += 1
            composite = composite + coded_result   # compile the results (as a list of coded strings)
        var_cycle += 1
    # print('\n', person, composite)

    # finally, compare the composite generated with the table specifications, and return what should happen next
    table = decision_spec[1]
    for tab in table:             # go one by one through table until
        if tab[0] == composite:   # we find a match to the composite
            return tab[1]         # then return what the table specified as the decision, the call(s) to make
# ### END DECISIONING FUNCTION ##########################################################


# BEGIN DECISION_SPECS  ##########################################################
spec_dict = {
    'BMI_d1':
        [[
            [[['~47']], 'float', [[' < ', 30], [' >= ', 30]]]
        ],
            [
                [['var11T', 'var12F'], None],
                [['var11F', 'var12T'], {'call': [['p0002', 1, 3]]}],
                ['missing', 'call missing_data_protocol']
            ]]
}
# ### END DECISION_SPECS #########################################################
