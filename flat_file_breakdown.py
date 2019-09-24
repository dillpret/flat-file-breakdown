import copy
import click
import json
import csv

import tkinter as tk
from tkinter.scrolledtext import ScrolledText

root = tk.Tk()

def parse():
    print("PARSE")
    input_text = flat_input_box.get(1.0, tk.END)

    output_text = split_flat_file(input_text)

    output_box.delete(1.0, tk.END)
    output_box.insert(1.0, output_text)

def split_flat_file(flat_file_string):
    """Generates a CSV file from a flat file based on configured field lengths."""
    config_file = "config.json"
    config_key = "test"

    output_file = "output.csv"

    # Load config from JSON
    f = open(config_file, "r", encoding="utf-8")
    config = json.load(f)
    f.close()

    # Open output csv file
    output = open(output_file, "w+", newline="")
    writer = csv.writer(output)

    # Write header
    writer.writerow(field["name"] for field in config[config_key])

    # Read each property of each row, and write to the output CSV
    json_output = copy.deepcopy(config[config_key])
    for row in flat_file_string.splitlines():
        i = 0
        for field in json_output:
            field["value"] = row[i:i + field["length"]]
            i += field["length"]
        writer.writerow(repr(field["value"]) for field in json_output)

    # Write JSON output (of last row)
    json.dump(json_output, open("output.json", "w+"), sort_keys=True, indent=2)

    # Write string literal output (of last row)
    string_literal_output = open("output.txt", "w+")
    string_literal_output.write("string " + config_key + " = \"\";\n")
    for field in json_output:
        string_literal_output.write("// [" + str(field["length"]) + "] " + field["name"] + "\n")
        string_literal_output.write(config_key + " += \"" + field["value"] + "\";\n")

    return json.dumps(json_output, sort_keys=True, indent=2)

root.title("Flat File Helper")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

flat_input_box = ScrolledText(root)
flat_input_box.grid(row=0, column=0, columnspan=3, sticky=tk.N + tk.S + tk.E + tk.W)

button_parse = tk.Button(root, text="Parse", command=parse).grid(row=1, column=0, sticky=tk.W)

output_box = ScrolledText(root)
output_box.grid(row=2, column=0, columnspan=3, sticky=tk.N + tk.S + tk.E + tk.W)

root.mainloop()