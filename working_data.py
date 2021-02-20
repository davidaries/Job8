"""working_data.py
This seems a hydrid module.
1. It is a place to create and reference certain 'global-ish' variables. See lines 7-16
-- Is this how to best do this?
2. It creates some initial entries for the pe_outs dictionary
-- These lines should go away with a proper staff sign-in process
3. It creates an initial adat dictionary for use
-- These lines will go away when the initial adat is created from reading in existing pdata at app startup.
"""

pdata = []             # existing pdata at startup - for now (only) is empty, which is why we have adat below.
pe_ins_sol = []        # protocol engine solicited inputs
pe_ins_unsol = []      # protocol engine unsolicited inputs
pe_waits = {}          # protocol engine waits
pe_outs = {}           # protocol engine outputs

log_dict = {}
token_status_dict ={}
flow_data = {}


# adat is a dictionary where the key is the person, and then each person is a dictionary
# where the key is k, and value is a list with lists (inner lists) within.
# each of the inner lists has the following seven fields.
# adatm[0], entity[1], parent[2], vt[3], v[4], units[5], event_dts[6]
adat = {
    'pers101': {
        '~1': [[101, None, None, 's', 'Tina Quarintina-Hugo-Cortez', None, 1603824276.5]],
        '~14': [[102, None, None, '~', '~22', None, 1603824276.5]],
        '~15': [[103, None, None, 'f', 40, '~40', 1603824276.5]],
        '~16': [[104, None, None, 's', '202-888-5431', None, 1603824276.5]],
        '~17': [[105, None, None, '~', '~28', None, 1603824276.5]],
        '~2': [[116, None, None, '~', '~5', None, 1603824276.5]],
        '~45': [[116, None, None, 'f', 1.7, '~46', 1603800000.5]],
        '~19': [[113, None, None, 'f', 70, '~41', 1603800000.5],
                [114, None, None, 'f', 71, '~41', 1603812000.5],
                [115, None, None, 'f', 72, '~41', 1603824276.5]]
    },
    'pers102': {
        '~1': [[107, None, None, 's', 'Tony Shalhoub', None, 1603824276.5]],
        '~14': [[108, None, None, '~', '~21', None, 1603824276.5]],
        '~15': [[109, None, None, 'f', 35, '~40', 1603824276.5]],
        '~16': [[110, None, None, 's', '703-999-3341', None, 1603824276.5]],
        '~17': [[111, None, None, '~', '~29', None, 1603824276.5]],
        '~2': [[112, None, None, '~', '~30', None, 1603824276.5]],
        '~45': [[116, None, None, 'f', 1.9, '~46', 1603800000.5]],
        '~19': [[116, None, None, 'f', 75, '~41', 1603800000.5],
                [117, None, None, 'f', 74, '~41', 1603812000.5],
                [118, None, None, 'f', 75, '~41', 1603824276.5]]
    },
    'pers103': {
        '~1': [[121, None, None, 's', 'Bill A. Ted', None, 1603824276.5]],
        '~14': [[122, None, None, '~', '~21', None, 1603824276.5]],
        '~15': [[123, None, None, 'f', 21, '~40', 1603824276.5]],
        '~16': [[124, None, None, 's', '703-999-8888', None, 1603824276.5]],
        '~17': [[125, None, None, '~', '~29', None, 1603824276.5]],
        '~2': [[126, None, None, '~', '~30', None, 1603824276.5]],
        '~45': [[116, None, None, 'f', 2.0, '~46', 1603800000.5]],
        '~19': [[127, None, None, 'f', 88, '~41', 1603800000.5],
                [128, None, None, 'f', 92, '~41', 1603812000.5],
                [129, None, None, 'f', 94, '~41', 1603824276.5]]
    },
    'pers104': {
        '~1': [[131, None, None, 's', 'Mary Cobbler', None, 1603824276.5]],
        '~14': [[132, None, None, '~', '~22', None, 1603824276.5]],
        '~15': [[133, None, None, 'f', 66, '~40', 1603824276.5]],
        '~16': [[134, None, None, 's', '703-999-1111', None, 1603824276.5]],
        '~17': [[135, None, None, '~', '~29', None, 1603824276.5]],
        '~2': [[136, None, None, '~', '~30', None, 1603824276.5]],
        '~45': [[116, None, None, 'f', 1.8, '~46', 1603800000.5]],
        '~19': [[137, None, None, 'f', 44, '~41', 1603800000.5],
                [138, None, None, 'f', 43, '~41', 1603812000.5],
                [139, None, None, 'f', 42, '~41', 1603824276.5]]
    },
    'pers105': {
        '~1': [[141, None, None, 's', 'Lisa Lipton', None, 1603824276.5]],
        '~14': [[142, None, None, '~', '~22', None, 1603824276.5]],
        '~15': [[143, None, None, 'f', 35, '~40', 1603824276.5]],
        '~16': [[144, None, None, 's', '703-999-3341', None, 1603824276.5]],
        '~17': [[145, None, None, '~', '~29', None, 1603824276.5]],
        '~2': [[146, None, None, '~', '~30', None, 1603824276.5]],
        '~45': [[116, None, None, 'f', 1.6, '~46', 1603800000.5]],
        '~19': [[147, None, None, 'f', 54, '~41', 1603800000.5],
                [148, None, None, 'f', 56, '~41', 1603812000.5],
                [149, None, None, 'f', 53, '~41', 1603824276.5]]
    },
    'pers106': {
        '~1': [[141, None, None, 's', 'Neal Armstrong', None, 1603824276.5]],
        '~14': [[142, None, None, '~', '~21', None, 1603824276.5]],
        '~15': [[143, None, None, 'f', 18, '~40', 1603824276.5]],
        '~16': [[144, None, None, 's', '612-926-0000', None, 1603824276.5]],
        '~17': [[145, None, None, '~', '~29', None, 1603824276.5]],
        '~2': [[146, None, None, '~', '~30', None, 1603824276.5]],
        '~45': [[116, None, None, 'f', 1.8, '~46', 1603800000.5]],
        '~19': [[147, None, None, 'f', 54, '~41', 1603800000.5],
                [148, None, None, 'f', 56, '~41', 1603812000.5],
                [149, None, None, 'f', 59, '~41', 1603824276.5]]
    }
}