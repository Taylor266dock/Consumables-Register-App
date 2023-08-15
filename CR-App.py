import tkinter
import customtkinter as ct
import pandas as pd
import os
import datetime as dt
from os.path import isfile
from CTkMessagebox import CTkMessagebox
import requests
import json
from PIL import Image
from ttkwidgets.autocomplete import AutocompleteEntry

cwd_is = os.path.dirname(__file__) + "/"

TYPE_COLUMNS = ["Id", "Type", "Min Quantity", "Quantity"]
COLUMNS = ["id", "name", "quantity", "last_modified_by", "last_modified_date", "sku", "location", "type", "category"]
HUB_LOCATIONS = ["A1", "A2", "A3", "A4", "B1", "B2", "B4", "C1", "C2", "C3", "C4", "D1", "D2", "D3", "D4",
                 "File Cabinet"]
CATEGORY = ["Cables", "Hardware", "Stationary", "Misc"]
types_list = []
y = 0

window = ct.CTk()
window.wm_title("Consumables Register App")
ct.set_appearance_mode("dark")
# window.attributes("-fullscreen", "True")

title_frame = ct.CTkFrame(window)
title_frame.pack(padx=3, pady=3,)
top_frame = ct.CTkFrame(window)
middletop_frame = ct.CTkFrame(window)
top_frame.pack(padx=3, pady=3,)
top_frame.grid_columnconfigure((0, 1, 3, 2, 4, 5, 6), weight=1, uniform="data")
middletop_frame.pack(fill="x", padx=3, pady=3,)
middletop_frame.grid_columnconfigure((0, 1, 3, 2, 4, 5, 6), weight=1, uniform="labels")
center_frame = ct.CTkFrame(window)
center_frame.pack(fill="both", padx=3, pady=3, expand=True)
center_frame.grid_columnconfigure((0, 1, 3, 2, 4, 5, 6), weight=1, uniform="data")
bottom_frame = ct.CTkFrame(window)
bottom_frame.pack(padx=3, pady=3)

if isfile(cwd_is + "/consumables.csv"):
    get_data = pd.read_csv(cwd_is + "/consumables.csv", index_col=[0])
    data_used = get_data.query("category == 'Cables'")
elif not isfile(cwd_is + "/consumables.csv"):
    with open(cwd_is + "/unique_id.txt", "r") as id_number:
        id_no = int(id_number.readline())
    blank_item = [int(id_no) - 1, "NaN", "NaN", "NaN", "NaN", "NaN", "NaN", "NaN", "NaN"]
    new_data = dict(zip(COLUMNS, blank_item))
    get_data = pd.DataFrame(data=new_data, columns=COLUMNS, index=[id_no])
    data_used = get_data.query("id == '10000'")

if isfile(cwd_is + "/types.csv"):
    get_type = pd.read_csv(cwd_is + "/types.csv", index_col=[0])
    types_list = get_type.Type.values.tolist()

labels_m_t = ["Name", "In Stock", "Received", "Location", "Min", "Plus", "Confirm"]
start_record = 0
end_record = 20

# TOP FRAME
logo_top = ct.CTkImage(light_image=Image.open(cwd_is + "/logo.jpg"), size=(75, 75))
logo_but = ct.CTkLabel(title_frame, image=logo_top, text="")
title_top = ct.CTkLabel(title_frame, text="Consumables Register App")
hardware_tab = ct.CTkButton(top_frame,
                            text="Hardware",
                            command=lambda: [tab_data(CATEGORY[1]), update_whole_table()],
                            )

cables_tab = ct.CTkButton(top_frame,
                          text="Cables",
                          command=lambda: [tab_data(CATEGORY[0]), update_whole_table()],
                          )

stationary_tab = ct.CTkButton(top_frame,
                              text="Stationary",
                              command=lambda: [tab_data(CATEGORY[2]), update_whole_table()],
                              )

misc_tab = ct.CTkButton(top_frame,
                        text="Misc",
                        command=lambda: [tab_data(CATEGORY[3]), update_whole_table()],
                        )
gap = ct.CTkLabel(top_frame, text=" ")
lookup_ = ct.CTkEntry(top_frame,
                      placeholder_text="Search",
                      )

check = ct.CTkButton(top_frame,
                     text="Search",
                     command=lambda: [checkit(), update_whole_table()],
                     )
logo_but.grid(row=0, column=0)
title_top.grid(row=1, column=0)
cables_tab.grid(row=2, column=0, padx=3, pady=3)
hardware_tab.grid(row=2, column=1, padx=3, pady=3)
stationary_tab.grid(row=2, column=2, padx=3, pady=3)
misc_tab.grid(row=2, column=3, padx=3, pady=3)
gap.grid(row=2, column=4, padx=3, pady=3)
lookup_.grid(row=2, column=5, padx=3, pady=3)
check.grid(row=2, column=6, padx=3, pady=3)


def checkit():
    global data_used
    search_term = lookup_.get().strip()
    if get_data["name"].str.contains(search_term, case=False, regex=True).any():
        search_results = get_data[get_data["name"].str.contains(search_term, case=False, regex=True)]
        data_used = search_results
    elif get_data["sku"].str.contains(search_term).any():
        search_results = get_data[get_data["sku"].str.contains(search_term)]
        data_used = search_results
    lookup_.delete(0, 100)
    return data_used


def tab_data(button_pressed):
    global data_used
    global start_record
    global end_record
    if button_pressed == CATEGORY[0]:
        cables_data = get_data.query("category == 'Cables'")
        data_used = cables_data
        start_record = 0
        end_record = 20
        return data_used
    elif button_pressed == CATEGORY[1]:
        hardware_data = get_data.query("category == 'Hardware'")
        data_used = hardware_data
        start_record = 0
        end_record = 20
        return data_used
    elif button_pressed == CATEGORY[2]:
        stationary_data = get_data.query("category == 'Stationary'")
        data_used = stationary_data
        start_record = 0
        end_record = 20
        return data_used
    elif button_pressed == CATEGORY[3]:
        misc_data = get_data.query("category == 'Misc'")
        data_used = misc_data
        start_record = 0
        end_record = 20
        return data_used


# MIDDLETOP
for label in labels_m_t:
    label = ct.CTkLabel(middletop_frame, text=label, anchor="center")
    label.grid(row=0, column=y, padx=3, sticky="ew")
    y += 1


class Line:

    def __init__(self, data_used, number):
        # Name from dataframe
        self.record_name = ct.CTkLabel(center_frame, text=(data_used.iloc[number]["name"]))
        self.record_name.grid(row=number, column=0, padx=3, pady=3, sticky="ew")
        # Quantity from dataframe
        self.record_amount = ct.CTkLabel(center_frame, text=(data_used.iloc[number]["quantity"]))
        self.record_amount.grid(row=number, column=1, padx=3, pady=3, sticky="ew")
        # Number of products to add
        self.entry = ct.CTkEntry(center_frame)
        self.entry.grid(row=number, column=2, sticky="ew")
        # Location from dataframe
        self.record_location = ct.CTkLabel(center_frame, text=(data_used.iloc[number]["location"]))
        self.record_location.grid(row=number, column=3, padx=3, pady=3, sticky="ew")
        # Minus button
        self.minus_but = ct.CTkButton(center_frame, text="-", command=lambda: [self.minus(number, data_used),
                                                                               self.update_table(data_used, number)], )
        self.minus_but.grid(row=number, column=4, padx=3, pady=3, sticky="ew")
        # Plus button
        self.plus_but = ct.CTkButton(center_frame, text="+", command=lambda: [self.plus(number, data_used),
                                                                              self.update_table(data_used, number)], )
        self.plus_but.grid(row=number, column=5, padx=3, pady=3, sticky="ew")
        # Update Amount Button
        self.confirm_Ln_up = ct.CTkButton(center_frame, text="Update",
                                          command=lambda: [self.update_line(number, data_used, get_type),
                                                           self.update_table(data_used, number)])
        self.confirm_Ln_up.grid(row=number, column=6, padx=3, pady=3, sticky="ew")

    def minus(self, line_number, data_used):
        number_of_rows = 0
        for (index, row) in data_used.iterrows():
            if number_of_rows == line_number:
                get_data.loc[row.id, "quantity"] = get_data.loc[row.id, "quantity"].astype(int) - 1
                data_used.loc[row.id, "quantity"] = data_used.loc[row.id, "quantity"].astype(int) - 1
                for (t_index, t_row) in get_type.iterrows():
                    if data_used.loc[row.id, "type"] == get_type.loc[t_row.Id, "Type"]:
                        get_type.loc[t_row.Id, "Quantity"] = get_type.loc[t_row.Id, "Quantity"].astype(int) - 1
                        if get_type.loc[t_row.Id, "Quantity"].astype(int) <= get_type.loc[t_row.Id, "Min Quantity"].astype(int):
                            CTkMessagebox(title="Stock Low Alert",
                                          message=f"You only have {get_type.loc[t_row.Id, 'Quantity'].astype(int)}"
                                                  f" {get_type.loc[t_row.Id, 'Type']} left! Please order more")
                            # slack_message = {"Content": f"You only have {get_type.loc[t_row.Id, 'Quantity'].astype(int)} {get_type.loc[t_row.Id, 'Type']} left! Please order more"}
                            # slack_channel_wh = "slack webhook goes here"
                            # send_slack_message(payload=slack_message, webhook=slack_channel_wh)
            number_of_rows += 1

    def plus(self, line_number, data_used):
        number_of_rows = 0
        for (index, row) in data_used.iterrows():
            if number_of_rows == line_number:
                get_data.loc[row.id, "quantity"] = get_data.loc[row.id, "quantity"].astype(int) + 1
                data_used.loc[row.id, "quantity"] = data_used.loc[row.id, "quantity"].astype(int) + 1
                for (t_index, t_row) in get_type.iterrows():
                    if data_used.loc[row.id, "type"] == get_type.loc[t_row.Id, "Type"]:
                        get_type.loc[t_row.Id, "Quantity"] = get_type.loc[t_row.Id, "Quantity"].astype(int) + 1
            number_of_rows += 1

    def update_line(self, line_number, data_used, get_type):
        number_of_rows = 0
        for (index, row) in data_used.iterrows():
            if number_of_rows == line_number:
                if self.entry.get().isnumeric():
                    get_data.loc[row.id, "quantity"] = get_data.loc[row.id, "quantity"].astype(int) + int(self.entry.get())
                    data_used.loc[row.id, "quantity"] = data_used.loc[row.id, "quantity"].astype(int) + int(self.entry.get())
                    for (t_index, t_row) in get_type.iterrows():
                        if data_used.loc[row.id, "type"] == get_type.loc[t_row.Id, "Type"]:
                            get_type.loc[t_row.Id, "Quantity"] = get_type.loc[t_row.Id, "Quantity"].astype(int) + int(self.entry.get())
                    self.entry.delete(0, 100)
                else:
                    CTkMessagebox(title="Not a Number!",
                                  message=f"You entered {self.entry.get()}, this need to be a number.")
            number_of_rows += 1

    def update_table(self, data_used, record_number):
        self.record_amount = ct.CTkLabel(center_frame, width=175,
                                         text=(data_used.iloc[record_number]["quantity"]))
        self.record_amount.grid(row=record_number, column=1)


p = 1

type_choice = ""

def combobox_callback(choice):
    type_choice = choice
    return type_choice

next_page = ct.CTkButton(bottom_frame,
                         text="Next Page",
                         command=lambda: [next_page_clicked(), update_whole_table()],
                         )
next_page.grid(row=0, column=6, sticky="ew")
prev_page = ct.CTkButton(bottom_frame,
                         text="Previous Page",
                         command=lambda: [previous_page_clicked(), update_whole_table()],
                         )
prev_page.grid(row=0, column=0, sticky="ew")
add_rec_txt = ct.CTkLabel(bottom_frame,
                          text="Add a new record below")
add_rec_txt.grid(row=1, column=0, sticky="ew")
add_rec_nme = ct.CTkLabel(bottom_frame,
                          text="Name")
add_amount_lab = ct.CTkLabel(bottom_frame,
                             text="Amount")

add_sku_lab = ct.CTkLabel(bottom_frame,
                          text="SKU")
hub_location = ct.CTkLabel(bottom_frame,
                           text="Location")
item_type = ct.CTkLabel(bottom_frame,
                        text="Type")
category_txt = ct.CTkLabel(bottom_frame,
                           text="Category")
add_rec_nme.grid(row=2, column=0, padx=3, sticky="ew")
add_amount_lab.grid(row=2, column=1, padx=3, sticky="ew")
add_sku_lab.grid(row=2, column=2, padx=3, sticky="ew")
hub_location.grid(row=2, column=3, padx=3, sticky="ew")
item_type.grid(row=2, column=4, padx=3, sticky="ew")
category_txt.grid(row=2, column=5, padx=3, sticky="ew")
name_entry = ct.CTkEntry(bottom_frame,
                         )

amount = ct.CTkEntry(bottom_frame,
                     )
sku = ct.CTkEntry(bottom_frame,
                  )

add_hub_location = ct.CTkComboBox(bottom_frame,
                                  values=HUB_LOCATIONS)
item_type_input = ct.CTkComboBox(bottom_frame, values=types_list, command=combobox_callback)
category_input = ct.CTkComboBox(bottom_frame, values=CATEGORY,)
confirm = ct.CTkButton(bottom_frame,
                       text="Confirm",
                       command=lambda: [add_item(), update_type_amout_new_item(), update_whole_table()],
                       )
name_entry.grid(row=3, column=0, padx=3, sticky="ew")
amount.grid(row=3, column=1, padx=3, sticky="ew")
sku.grid(row=3, column=2, padx=3, sticky="ew")
add_hub_location.grid(row=3, column=3, padx=3, sticky="ew")
item_type_input.grid(row=3, column=4, padx=3, sticky="ew")
category_input.grid(row=3, column=5, padx=3, sticky="ew")
confirm.grid(row=3, column=6, padx=3, sticky="ew")
exit_prog = ct.CTkButton(bottom_frame,
                         text="Save and Exit",
                         command=lambda: exit_program(),
                         )
exit_prog.grid(row=5, column=6, pady=3, sticky="ew")

add_type_button = ct.CTkButton(bottom_frame,
                        text="Add a Type",
                        command=lambda: type_window_fun(),
                        )
add_type_button.grid(row=5, column=4, pady=3)


def send_slack_message(payload, webhook):
    return requests.post(webhook, json.dumps(payload))


def type_window_fun():
    type_window = ct.CTk()
    type_window.wm_title("Add a Type")
    type_frame = ct.CTkFrame(type_window)
    type_frame.pack()

    add_type_name_lab = ct.CTkLabel(type_frame,
                                    text="Name")
    add_min_amount_lab = ct.CTkLabel(type_frame,
                                     text="Amount")
    add_type_name_lab.grid(row=2, column=0, padx=3)
    add_min_amount_lab.grid(row=2, column=1, padx=3)
    type_name = ct.CTkEntry(type_frame,
                            )

    min_quantity = ct.CTkEntry(type_frame,
                               )

    confirm_type = ct.CTkButton(type_frame,
                                text="Confirm",
                                command=lambda: add_type(),
                                )
    type_name.grid(row=3, column=0, padx=3)
    min_quantity.grid(row=3, column=1, padx=3)
    confirm_type.grid(row=3, column=5, padx=3)

    def reload_main_type():
        item_type_input = ct.CTkComboBox(bottom_frame, values=types_list, command=combobox_callback)
        item_type_input.grid(row=3, column=4, padx=3)

    def add_type():
        global get_type, types_list
        new_item = create_type()
        with open(cwd_is + "/type_id.txt", "r") as id_number1:
            id_no_type = int(id_number1.readline()) - 1
        if not isfile(cwd_is + "/types.csv"):
            new_data1 = dict(zip(TYPE_COLUMNS, new_item))
            types = pd.DataFrame(data=new_data1, columns=TYPE_COLUMNS, index=[id_no_type])
            types.to_csv(cwd_is + "/types.csv")
            get_type = pd.read_csv(cwd_is + "/types.csv", index_col=[0])
            types_list = get_type.Type.values.tolist()
            reload_main_type()
        else:
            new_list_2 = dict(zip(TYPE_COLUMNS, new_item))
            new_data_2 = pd.DataFrame(new_list_2, columns=TYPE_COLUMNS, index=[id_no_type])
            get_type = pd.concat([get_type, new_data_2], axis=0)
            new_types = pd.DataFrame(data=get_type, columns=TYPE_COLUMNS)
            new_types.to_csv(cwd_is + "/types.csv")
            get_type = pd.read_csv(cwd_is + "/types.csv", index_col=[0])
            types_list = get_type.Type.values.tolist()
            reload_main_type()

    def create_type():
        global types_list, get_type
        with open(cwd_is + "/type_id.txt", "r") as id_number_type:
            id_no_type = int(id_number_type.readline())
        new_type = [id_no_type, type_name.get(), min_quantity.get(), 0]
        id_no_type += 1
        with open(cwd_is + "/type_id.txt", "w") as id_number_type:
            id_number_type.write(f"{id_no_type}")
        type_name.delete(0, 100)
        min_quantity.delete(0, 100)
        return new_type

    type_window.mainloop()


def key_entry(sequence):
    if len(lookup_.get()) >= 1:
        checkit()
        update_whole_table()
    elif len(name_entry.get()) >= 1:
        add_item()
    # elif len(new_am1.get()) >= 1 or len(new_am2.get()) >= 1 or len(new_am3.get()) >= 1 or len(new_am4.get()) >= 1 or \
    #         len(new_am5.get()) >= 1 or len(new_am6.get()) >= 1 or len(new_am7.get()) >= 1 or len(new_am7.get()) >= 1 \
    #         or len(new_am8.get()) >= 1 or len(new_am9.get()) >= 1 or len(new_am10.get()) >= 1:
    #     confirm_update()


def exit_program():
    global get_data
    get_type.to_csv(cwd_is + "/types.csv")
    get_data.to_csv(cwd_is + "/consumables.csv")
    window.destroy()


def on_closing():
    # get yes/no answers
    msg = CTkMessagebox(title="Exit?", message="Do you want to close the program?",
                        icon="question", option_1="No", option_2="Yes")
    response = msg.get()

    if response == "Yes":
        exit_program()


def add_item():
    global get_data, type_choice
    with open(cwd_is + "/unique_id.txt", "r") as id_number:
        id_no = int(id_number.readline())
    if amount.get().isnumeric():
        if not isfile(cwd_is + "/consumables.csv"):
            new_item1 = create_item()
            new_data = dict(zip(COLUMNS, new_item1))
            consumables = pd.DataFrame(data=new_data, columns=COLUMNS, index=[id_no])
            consumables.to_csv(cwd_is + "/consumables.csv")
            get_data = pd.read_csv(cwd_is + "/consumables.csv", index_col=[0])
        else:
            new_item2 = create_item()
            new_list_1 = dict(zip(COLUMNS, new_item2))
            new_data_1 = pd.DataFrame(new_list_1, columns=COLUMNS, index=[id_no])
            get_data = pd.concat([get_data, new_data_1], axis=0)
            new_consumables = pd.DataFrame(data=get_data, columns=COLUMNS)
            new_consumables.to_csv(cwd_is + "/consumables.csv")
            get_data = pd.read_csv(cwd_is + "/consumables.csv", index_col=[0])
    else:
        CTkMessagebox(title="Not a Number!", message=f"You entered {amount.get()}, this need to be a number.")


def create_item():
    with open(cwd_is + "/unique_id.txt", "r") as id_number:
        id_no = int(id_number.readline())
    new_item = [id_no, name_entry.get(), amount.get(), os.getenv("user"), dt.datetime.now(), sku.get(),
                add_hub_location.get(), item_type_input.get(), category_input.get()]
    id_no += 1
    with open(cwd_is + "/unique_id.txt", "w") as id_number:
        id_number.write(f"{id_no}")
    name_entry.delete(0, 100)
    amount.delete(0, 100)
    sku.delete(0, 100)
    return new_item  
    
    
    
def update_type_amout_new_item():    
    get_type = pd.read_csv(cwd_is + "/types.csv", index_col=[0])
    for (m_index, m_row) in get_type.iterrows():
        if item_type_input.get() == get_type.loc[m_index, 'Type']:
            get_type.loc[m_row.Id, "Quantity"] = get_type.loc[m_row.Id, "Quantity"].astype(int) + int(amount.get())
            break
    get_type.to_csv(cwd_is + "/types.csv")


def next_page_clicked():
    global start_record, end_record, p
    if data_used.shape[0] % 20 != 0:
        start_record += 20
        end_record += (data_used.shape[0] % 20)
        if (data_used.shape[0] % 20 - end_record) < 0:
            CTkMessagebox(title="Too Far",
                          message="'If you look long enough into the void, the void begins to look back through you.' - Fredrich Nietzche")
    else:
        start_record += 20
        end_record += 20
        if (data_used.shape[0] % 20 - end_record) < 0:
            CTkMessagebox(title="Too Far",
                          message="'If you look long enough into the void, the void begins to look back through you.' - Fredrich Nietzche")
    p += 1


def previous_page_clicked():
    global start_record, end_record, p
    start_record -= 20
    end_record -= 20
    p -= 1
    if start_record < 0:
        CTkMessagebox(title="Too Far",
                      message="'If you look long enough into the void, the void begins to look back through you.' - Fredrich Nietzche")


def update_whole_table():
    global data_used
    clear_frame()
    if data_used.shape[0] < 20:
        for each in range(start_record, data_used.shape[0]):
            line = Line(data_used, each)
        page_num = ct.CTkLabel(bottom_frame, height=1,
                               width=175,
                               text=f"Page {p}",
                               )
        page_num.grid(row=0, column=3)
    else:
        for each in range(start_record, end_record):
            line = Line(data_used, each)
        page_num = ct.CTkLabel(bottom_frame, height=1,
                               width=175,
                               text=f"Page {p}",
                               )
        page_num.grid(row=0, column=3)


def clear_frame():
    for widgets in center_frame.winfo_children():
        widgets.destroy()


if get_data.shape[0] < 1:
    update_whole_table()

window.bind("<Return>", key_entry)

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()
