import copy
import click
import json
import csv


@click.command()
@click.option('--input_file',
              help='The relative file path of the input file.',
              default ="input.txt")
@click.option('--config_file',
              help='The relative file path of the configuration.',
              default ="config.json")
@click.option('--output_file',
              help='The relative file path of the output file (this will be overwritten if it exists).',
              default ="output.csv")
def split_flat_file(input_file, config_file, output_file):
    """Generates a CSV file from a flat file based on configured field lengths."""
    # Load config from JSON
    f = open(config_file, "r", encoding="utf-8")
    config = json.load(f)
    f.close()

    # Open output csv file
    output = open(output_file, "w+")
    writer = csv.writer(output)

    # Write header
    writer.writerow(field["name"] for field in config["record"])

    # Open input file
    flat_file = open(input_file)

    json_output = copy.deepcopy(config)
    for row in flat_file:
        i = 0
        for field in json_output["record"]:
            field["value"] = row[i:field["length"]]
            i += field["length"]
        writer.writerow(field["value"] for field in json_output["record"])

    # Write JSON output
    json.dump(json_output, open("output.json", "w+"), sort_keys=True, indent=4)



if __name__ == '__main__':
    split_flat_file()
