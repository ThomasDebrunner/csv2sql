#!/usr/bin/python

import argparse
import csv
import sys

'''
This script takes a CSV file with a mandatory header and a sql table_name and converts the data in the csv file into
an SQL INSERT statement.
'''

# Data types for each field.
field_types = []


# Get each types for the current field and return the field name.
def parse_header(field, types=field_types):
    field_name, *field_type = map(str.strip, field.split(':'))
    if field_type == []:
        types.append('TextNotNull')
        return field_name
    field_type = field_type[0].lower()
    if 'text' in field_type and 'not' in field_type and 'null' in field_type:
        types.append('TextNotNull')
    elif 'text' in field_type and 'not' not in field_type:
        types.append('Text')
    elif 'numeric' in field_type and 'not' not in field_type:
        types.append('Numeric')
    elif 'boolean' in field_type and 'not' not in field_type:
        types.append('Boolean')
    elif 'datetime' in field_type and 'not' not in field_type:
        types.append('Datetime')
    else:
        types.append(field_type.capitalize())
    return field_name

# Parse item according to its types.
def parse_item(index, item, types=field_types):
    current_type = types[index]
    result_item = item.replace('\'', '\'\'').replace('"', '\'').replace('&', '&.').replace('""', '"')
    if current_type == 'TextNotNull':
        result_item = '\'' + result_item + '\''
    elif current_type == 'Text':
        result_item = 'NULL' if result_item == '' else '\'' + result_item + '\''
    elif current_type == 'Datetime':
        result_item = 'NULL' if result_item == '' else '\'' + result_item + '\''
    elif current_type == 'Numeric':
        result_item = 'NULL' if result_item == '' else result_item
    elif current_type == 'Boolean':
        result_item = 'NULL' if result_item == '' else result_item
    else:
        result_item = 'NULL' if result_item == '' else result_item
    return result_item


def parse_arguments():
    # initialize argumentparser and arguments
    parser = argparse.ArgumentParser(description='Takes a csv file and a table_name and creates an SQL insert statement')
    parser.add_argument('csv_file', help='The CSV file to be read')
    parser.add_argument('-t', '--table', dest='table_name', help='The name of the destination SQL table', required=True)
    parser.add_argument('-d', '--delimiter', dest='delimiter', default=',', help='The delimiter used in the CSV')
    parser.add_argument('-o', '--output', dest='output', default='stdout', help='The output of the SQL statement')
    parser.add_argument('-e', '--encoding', dest='encoding', default='utf-8', help='Encoding when reading and writing file.')

    # parse arguments
    args = parser.parse_args()
    return args


def output_statement(args, output=sys.stdout):
    # Open CSV and start output
    with open(args.csv_file, 'r', encoding=args.encoding) as f:
        reader = csv.reader(f, delimiter=args.delimiter, quoting=csv.QUOTE_ALL)

        # Create the header row, since we may have to repeat it
        header_row = 'INSERT INTO "' + args.table_name + '" ('
        first = True
        for item in next(reader):
            if first:
                first = False
            else:
                header_row += ', '
            header_row += '"' + parse_header(item) + '"'
        header_row += ') VALUES '

        # Set a counter, since there can't be more than 1000 inserts at a time
        counter = 0

        # Loop through the rows...
        for row in reader:
            if counter % 1000 == 0:
                if counter != 0:
                    print(';', end='\n')
                print(header_row)
            else:
                print(',', end='\n')
            print('(', end='')
            first = True

            # Loop through the items in each row
            for index, item in enumerate(row):
                if first:
                    first = False
                else:
                    print(', ', end='')
                print(parse_item(index, item), end='')
            print(')', end='')
            # Increase counter
            counter += 1

        print(';', end='\n')


def main():
    try:
        # parse arguments
        args = parse_arguments()

        # Redirect stdout
        if args.output != 'stdout':
            with open(args.output, 'w', encoding=args.encoding) as f_handler:
                sys.stdout = f_handler
                output_statement(args)
        else:
            output_statement(args)
    except Exception as e:
        raise e


if __name__ == "__main__":
    main()
