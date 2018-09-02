class Table():
    '''A class to represent a SQuEaL table'''

    def __init__(self):
        '''(Table,dict of {str: list of str}) -> NoneType

        Creates a new Table using the data from the given
        dictionary
        '''
        # make the class variable equal to table
        self._table = {}

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType

        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        '''
        # make the table the new dict
        self._table = new_dict

    def get_dict(self):
        '''(Table) -> dict of {str: list of str}

        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        # return the table in that class
        return self._table

    def reset(self):
        '''(Table) -> NoneType
        Reset the dictionary in the table to a blank table
        '''
        self._table = {}

    def add_column(self, key, value):
        '''(Table,str,list) -> NoneType
        Adds the column to the dict in the table
        with the list as that value for the key
        '''
        # add the key value pairing to the dict
        self._table.update({key: value})

    def merge_tables(self, table):
        '''(Table,Table) -> NoneType
        Takes two tables which have been prepped for
        the cartesian equation and merges them together
        '''
        # update one table with the other
        self._table.update(table._table)

    def add_value(self, key, value):
        '''(Table,str,str) -> NoneType
        Appends the given value to the list at
        the given key
        '''
        # append the value to the list at that key
        self._table[key].append(value)

    def __str__(self):
        return str(self._table)

    def get_columns(self):
        '''(Table) -> list
        Returns the names of the keys in the dict
        in a list
        '''
        # return the keys in the classes table
        return self._table.keys()

    def get_length_columns(self):
        '''(Table) -> int
        Returns the length of the table in an
        integer
        '''
        # get a list of the keys
        key_list = list(self.get_columns())
        # check if there are keys
        if (key_list != []):
            length = len(self._table[key_list[0]])
        else:
            length = 0
        # get the length of the column
        return length

    def get_length_rows(self):
        '''(Table) -> int
        Returns the number of rows the table
        has
        '''
        # make a list of the keys
        key_list = list(self.get_columns())
        # return the length of one keys list length
        return len(key_list)

    def delete_column(self, column):
        '''(Table,str) -> NoneType
        Delete the given column from the table
        REQ: column is in the table
        '''
        # delete the key:value pairing at that key
        del self._table[column]

    def delete_row(self, row):
        '''(Table,int) -> NoneType
        Delete the row by using the row number
        or index of the list
        REQ: row>=0
        '''
        # go through all the columns
        for i in self.get_columns():
            # delete the list value at given index
            del self._table[i][row]

    def delete_column(self, column):
        '''(Table,str) -> NoneType
        Deletes the given column
        REQ: column in table
        '''
        del self._table[column]

    def get_value_index(self, key, index):
        '''(Table) -> str
        Returns the value at an index of the list
        in the key:value pairing
        REQ: key is in dict
        REQ: index is in list at key
        '''
        # returns the value at that key and index of the value
        return self._table[key][index]

    def get_value(self, key):
        '''(Table) -> list
        Returns the list at the key in the table
        REQ: key is in dict
        '''
        return self._table[key]


class Database():
    '''A class to represent a SQuEaL database'''

    def __init__(self, database={}):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        # make the class variable the given database
        self._database = database

    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        # make the database the new dict
        self._database = new_dict

    def get_dict(self):
        '''(Database) -> dict of {str: Table}

        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        # return the current database variable
        return self._database

    def add_table(self, key, table):
        '''(Database,str,list) -> NoneType
        Adds the column to the database with the
        table as the value
        '''
        # add the key value pairing to the dict
        self._database.update({key: table})

    def __str__(self):
        return str(self._database)

    def get_tables(self):
        '''(Database) -> list of str
        Returns all the tables in the database
        '''
        # return the tables in the databse
        return self._database.keys()

    def get_table_value(self, key):
        '''(Database) -> Table
        Returns the table at the given
        key
        REQ: table(key) is in database
        '''
        return self._database[key]
