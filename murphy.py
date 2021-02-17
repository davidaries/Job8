""" murphy.py
main idea is that something can call a murphy, to get a calculation or some logic
and the murphy gets the data it needs using query.py
then return value(s) to whatever called it
at some point review decisioning.xlsx - and maybe shrink it, revise rename it, ...
and is there anything still of value in murphy.docx?
Okay, a murphy can come in with options of last, earliest, latest. And that would be by each variable I guess
do we still have an issue of order of calling variables?
since murphy is handling them as a, b, c based on order received
we need to be sure that they come from the caller in that order
-- the UI that guides the user in building the call to murphy must do that.
think about how to call data that is relative to other data? Something that must follow something else.
today we're thinking that is done by querying for plenty of data, and then handling it inside the murphy
Many murphys simply take what it was specified maps_keys_values and do their thing
Other (future) murphys (e.g., diffdx) might just be called by the Murphy number and would have within them
(in a data table of some sort) the specs on data what data to call.
On units:
- Some murphys may need conversion to different units before use (e.g., BMI)
- for those, when the values are pulled in, there needs to be a specification of the units the murphy expects
- and a check for what came in to see if it matches - and if not a routine to
- convert the number to the units the murphy uses
- do the murphy (as usual)
- and if the murphy created something with units, potentially reconvert the units back to what the sender expects
- and the sender would have to had also specified what those units should be
- Hmm, a lot to specify. It may be easier just to create different murphys to handle such cases if there aren't many.
"""

import query

# func_dict={'murphy005': lambda p: murphy005(p)}
func_dict={'murphy005': lambda p: murphy005(p),  #not sure we will need the formatting with this implementation
           'murmkv004': lambda v: murmkv004(v),
            'murmkv003': lambda v: murmkv003(v)
           }
# BEGIN THE MURPHY FUNCTIONS - that call the specified murphy ######################################

def murphy_mkv(person, murphy_num, maps_keys_values):
    """here the murphy is being told by the caller the murphy_num AND what values to evaluate
    this would typically be for a single key and for math operations: averages, trends, etc.
    :param person: person whose values to operate on
    :type person: str
    :param murphy_num: the murphy to do
    :type murphy_num: str
    :param maps_keys_values: which key(s) and time specification of which values (by last, earliest, latest) to use
    :type maps_keys_values: list
    :return: the output of the murphy
    """
    values = []
    for mkv in maps_keys_values:
        key = mkv[1]
        valuespec = mkv[2]
        if not valuespec:                            # if there is not time specification of values to receive
            v = query.adat_person_key(person, key)   # default is to get the most recent
            values.append(v[1])
        if valuespec:
            try:
                last = valuespec[0]
            except:
                last = 1
            try:
                earliest = valuespec[1]
            except:
                earliest = None
            try:
                latest = valuespec[2]
            except:
                latest = None
            vs = query.adat_person_key_options(person, key, last, earliest, latest)
            for v in vs:
                values.append(v[1])
    result = func_dict[murphy_num](values)
    datas = {'data': [{'k': key, 'v': (str(result)), 'vt': 'f', 'units': None}]}
    return datas



def murphy(person, murphy_num):
    """here the murphy is being told by the caller only the murphy_num
    this would typically be for things (like BMI) where the values to call are built into the murphy
    :param person: person whose values to operate on
    :type person: str
    :param murphy_num: the murphy to do
    :type murphy_num: str
    :return: the output of the murphy
    """
    result = func_dict[murphy_num](person)
    return result  # but then it needs trimming after reception in the murphy

# ### END THE MURPHY FUNCTIONS - that call the specified murphy ######################################


# BEGIN THE ACTUAL MURPHYS  #############################################################
# Their name is their murphy_num


def murmkv003(values):
    """ # calculate average of a list of values
    :param values: list with a series of numbers in it
    :type values: list
    :return: the average of the numbers submitted
    """
    a = values
    if a:
        result = sum(a) / len(a)
        return result
    else:
        return []


def murmkv004(values):
    """  receives a weight and height and calculates a returns the BMI
    :param values: height and weight
    :type values: list with two numbers
    :return: BMI
    """
    a, b = values[0], values[1]
    result = round(a / b ** 2, 1)
    return result


def murphy005(person):
    """   receives a person and calculates and returns the BMI
    :param person: person
    :type person: str
    :return: BMI
    """
    a, b = query.adat_person_key(person, '~19')[1], query.adat_person_key(person, '~45')[1]  # get last height & wt
    a, b = float(a), float(b)
    result = round(a / b ** 2, 1)
    datas ={'data': [{'k': '~47', 'v': (str(result)), 'vt': 'f', 'units': None}]}
    return datas


# ### END THE ACTUAL MURPHYS #############################################################


"""
Other possible murphy ideas
trend - this could innumerably complex, depending on how many values, recency, 
  range of measurement error, short term or long term, etc.
  so, trend will be a pretty interesting function
outlier - to score as high or low might also be a function that could be invoked. 
  It would mean hitting a reference table that would have to be local
"""