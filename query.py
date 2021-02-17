"""query.py
   receives requests for data, with keys and value selection criteria, and returns them.
   can be used by the UI (including viewers), PE, Murphy, EE, etc.
   it returns any empty list when a query comes up empty
      it is up the whatever used query to deal with not getting a result, or not getting as many as requested
 If something that queries needs multiple keys, it should query multiple times. (Bundling of queries was removed).
 Also, for now skipping entity as a possible criteria (the examples in my head don't need distinction)

WARNING: the proper function of this depends on the values in adat being in chronological order
         from oldest to newest. If that's the not the case, this is totally not going to work.
         What this would mean is practice is:
         1. when adat is compiled at the time of expansion, there is a mechanism to be sure they are properly sorted.
         2. when an adat is added real-time, it should be appended and that works
         3. well, excepting perhaps for both #1 and #2, the situations where event_dts is different than record_dts
         4. that could/would need special attention. Where to build that in?

Here is thinking about returning data by time constraints (after earliest, before latest)
- it could go in the query
- or it could be done in the context of what called query
- but there might be times you when you want a time constraint (e.g., only from that hospitalization)
- so wouldn't it be nice to handle that once in the query, rather than needing a second step after data is returned?
Okay - earliest and latest functionality added
Didn't specify a explicit way to do "all" - for now just specify a really early earliest (e.g., 1) would work
"""

import \
    initial_load_data as ild  # query needs to be able to access the data in adat (currently found in initial_load_data.py)
import working_data as wd


def adat_person_key(person, key):
    """ this query by default returns only the latest (most recent) value for the key for the person

    :param person: the person to get the value for
    :type person: str
    :param key: the key to get the value for
    :type key: str
    :return: list[timestamp, value, value type]
    """
    adat = wd.adat
    values = adat[person].get(key)
    if not values:
        return []      # if no values returns an empty list
    return [values[-1][6], values[-1][4], values[-1][5]]


def adat_person_key_options(person, key, last=None, earliest=None, latest=None):
    """ this query by returns values for the key for the person by options of how many and/or earliest and latest

    :param person: the person to get the value for
    :type person: str
    :param key: the key to get the value for
    :type key: str
    :param last: how many values to return (starting with most recent)
    :type last: int
    :param earliest: earliest datetimestamp for a value to return
    :type earliest: float
    :param latest: latest datetimestamp for a value to return
    :type latest: float
    :return: list of lists, each internal list as [timestamp, value, value type]
    """
    adat = wd.adat
    values = adat[person].get(key)
    if not values:
        return []        # if no values returns an empty list
    valued = []
    if last:  # it will return up to that number. If len(values) < last it will return all values, however many.
        last_values = values[-last:]
        for each in last_values:
            valued.append([each[6], each[4], each[5]])
    else:
        for each in values:
            valued.append([each[6], each[4], each[5]])
    # Note: earliest and latest do operate on the output of latest if it was specified
    if earliest:  # if earliest it will only return values with times > earliest
        valued_in = tuple(valued)
        valued = []
        for each in valued_in:
            if each[0] > earliest:
                valued.append(each)
    if latest:  # if latest it will only return values with times < latest
        valued_in = tuple(valued)
        valued = []
        for each in valued_in:
            if each[0] < latest:
                valued.append(each)
    return valued  # returns value after last, earliest, latest have all had the chance to filter the values

