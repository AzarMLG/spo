def form_list(var, name):
    array = clear_list(var)
    insert_name(array, name)
    return array


def insert_name(array, name):
    array.insert(0, name)


def clear_list(var):
    array = var.split('  ')
    array = list(filter(None, array))
    return array