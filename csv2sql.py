#!/usr/bin/python

import argparse
import csv
import sys

'''
This script takes a CSV file with a mandatory header and a sql tableName and converts the data in the csv file into
an SQL INSERT statement.
'''

# TODO:Data types for each field.
field_types = []


def parse_arguments():
    # initialize argumentparser and arguments
    parser = argparse.ArgumentParser(description='Takes a csv file and a tableName and creates an SQL insert statement')
    parser.add_argument('csvFile', help='The CSV file to be read')
    parser.add_argument('-t', '--table', dest='tableName', help='The name of the destination SQL table', required=True)
    parser.add_argument('-d', '--delimiter', dest='delimiter', default=',', help='The delimiter used in the CSV')
    parser.add_argument('-o', '--output', dest='output', default='stdout', help='The output of the SQL statement')
    parser.add_argument('-e', '--encoding', dest='encoding', default='utf-8', help='Encoding when reading and writing file.')

    # parse arguments
    args = parser.parse_args()
    return args


def output_statement(args, output=sys.stdout):
    # Open CSV and start output
    with open(args.csvFile, 'r', encoding=args.encoding) as f:
        reader = csv.reader(f, delimiter=args.delimiter, quoting=csv.QUOTE_ALL)

        # Create the header row, since we may have to repeat it
        header_row = 'INSERT INTO ' + args.tableName + ' ('
        first = True
        for item in next(reader):
            if first:
                first = False
            else:
                header_row += ', '
            header_row += '"' + item + '"'
        header_row += ') VALUES '

        # Set a counter, since there can't be more than 1000 inserts at a time
        counter = 0

        # Loop through the rows...
        for row in reader:
            if counter % 1000 == 0:
                if counter != 0:
                    output.write(';\n')
                print(header_row)
            else:
                output.write(',\n')
            output.write('(')
            first = True

            # Loop through the items in each row
            for index, item in enumerate(row):
                if first:
                    first = False
                else:
                    output.write(', ')
                output.write('\'' + item.replace('\'', '\'\'').replace('"', '\'').replace('&', '&.').replace('""', '"') + '\'')
            output.write(')')
            # Increase counter
            counter += 1

        output.write(';')


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
