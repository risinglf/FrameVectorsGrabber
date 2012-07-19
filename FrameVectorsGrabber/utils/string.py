
def str_insert(original, new, pos):
    '''Inserts new inside original at pos. Taken from http://twigstechtips.blogspot.it/2010/02/python-insert-string-into-another.html'''
    return original[:pos] + new + original[pos:]