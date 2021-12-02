from canvas import tk


def clean_screen():
    for el in tk.grid_slaves():
        el.destroy()
    for el in tk.pack_slaves():
        el.destroy()


def check_entries_value(data):
    if data == '':
        raise ValueError('Empty string')
    return data
