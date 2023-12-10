from SerializeFile import *
from Customer import *
import PySimpleGUI as sg
import re
import operator

filename = 'Customer.csv'
lCustomer = []
pattern_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
pattern_ID = r"\d{3}"
pattern_phone = r"\d{3}-\d{6}"

def addCustomer(customer_list, table_data, customer_object):
    customer_list.append(customer_object)
    saveCustomer(filename, customer_object)
    table_data.append([customer_object.ID, customer_object.name, customer_object.bill,
                       customer_object.phone, customer_object.email, customer_object.posFile])

def delCustomer(customer_list, table_data, pos_in_table):
    pos_in_file = table_data[pos_in_table][-1]
    customer_to_delete = None
    for customer in customer_list:
        if customer.customerinPos(pos_in_file):
            customer_to_delete = customer
            break
    if customer_to_delete is not None:
        customer_list.remove(customer_to_delete)
        table_data.remove(table_data[pos_in_table])
        customer_to_delete.erased = True
        modifyCustomer(filename, customer_to_delete)

def updateCustomer(customer_list, row_to_update, pos_in_file):
    customer_to_update = None
    for customer in customer_list:
        if customer.customerinPos(pos_in_file):
            customer_to_update = customer
            break
    if customer_to_update is not None:
        customer_to_update.setCustomer(row_to_update[1], row_to_update[2], row_to_update[3], row_to_update[4])
        modifyCustomer(filename, customer_to_update)

def sort_table(table, cols):
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table

def create_interface():
    font1, font2 = ('Helvetica', 14), ('Arial', 16, 'bold')
    sg.theme('DarkBlue')
    sg.set_options(font=font1)
    table_data = []

    readCustomer(filename, lCustomer)
    for customer_obj in lCustomer:
        if not customer_obj.erased:
            table_data.append([customer_obj.ID, customer_obj.name, customer_obj.bill,
                               customer_obj.phone, customer_obj.email, customer_obj.posFile])

    layout = [
        [sg.Push(), sg.Text('Customer CRUD'), sg.Push()]] + [
        [sg.Text(text), sg.Push(), sg.Input(key=key)] for key, text in Customer.fields.items()] + [
        [sg.Push()] +
        [sg.Button(button) for button in ('Add', 'Delete', 'Modify', 'Clear')] +
        [sg.Push()],
        [sg.Table(values=table_data, headings=Customer.headings, max_col_width=50, num_rows=10,
                  display_row_numbers=False, justification='center', enable_events=True,
                  enable_click_events=True,
                  vertical_scroll_only=False, select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                  expand_x=True, bind_return_key=True, key='-Table-')],
        [sg.Button('Purge'), sg.Push(), sg.Button('Sort File')],
    ]
    sg.theme('DarkBlue')
    window = sg.Window('Customer Management with Files', layout, finalize=True)
    window['-PosFile-'].update(disabled=True)
    window['-Table-'].bind("<Double-Button-1>", " Double")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        # ... (other code)

    window.close()

# Close the file using the with statement to ensure it is closed properly
with open(filename, 'rb+') as fCustomer:
    pass  # You don't need to do anything here; the with block will take care of closing the file

create_interface()
