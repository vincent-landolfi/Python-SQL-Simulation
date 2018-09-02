from reading import *
from database import *

# Below, write:
# *The cartesian_product function
# *All other functions and helper functions
# *Main code that obtains queries from the keyboard,
#  processes them, and uses the below function to output csv results


def print_csv(table):
    '''(Table or Database) -> NoneType
    Print a representation of table.
    >>>princt_csv(movies)
    m.year,m.title,m.studio,m.gross
    1997,Titanic,Par.,2186.8
    2003,The Lord of the Rings: The Return of the King,NL,1119.9
    2010,Toy Story 3,BV,1063.2
    '''
    dict_rep = table.get_dict()
    columns = list(dict_rep.keys())
    print(','.join(columns))
    rows = num_rows(table)
    for i in range(rows):
        cur_column = []
        for column in columns:
            cur_column.append(dict_rep[column][i])
        print(','.join(cur_column))


def num_rows(table):
    '''(Table) -> int
    Takes a Table and determines the number
    of rows that the table has
    >>> num_rows(movies)
    3
    '''
    # get the length of the table
    return table.get_length_columns()


def run_query(database, query):
    '''(Database,str) -> Table
    Takes a database object and a query, and then
    runs the query on the database to create and
    return a table
    REQ: query of form 'select x from y (where x=z)'
    >>> run_query(database,'select book.year from books')
    '''
    # make blank table to work with
    work_table = Table()
    # make an empty list of rows to delete
    delete_list = []
    # split the query
    query = query.split()
    # go check which tables we're taking from, make list
    query[3] = query[3].split(',')
    # check if we have more than one table
    if (len(query[3]) > 1):
        # make the cartesian product
        for i in range(0, len(query[3]) - 1):
            # do the cartesian product of two values for first time
            if (i == 0):
                # cartesian product of first two
                work_table = cartesian_product(database.get_table_value(
                    query[3][i]), database.get_table_value(query[3][i + 1]))
            # if it is not the first time
            else:
                # do the cartesian product with the previous
                work_table = cartesian_product(
                    work_table, database.get_table_value(query[3][i + 1]))
    # check if there is a 'where' clause
    if (len(query) > 4):
        # split the where clauses
        query[5] = query[5].split(',')
        # check if there are spaces
        if (len(query) > 6):
            # go through the extra words in the where clause
            for i in range(6, len(query)):
                # And the extra words to the query were testing
                query[5][0] += (' ' + query[i])
        # check if we have only one table
        if (len(query[3]) == 1):
            work_table = database.get_table_value(query[3][0])
        # go through the where clauses
        for j in query[5]:
            # go through the values in each row
            for i in range(0, work_table.get_length_columns()):
                # check if the statement is false
                if not(evaluate_where(j, work_table, i)):
                    delete_list.append(i)
        for num in range(len(delete_list) - 1, -1, -1):
            work_table.delete_row(delete_list[num])
    # now take care of the columns wanted
    # split the columns at the commas
    query[1] = query[1].split(',')
    # check if we have more than one table
    if (len(query[3]) > 1):
        # get all the columns from the current table
        current_columns = list(work_table.get_columns())
    # if we only have one table
    else:
        # get all the columns from the one table
        current_columns = list(
            database.get_table_value(query[3][0]).get_columns())
        # use the table at query[3][0] for deleting
        work_table = database.get_table_value(query[3][0])
    # go through the columns in the current table
    for i in current_columns:
        # check if we want to delete the column
        if (i not in query[1] and query[1][0] != '*'):
            # delete the column
            work_table.delete_column(i)
    # return the table we worked with
    return work_table


def cartesian_product(table1, table2):
    '''(Table,Table) -> Table
    The cartesian product of two tables is a new table
    where each row in the first table is paired with
    every row in the second table
    REQ: table1,table2 in database
    '''
    # make empty dicts for the product
    cartesian1 = Table()
    cartesian2 = Table()
    # get the two lists of keys from each table
    keys1 = table1.get_columns()
    keys2 = table2.get_columns()
    # go through the first table
    for i in keys1:
        # make an empty list for values
        value_list = []
        # go the the elements of the list value at the key
        for j in range(0, table1.get_length_columns()):
            # apply the same value, table2 length times
            for k in range(0, table2.get_length_columns()):
                # update the value list with the values obtained
                value_list.append(table1.get_value_index(i, j))
        # put the completed value list in the cartesian dict
        cartesian1.add_column(i, value_list)
    # go through the second table
    for i in keys2:
        # list of empty values
        value_list2 = []
        # go the the elements of the list value at the key
        for j in range(0, table1.get_length_columns()):
            # apply the same value, table2 length times
            for k in range(0, table2.get_length_columns()):
                # update the value list with the values obtained
                value_list2.append(table2.get_value_index(i, k))
        # add the made list to the proper key
        cartesian2.add_column(i, value_list2)
    # combine the two lists together
    cartesian1.merge_tables(cartesian2)
    # return the merged tables
    return cartesian1


def evaluate_where(where_clause, table, index):
    '''(list,table,int) -> bool
    Takes the where clause and tells the
    program whether it is True or False
    at various instances.Index is the index of the row.
    >>> evaluate_where(['book.year=2015'],books,2)
    False
    >>> evaluate_where(['book.year=2015'],books,3)
    True
    '''
    # make a list of operators to look for
    op_list = ['>', '=']
    # go through the letters in the clause
    for i in where_clause:
        # find the operator
        if (i in op_list):
            # get first key by going from beginning to operator
            t1 = where_clause[0:where_clause.index(i)]
            # get the operator
            op = i
            # get second key by going from operator to end
            t2 = where_clause[where_clause.index(i) + 1:len(where_clause)]
            # check if there are quotes after the equal sign
            if ('"' in t2) or ("'" in t2):
                # get rid of the quotes
                t2 = t2[1:-1]
    # check if the operator is equals
    if (op == '='):
        # check if the value isn't hard coded
        if (t2 in table.get_columns()):
            # check if the actual values equal each other
            ret_bool = (table.get_value_index(t1, index).lstrip() ==
                        table.get_value_index(t2, index).lstrip())
        # if the value is had coded
        else:
            # check if it equals the hard coded value
            ret_bool = (table.get_value_index(
                t1, index).lstrip() == t2.lstrip())

    # check if the operator is greater than
    elif (op == '>'):
        # check if the value isn't hard coded
        if (t2 in table.get_columns()):
            # check if the actual values equal each other
            ret_bool = (table.get_value_index(t1, index).lstrip() >
                        table.get_value_index(t2, index).lstrip())
        # if the value is had coded
        else:
            # check if it equals the hard coded value
            ret_bool = (table.get_value_index(t1, index).strip() > t2.lstrip())
    # return the boolean resolving each expression
    return ret_bool


if(__name__ == "__main__"):
    query = input("Enter a SQuEaL query, or a blank line to exit:")
    database = read_database()
    print_csv(run_query(database, query))
