""" pe.py is the home of the protocol engine 'PE'. It is called by the controller when the program starts and never
    returns anything to the controller, rather it just keeps doing its thing. It is effectively the heart of the
    program, keeping things happening within protocols, going step by step, and sometimes forking or branching or
    passing along to other protocols.
"""

import datetime
import random
import initial_load_data as ild
import working_data as wd
import get_responsible_staff as grs
import murphy
import decisioning
import simulation_time as sim_time
from icecream import ic

# START - PE - the Protocol Engine #############################################################################
def protocol_engine(pe_ins_sol, pe_ins_unsol, pe_outs, pe_waits, pdata):
    """ The protocol engine 'PE' starts by receiving any existing queues: pe_ins_sol, pe_waits, pe_ins_unsol, pe_outs,
        and also pdata - which are empty lists or dictionaries, because it needs to write to each.
        Things can come into PE in one of two queues
        - pe_ins_sol - are inputs to PE that it did request (solicited) - from the UI (and someday external agents)
        - pe_ins_unsol - are inputs to PE that is did not request (unsolicited) - from the UI (and someday external agents)
        PE first processes any solicited inputs (see: if pe_ins_sol)
        PE then processes any unsolicited inputs (see: if pe_ins_unsol)
        Processing of each of each pe_in_sol and pe_in_unsol generates a line which is put into pdata_addendum
        - and also any calls (for others steps to be done) are added to a calls_list
        pdata_addendum is then processed (see: if pdata_addendum)
        - to be written to pdata
        - for any 'datas' to be expanded into adat
        Then the calls_list is processed - the next steps are called (see: if calls_list)
        - note, some steps (murphys and decisionings) so the step in called/executed within the call_list processing
            whereas others (UI and at some point external agents) must be written to pe_outs & pe_waits
            and await something in (to be pe_ins) before the step can be completed.
    :param pe_ins_sol: queue of solicited inputs
    :type pe_ins_sol: list
    :param pe_ins_unsol: queue of unsolicited inputs
    :type pe_ins_unsol: list
    :param pe_outs: things PE it putting out for staffers (via the UI) to do. (And someday external agents)
    :type pe_outs: dict
    :param pe_waits: for each pe_outs this is data needed to process what comes back. Matched to pe_outs by the token
    :type pe_waits:dict
    :param pdata: data to be recorded for each step processed
    :type pdata: list
    """
    global sim_time
    pdata_appendums = []
    calls_list = []

    if pe_ins_sol:
        replacing_pe_outs = []
        replacing_pe_waits = []
        while pe_ins_sol:
            pe_in_sol = pe_ins_sol.pop(0)
            token_in = pe_in_sol[0]
            pe_wait = pe_waits[token_in]
            # Here we gather the data to append a new row to pdata
            pdatm = random.randint(100001, 999999)  # this to be replaced by get global next datm call
            person = pe_wait[3]
            entity = pe_wait[4]
            caller = pe_wait[5]
            protocol = pe_wait[6]
            step = pe_wait[7]
            thread = pe_wait[8]
            datas = pe_in_sol[2]
            record_dts = sim_time.get_time_stamp()
            pdata_appendum = [pdatm, person, entity, caller, protocol, step, thread, record_dts, datas]
            pdata_appendums.append(pdata_appendum)
            calls = pe_wait[9].get('call')
            # Here we deal with submissions via the UI that have a flow key (with a value of drop, skip, or return)
            if datas.get('flow') == '~53':       # if instruction is to drop
                calls = None                      # it stops the protocol flow, nothing subsequent is called
            elif datas.get('flow') == '~52':     # if instruction is to skip
                pass                              # protocol continues just the same (no change to calls)
            elif datas.get('flow') == '~8':  # if instruction is to return
                # protocol continues just the same (no change to calls), but we need to
                # - repost the task to the person with a status of return
                # - have pe_waits[9], which is flow, be empty
                new_token = random.randint(1000000000000001, 9999999999999999)
                returning_pe_wait_core = pe_wait
                returning_pe_wait_core[9] = {}
                replacing_pe_wait = [new_token, returning_pe_wait_core]  ###
                replacing_pe_waits.append(replacing_pe_wait)
                returning_pe_out_core = pe_outs[pe_wait[0]][token_in]
                returning_pe_out_core[8] = '~8'
                replacing_pe_out = [pe_wait[0], new_token, returning_pe_out_core] ####
                replacing_pe_outs.append(replacing_pe_out)
            if calls:  # there can be more than one call
                for call in calls:
                    calls_list.append([call, pdata_appendum, pe_outs, pe_waits])    # Jan 22 wondering if we need to / should send pe_outs and pe_waits to the call_list every time
            # And finally need to remove the lines processed from pe_outs and pe_waits
            del pe_outs[pe_waits[token_in][0]][token_in]
            del pe_waits[token_in]

            # Now we add to (replace) in pe_outs and pe_waits things staffers said they would come back to
            for replacing_pe_out in replacing_pe_outs:
                pe_outs[replacing_pe_out[0]][replacing_pe_out[1]] = replacing_pe_out[2]  # adds to pe_outs

            for replacing_pe_wait in replacing_pe_waits:
                pe_waits[replacing_pe_wait[0]] = replacing_pe_wait[1]  # adds to pe_waits


    if pe_ins_unsol:
        while pe_ins_unsol:
            pe_in_unsol = pe_ins_unsol.pop(0)
            token_in = pe_in_unsol[0]
            # Here we compile the data to append a new row to pdata
            pdatm = random.randint(100001, 999999)  # this to be replaced by get global next datm call
            person = pe_in_unsol[2].get('person')
            entity = pe_in_unsol[2].get('entity')
            caller = None  # since there is no caller row
            protocol = pe_in_unsol[0]   # for unsolicited inputs pe_in[0] will be the name of the unsolicited protocol
            step = 1  # hmm - will it always be 1?
            thread = random.randint(100001, 999999)  # this to be replaced by get global next thread call
            datas = None  # Do not expect unsolicited pe_ins to carry data to be written to adat (could be dangerous)
            record_dts = sim_time.get_time_stamp()
            # and then create the row to append and append
            pdata_appendum = [pdatm, person, entity, caller, protocol, step, thread, record_dts, datas]
            pdata_appendums.append(pdata_appendum)
            calls = pe_in_unsol[2].get('call')
            if calls:
                for call in calls:
                    calls_list.append([call, pdata_appendum, pe_outs, pe_waits])     # Jan 22 wondering if we need to / should send pe_outs and pe_waits to the call_list every time

    if pdata_appendums:
        for pdat in pdata_appendums:
            pdata.append(pdat)
            if pdat[8]:
                datums = pdat[8].get('data')  # if KVP data for expansion it is added to adat
                if datums:  # we gather the additional data needed to append to adat
                    for datum in datums:
                        datas_expansion(pdat[1], pdat[2], pdat[0], datum)
    pdata_appendum, pdata_appendums = [], []

    if calls_list:
        while calls_list:

            call = calls_list.pop(0)  # now we need to get what they are calling
            proto_ = call[0][0]
            step_ = call[0][1]
            call_type = ild.protocols[proto_][step_][2]
            if call_type in ['murphy', 'murphy_mkv']:
                if call_type == 'murphy':
                    spec = ild.protocols[proto_][step_][3]
                    datas = murphy.murphy(person, spec)
                else:
                    murphy_num = ild.protocols[proto_][step_][3][0]
                    spec = ild.protocols[proto_][step_][3][1]
                    datas = murphy.murphy_mkv(person, murphy_num, spec)
                # now we need to create the line to write to pdata
                pdatm = random.randint(100001, 999999)
                entity = call[1][2]
                caller = call[1][0]
                protocol = proto_
                step = step_
                thread = call[1][6]
                record_dts = sim_time.get_time_stamp()
                pdata_appendum = [pdatm, person, entity, caller, protocol, step, thread, record_dts, datas]
                pdata.append(pdata_appendum)   # append to pdata
                datas_expansion(person, entity, pdatm, datas['data'][0])  # call expansion of murphy-created to adat
                calls_from_murphy = ild.protocols[proto_][step_][5].get('call')  # now time to think routing
                if calls_from_murphy:   # if the murphy step had calls specified
                    for call_fm in calls_from_murphy:
                        call_type_fm = ild.protocols[call_fm[0]][call_fm[1]][2]    # what is the call_type from murphy?
                        if call_type_fm == 'UI':
                            process_call_for_pe_queues(call_fm, pdata_appendum, pe_outs, pe_waits)  # send to UI process
                        elif call_type_fm in ['murphy', 'decisioning']:
                            calls_list.append([call_fm, pdata_appendum, pe_outs, pe_waits])  # append here for process
            elif call_type == 'UI':                # send to UI process
                process_call_for_pe_queues(call[0], call[1], call[2], call[3])
            elif call_type == 'decisioning':
                existing_calls_for_step = ild.protocols[proto_][step_][5].get('call')  # get any pre-specified steps
                for existing_call in existing_calls_for_step:                          # for each step append it here.
                    calls_list.append([existing_call, pdata_appendum, pe_outs, pe_waits])
                decision_spec = ild.protocols[proto_][step_][3]          # get the decision spec
                new_calls = decisioning.decision(person, decision_spec)  # get any new calls pers decision spec
                if new_calls:                                             # if calls append each step
                    for new_call in new_calls.get('call'):
                        calls_list.append([new_call, pdata_appendum, pe_outs, pe_waits])
            else:                                       # at some future point there will be other call_types
                pass
# ### END - PE - the Protocol Engine #############################################################################


# START - supporting functions ###################################################################################
def process_call_for_pe_queues(call, pdata_appendum, pe_outs, pe_waits):
    """ Process calls to made to UI (and in future to external agents)
    creating a new pe_out and pe_wait - by calling create_pe_queues_additions
    then appending them to pe_outs and pe_waits
    :param call: the protocol and step to call and its priority
    :type call: list
    :param pdata_appendum: the pdata to append
    :type pdata_appendum: list
    :param pe_outs: existing pe_outs
    :type pe_outs: dict
    :param pe_waits: existing pe_waits
    :type pe_waits: dict
    """
    pe_out, pe_wait = create_pe_queues_additions(call, pdata_appendum)  # call function to get pe_out & pe_wait
    pe_outs[pe_out[0]][pe_out[1]] = pe_out[2]    # this adds the new pe_out to pe_outs
    if pe_wait[1]:    # this if because without it when a protocol ended we'd get a empty pe_wait written anyway
        pe_waits[pe_wait[0]] = pe_wait[1]        # this adds the new pe_wait to pe_waits


def create_pe_queues_additions(call, pdata_appendum):
    """ called by process_call_for_pe_queues to create the additions for two pe queues: pe_outs and pe_waits
    :param call: the protocol and step to call and its priority
    :type call: list
    :param pdata_appendum: pdata to be used
    :type pdata_appendum: list
    :return: pe_out, pe_wait
    """
    # for reference pdata_appendum = [pdatm[0], person[1], entity[2], caller[3],
    #                                 protocol[4], step[5], thread[6], record_dts[7], datas[8]]
    protocol, step, priority = call[0], call[1], call[2]
    token = random.randint(1000000000000001, 9999999999999999)
    # the next fields are read directly from pdata_addendum
    caller = pdata_appendum[0]
    person = pdata_appendum[1]
    entity = pdata_appendum[2]
    thread = pdata_appendum[6]
    if step == 1:   # if this is the first step in a protocol it needs a new thread number
        thread = random.randint(100001, 999999)
    # the next four are from the protocol specification for that step
    task = ild.protocols[protocol][step][1]
    task_type = ild.protocols[protocol][step][2]
    spec = ild.protocols[protocol][step][3]
    flow = ild.protocols[protocol][step][5]
    # then a few more loose fields
    time_posted = sim_time.get_time_stamp()
    time_reposted = None    # this start empty
    status = '~55'          # the initial status is assigned (~55)
    log = None              # this starts empty
    # here we run the grs function to get what device to write to
    device_out = str(grs.get_device_out(protocol, step))
    # and now we compile the two items to be returned
    pe_out = [device_out, token, [person, entity, priority, task,
              task_type, spec, time_posted, time_reposted, status, log]]
    pe_wait = [token, [device_out, log, time_posted, person, entity, caller, protocol, step, thread, flow]]
    return pe_out, pe_wait


def datas_expansion(person, entity, parent, datum):
    """ writes a pdata it receives to adat
    :param person: person whose data it is
    :type person: str
    :param entity: entity that the data applies to
    :type entity: str
    :param parent: the pdatm (id) of the pdata row of this data
    :type parent: int
    :param datum: data to be expanded
    :type datum: dict
    """
    global sim_time
    adatm = random.randint(1001, 9999)  # this to be replaced by get global next datm call
    k = datum['k']
    vt = datum['vt']
    v = datum['v']
    units = datum['units']
    event_dts = sim_time.get_time_stamp()   # someday beyond more complex for microbio etc.
    adat_ = [person, k, [adatm, entity, parent, vt, v, units, event_dts]]
    try:
        wd.adat[adat_[0]][adat_[1]].append(adat_[2])
    except:
        wd.adat[adat_[0]][adat_[1]] = [adat_[2]]
# ### END - supporting functions #################################################################################
