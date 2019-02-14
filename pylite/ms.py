# PyLite commands:
#   CREATE tablename WITH col1 col2 col3
#   ADD col1_val col2_val col3_val TO tablename
#   CHANGE col TO val WHERE colname=val IN tablename
#   GET colname1 colname2 WHERE colname=val FROM tablename
#   REMOVE colname=val FROM tablename
#   DISPLAY tablename
#   DELETE tablename
#   EXIT



# IMPORTS
import os
from sys import argv
from warnings import warn



# DB FUNCTIONALITY
def namefile(tablename):
    return f'dbs{os.sep}{tablename}.db'

def tread(tablename): # dict
    filename = namefile(tablename)
    if os.path.exists(filename):
        table = open(filename, 'r')
        contents = [ line.rstrip() for line in table.readlines() ]
        table.close()
        table = dict()
        columns = contents.pop(0).split(' | ')
        for col in columns:
            table[col] = list()
        for entry in contents:
            values = entry.split(' | ')
            for col, val in zip(columns, values):
                table[col].append(val)
        return table
    else:
        raise ValueError(f"Table '{tablename}' does not exist.")
        
    
def twrite(tablename, table):
    filename = namefile(tablename)
    file = open(filename, 'w')
    file.write( ' | '.join( list( table.keys() ) ) + '\n' )
    length = len( table[ list( table.keys() )[0] ] )
    for i in range(length):
        line = list()
        for col in table:
            line.append(table[col][i])
        file.write( ' | '.join(line) + '\n' )
    file.close()
    
    
def gide(table, key, value): # int
    if key in table:
        try:
            id = table[key].index(value)
            return id
        except ValueError:
            warn(f"There is no '{value}' in the specified column.")
    else:
        raise ValueError(f"Column '{key}' does not exist in the given table.")
        
        
def gcol(table, targets, id):
    out = list()
    for col in targets:
        if col in table:
            out.append(table[col][id])
        else:
            raise ValueError(f"Column '{col}' does not exist in the given table.")
    out = tuple(out)
    return out


def create(tablename, params): # void
    columns = params
    filename = namefile(tablename)
    if os.path.exists(filename):
        warn(f"Table '{tablename}' already exists -- it will be overriden.")
    table = open(filename, 'w')
    table.write( ' | '.join(columns) + '\n' )
    table.close()
    
    
def add(tablename, params): # void
    values = params
    filename = namefile(tablename)
    if os.path.exists(filename):
        table = open(filename, 'a')
        table.write( ' | '.join(values) + '\n')
        table.close()
    else:
        raise ValueError(f"Table '{tablename}' does not exist.")
        
        
def change(tablename, params): # void
    column, fin, key, value = params
    table = tread(tablename)
    id = gide(table, key, value)
    table[column][id] = fin
    twrite(tablename, table)
    
    
def get(tablename, params): # tuple
    targets, key, value = params
    table = tread(tablename)
    id = gide(table, key, value)
    out = gcol(table, targets, id)
    print(out)
    return out
    

def remove(tablename, params): # void
    key, value = params
    table = tread(tablename)
    id = gide(table, key, value)
    for col in table:
        table[col].pop(id)
    twrite(tablename, table)
    
    
def display(tablename, p): # void
    filename = namefile(tablename)
    file = open(filename, 'r')
    table = [ line.rstrip() for line in file.readlines() ]
    file.close()
    for line in table:
        print(line)
    
    
def delete(tablename, p): # void
    filename = namefile(tablename)
    if os.path.exists(filename):
        os.remove(filename)
    else:
        warn(f"Table '{tablename}' does not exist.")
    
    

# COMMAND EXECUTION
def parse(exp): # tuple( func, tablename, tuple(params) )
    splt = exp.split()
    func = splt.pop(0).lower()
    
    if func == 'create':
        tablename = splt.pop(0)
        splt.pop(0)
        params = tuple(splt)
        
    elif func == 'add':
        tablename = splt.pop(-1)
        splt.pop(-1)
        params = tuple(splt)
        
    elif func == 'change':
        tablename = splt.pop(-1)
        splt.pop(-1)
        key, value = tuple( splt.pop(-1).split('=') )
        splt.pop(-1)
        init = splt[0]
        fin = splt[-1]
        params = (init, fin, key, value)
        
        
    elif func == 'get':
        tablename = splt.pop(-1)
        splt.pop(-1)
        key, value = tuple( splt.pop(-1).split('=') )
        splt.pop(-1)
        targets = tuple(splt)
        params = (targets, key, value)
        
    elif func == 'remove':
        tablename = splt.pop(-1)
        splt.pop(-1)
        params = tuple( splt.pop(-1).split('=') )
        
    elif func == 'display':
        tablename = splt.pop(-1)
        params = None
        
    elif func == 'delete':
        tablename = splt.pop(-1)
        params = None
        
    elif func == 'exit':
        exit()
        
    return (func, tablename, params)
    
    

def exec(exp): # void / tuple
#   str   str        tuple    
    func, tablename, params = parse(exp)
    if func in commands:
        return commands[func](tablename, params)
    else:
        raise ValueError("Undefined command. Query failed.")
    
    
    
# GLOBAL VARIABLES
commands = {
    'create'    : create,
    'add'       : add,
    'change'    : change,
    'get'       : get,
    'remove'    : remove,
    'display'   : display,
    'delete'    : delete,
    'exit'      : exit,
}
    


# RUNTIME
def runtime(): # void
    try:
        mode = argv[1]
        while mode == '-t':
            exec( input('~$ ') )
    except IndexError:
        pass
    
    
runtime()
