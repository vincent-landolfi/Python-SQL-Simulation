# Functions for reading tables and databases

import glob
from database import *

# a table is a dict of {str:list of str}.
# The keys are column names and the values are the values
# in the column, from top row to bottom row.

# A database is a dict of {str:table},
# where the keys are table names and values are the tables.

# Write the read_table and read_database functions below


def read_table(filename):
    '''(str) -> Table
    Opens the .csv file and makes the line a table
    REQ: file is in same directory as .py file
    >>>read_table('books.csv')
    '''
    # take the str, make filehandle
    filehandle = open(filename, 'r')
    # read the lines of the file
    line_list = filehandle.readlines()
    # make a blank table
    reader = Table()
    reader.reset()
    # make a blank list to save the keys
    key_list = []
    # go through all of the lines
    for i in range(0, len(line_list)):
        # split at the commas,mutate list
        line_list[i] = line_list[i].strip('\n').split(',')
        # check if it is the first iteration
        if (i == 0):
            # put the keys into the dictionary with blank list
            for j in line_list[i]:
                reader.add_column(j, [])
                # save the actual keys to a list to help later
                key_list.append(j)
        # any other iteration
        else:
            # check for messy inputs
            if (len(line_list[i]) == len(line_list[0])):
                # add proper values to proper table key
                for j in range(0, len(key_list)):
                    reader.add_value(key_list[j], line_list[i][j])
    # close the file
    filehandle.close()
    # return a new table
    return reader


def read_database():
    ''' () -> Database
    Reads all the .csv files in the directory and returns
    a database of all of them.
    '''
    # make the blank database
    database = Database()
    # get a list of all the file names
    file_list = glob.glob('*.csv')
    # go through each of the files
    for i in file_list:
        # get a name for the key
        key_name = i.replace('.csv', '')
        # get the table form read table
        table_name = read_table(i)
        # update our database
        database.add_table(key_name, table_name)
    # return a new database
    return database
