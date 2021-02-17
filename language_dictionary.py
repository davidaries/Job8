"""This modules contains the language dictionary to be used in the program
It will at the completion of Job 7 be replaced by a process that imports the language dictionary from
a SQLite table.
:param english: this dictionary contains the english vocabulary used in this program.  Based on the key value
    the corresponding word is returned.  The layout for the key value is '~NUMBER'
:type english: dict
:param spanish: this dictionary contains the spanish vocabulary used in this program.  Based on the key value
    the corresponding word is returned.  The layout for the key value is '~NUMBER'
:type spanish: dict
:param language_dictionary: this dictionary contains both english and spanish dictionaries for easy access
    to both dictionaries.  It allows language preference (~101 for english) (~102 for spanish) to be used
    as a key to link to the corresponding dictionary and retrieve the specific word requested
:type language_dictionary: dict
"""
english = {
    '~1': 'Name',
    '~2': 'diagnosis',
    '~3': 'treat',
    '~4': 'Hello! Please treat:',
    '~5': 'flu',
    '~6': 'Pause',
    '~7': 'Un Pause',
    '~8': 'Return',
    '~9': 'Event',
    '~10': 'Time',
    '~11': 'Job',
    '~12': 'Timer',
    '~13': 'Log',
    '~14': 'Sex',
    '~15': 'Age',
    '~16': 'Phone',
    '~17': 'Chief Complaint',
    '~18': 'Test',
    '~19': 'Weight',
    '~20': 'Submit',
    '~21': 'Male',
    '~22': 'Female',
    '~23': 'Role',
    '~24': 'Receptionist',
    '~25': 'Assistant',
    '~26': 'Provider',
    '~27': 'Lab Technician',
    '~28': 'Headache',
    '~29': 'Fever',
    '~30': 'COVID',
    '~31': 'Flu Test',
    '~32': 'Coronavirus Test',
    '~33': 'Task',
    '~34': 'Receive',
    '~35': 'Room',
    '~36': 'Diagnose',
    '~37': 'Pneumonia',
    '~38': 'Appendicitis',
    '~39': 'Cholelithiasis',
    '~40': 'Years',
    '~41': 'Kgs',
    '~42': 'User ID',
    '~43': 'Password',
    '~44': 'HgA1c',
    '~45': 'Height',
    '~46': 'Meters',
    '~47': 'BMI',
    '~48': 'Status',
    '~49': 'Priority',
    '~50': 'Forward',
    '~51': 'Reassign',
    '~52': 'Skip',
    '~53': 'Drop',
    '~54': 'Close',
    '~55': 'Assigned',
    '~56': 'Staffers',
    '~57': 'User',
    '~58': 'Action',
    '~59': 'Comments',
    '~100': 'Language Preference',
    '~101': 'English',
    '~102': 'Spanish'
}

spanish = {
    '~1': 'Nombre',
    '~2': 'diagnostico',
    '~3': 'curar',
    '~4': 'Hola! Por favor curar:',
    '~5': 'gripe',
    '~6': 'Pausa',
    '~7': 'Reanudar',
    '~8': 'Regresa',
    '~9': 'Evento',
    '~10': 'Hora',
    '~11': 'Trabajo',
    '~12': 'Temporizador',
    '~13': 'Sesion',
    '~14': 'Sexo',
    '~15': 'Edad',
    '~16': 'Teléfono',
    '~17': 'Problema',
    '~18': 'Prueba',
    '~19': 'Peso',
    '~20': 'Enviar',
    '~21': 'Hombre',
    '~22': 'Mujer',
    '~23': 'Cargo',
    '~24': 'Recepcionista',
    '~25': 'Asistente',
    '~26': 'Doctor',
    '~27': 'Técnico de Laboratorio',
    '~28': 'dolor de cabeza',
    '~29': 'fiebre',
    '~30': 'COVID',
    '~31': 'Prueba de gripe',
    '~32': 'Prueba de COVID',
    '~33': 'Tarea',
    '~34': 'Receive',
    '~35': 'Dar una habitacion',
    '~36': 'Diagnosticar',
    '~37': 'Neumonía',
    '~38': 'Apendicitis',
    '~39': 'Colelitiasis',
    '~40': 'Años',
    '~41': 'Kgs',
    '~42': 'el nombre de usuario',                       #
    '~43': 'la contraseña',
    '~44': 'HgA1c',
    '~45': 'la estatura',
    '~46': 'Meters',
    '~47': 'BMI',      # might be IMC for índice de masa corporal
    '~48': 'Estado',
    '~49': 'Prioridad',
    '~50': 'Reenviar',
    '~51': 'Reasignar',
    '~52': 'Saltarse',
    '~53': 'Soltar',
    '~54': 'Cerrar',
    '~55': 'Asignado',
    '~56': 'Empleados',
    '~57': 'Usuario',
    '~58': 'Accion',
    '~59': 'Comentarios',
    '~100': 'Preferencia de idioma',
    '~101': 'ingles',
    '~102': 'espanol'
}

language_dictionary = {
    "~101": english,
    "~102": spanish
}


def get_text_from_dict(language, text):
    """Function for returning the requested value from the dictionary
    Args:
    :param language: string in format ('~101' for english) ('~102' for spanish) used as a key to choose which
        language dictionary should be returned
    :type language: str
    :param text: string in form '~NUMBER' used to get the specific word from the dictionaries listed above
    :type text: str
    :return: is the requested dictionary value based language and text keys given to the function
    :rtype: str"""
    return language_dictionary.get(language).get(text)
