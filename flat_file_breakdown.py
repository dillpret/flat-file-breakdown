import copy
import json
import csv
import os

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

STICK_ALL_SIDES = tk.N + tk.S + tk.E + tk.W

config_file = "config.json"

if os.path.exists(config_file):
    # Load config from JSON
    f = open(config_file, "r", encoding="utf-8")
    config = json.load(f)
    f.close()
else:
    # Create config file
    config = {
        "test": [
            {
                "name" : "Field1",
                "length" : 5
            },
            {
                "name" : "Field2",
                "length" : 3
            }
        ]
    }
    json.dump(config, open(config_file, "w+"), sort_keys=True, indent=2)

unsaved_config_name = "New"
unsaved_config = copy.deepcopy(config)

def parse():
    input_text = flat_input_box.get(1.0, tk.END)
    
    split = split_flat_file(input_text)

    write_friendly(split)
    write_json(split)
    write_csv(split)
    write_string_literal(split)

def split_flat_file(flat_file_string):
    """Splits a flat file into a list of dictionaries"""
    split_rows = []

    for row in flat_file_string.splitlines():
        split_rows.append(split_row(row))
    
    return split_rows
        
def split_row(flat_row):
    split_row = copy.deepcopy(config[selected_config.get()])
    i = 0
    for field in split_row:
        field["value"] = flat_row[i:i + field["length"]]
        i += field["length"]
    return split_row

def write_friendly(row_dictionaries):
    friendly_output_box.delete(1.0, tk.END)
    i = 0
    for dict in row_dictionaries:
        friendly_output_box.insert(tk.INSERT, "\n================== ROW " + str(i) + " ==================\n")
        for field in dict:
            friendly_string = field["name"] + ": " + field["value"] + "\n"
            friendly_output_box.insert(tk.INSERT, friendly_string)
        i+=1

def write_csv(row_dictionaries):
    """Write a CSV representation to a file and the GUI."""
    # Open output csv file
    output_file = "output.csv"
    with open(output_file, "w+", newline="") as output:
        writer = csv.writer(output)

        # Write header
        writer.writerow(field["name"] for field in row_dictionaries[0])

        for dict in row_dictionaries:
            writer.writerow(repr(field["value"]) for field in dict)

    with open(output_file, "r", newline="") as output:
        csv_output_box.delete(1.0, tk.END)
        csv_output_box.insert(1.0, output.read())
    
def write_json(row_dictionaries):
    """Write JSON outputs"""
    json.dump(row_dictionaries[0], open("output.json", "w+"), sort_keys=True, indent=2)

    json_output_box.delete(1.0, tk.END)
    i = 0
    for dict in row_dictionaries:
        json_output_box.insert(tk.INSERT, "\n================== ROW " + str(i) + " ==================\n")
        json_output_box.insert(tk.INSERT, json.dumps(dict, sort_keys=True, indent=2))
        i+=1

def write_string_literal(row_dictionaries):
    """Write C# code to build a string literal"""
    variable_name = selected_config.get()
    output_file = "output.txt"

    with open(output_file, "w+") as string_literal_output:
        string_literal_output.write("string " + variable_name + " = \"\";\n")
        for field in row_dictionaries[0]:
            string_literal_output.write("// [" + str(field["length"]) + "] " + field["name"] + "\n")
            string_literal_output.write(variable_name + " += \"" + field["value"] + "\";\n")

    with open(output_file, "r", newline="") as string_literal_output:
        string_output_box.delete(1.0, tk.END)
        string_output_box.insert(1.0, string_literal_output.read())

def create_text_tab(notebook, name):
    frame = ttk.Frame(notebook)
    set_resizable_inner(frame)
    notebook.add(frame, text=name)
    box = ScrolledText(frame)
    set_resizable_inner(box)
    return box

def set_resizable_inner(widget):
    widget.grid_columnconfigure(0, weight=1)
    widget.grid_rowconfigure(0, weight=1)
    widget.grid(column=0, row=0, sticky=STICK_ALL_SIDES)

def selected_config_changed(*args):
    global unsaved_config
    global unsaved_config_name
    unsaved_config = copy.deepcopy(config)
    unsaved_config_name = selected_config.get()
    populate_config_tab()

def create_new_config():
    global unsaved_config
    global unsaved_config_name
    unsaved_config_name = "new"
    unsaved_config[unsaved_config_name] = [
                {
                    "name": "FieldName",
                    "length": 1
                }
        ]
    populate_config_tab()

def create_new_field():
    global unsaved_config
    global unsaved_config_name
    unsaved_config[unsaved_config_name].append({
        "name": "FieldName",
        "length": 1
    })

def save_config():
    json.dump(unsaved_config, open(config_file, "w+"), sort_keys=True, indent=2)
    selected_config.set(unsaved_config_name)

def populate_config_tab():
    for child in config_edit_frame.winfo_children():
        child.destroy()
    i=0

    tk.Label(config_edit_frame, text="Config Name: ").grid(column=0, row=i, sticky=tk.E)

    config_name_entry = tk.Entry(config_edit_frame, width=50)
    config_name_entry.grid(column=1, row=i, sticky=tk.E + tk.W)
    config_name_entry.insert(0, unsaved_config_name)

    new_config_button = tk.Button(config_edit_frame, text="New Configuration", command=create_new_config)
    new_config_button.grid(column=2, row=i, sticky=tk.E + tk.W)
    i+=1

    tk.Label(config_edit_frame, text="Field Name").grid(column=0, row=i)
    tk.Label(config_edit_frame, text="Field Length").grid(column=1, row=i)
    i+=1
    for field in unsaved_config[unsaved_config_name]:
        name = tk.Entry(config_edit_frame, width=50)
        name.grid(column=0, row=i, sticky=tk.E+tk.W)
        name.insert(0, field["name"])

        length = tk.Entry(config_edit_frame)
        length.grid(column=1, row=i, sticky=tk.E+tk.W)
        length.insert(0, field["length"])

        delete = tk.Button(config_edit_frame, text="Delete")
        delete.grid(column=2, row=i, sticky=tk.E+tk.W)
        i+=1

    new_field = tk.Button(config_edit_frame, text="New Field")
    new_field.grid(column=0, row=i, sticky=tk.E+tk.W)
    i += 1

    new_field = tk.Button(config_edit_frame, text="Save")
    new_field.grid(column=0, row=i, sticky=tk.E + tk.W)

root = tk.Tk()

root.title("Flat File Helper")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

input_tabs = ttk.Notebook(root)
input_tabs.grid(row=0, columnspan=3, sticky=STICK_ALL_SIDES)
input_tabs.grid_rowconfigure(0, weight=1)
input_tabs.grid_columnconfigure(0, weight=1)

flat_input_box = create_text_tab(input_tabs, "Input")

config_edit_frame = ttk.Frame(input_tabs)
config_edit_frame.grid(column=0, row=0, sticky=STICK_ALL_SIDES)
input_tabs.add(config_edit_frame, text="Configuration")

button_parse = tk.Button(root, text="Parse", command=parse).grid(row=1, column=0, sticky=tk.E+tk.W)

tk.Label(root, text="Layout:").grid(row=1, column=1, sticky=tk.E)

options = list(config.keys())
selected_config = tk.StringVar(root)
selected_config.set(options[0])
selected_config.trace("w", selected_config_changed)
option_menu = tk.OptionMenu(root, selected_config, *options)
option_menu.grid(row=1, column=2, sticky=tk.E+tk.W)

selected_config_changed()

output_tabs = ttk.Notebook(root)
output_tabs.grid(row=2, columnspan=3, sticky=STICK_ALL_SIDES)
output_tabs.grid_rowconfigure(0, weight=1)
output_tabs.grid_columnconfigure(0, weight=1)

friendly_output_box = create_text_tab(output_tabs, "Friendly")
string_output_box = create_text_tab(output_tabs, "String")
csv_output_box = create_text_tab(output_tabs, "CSV")
json_output_box = create_text_tab(output_tabs, "JSON")

root.mainloop()