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

def create_tab(name):
    output_frame = ttk.Frame(output_tabs)
    set_resizable_inner(output_frame)
    output_tabs.add(output_frame, text=name)
    output_box = ScrolledText(output_frame, height=5)
    set_resizable_inner(output_box)
    return output_box

def set_resizable_inner(widget):
    widget.grid_columnconfigure(0, weight=1)
    widget.grid_rowconfigure(0, weight=1)
    widget.grid(column=0, row=0, sticky=STICK_ALL_SIDES)

root = tk.Tk()

root.title("Flat File Helper")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

flat_input_box = ScrolledText(root, height=5)
flat_input_box.grid(row=0, columnspan=3, sticky=STICK_ALL_SIDES)

button_parse = tk.Button(root, text="PARSE", command=parse).grid(row=1, column=0, sticky=tk.E+tk.W)

#tk.Label(root, text="Layout:").grid(row=2, column=0, sticky=tk.W)

options = list(config.keys())
selected_config = tk.StringVar(root)
selected_config.set(options[0])
option_menu = tk.OptionMenu(root, selected_config, *options)
option_menu.grid(row=1, column=1, sticky=tk.E+tk.W)

output_tabs = ttk.Notebook(root)
output_tabs.grid(row=2, columnspan=3, sticky=STICK_ALL_SIDES)
output_tabs.grid_rowconfigure(0, weight=1)
output_tabs.grid_columnconfigure(0, weight=1)

friendly_output_box = create_tab("Friendly")
string_output_box = create_tab("String")
csv_output_box = create_tab("CSV")
json_output_box = create_tab("JSON")

root.mainloop()