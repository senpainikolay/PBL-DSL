class Variable:
    # class for mapping a value for each key name in the code writen in the built language

    identifier = ''  # name
    value = ''  # symbol

    def __init__(self, identifier, value):
        """
            The constructor of the class
                :param identifier: string
                    key name
                :param value: pandas df
                    value to be assigned to the key
        """
        self.identifier = identifier
        self.value = value
