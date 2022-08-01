#!/usr/bin/python

import argparse
import csv
import sys

'''
This script takes a CSV file with a mandatory header and a sql tablename and converts the data in the csv file into
an SQL INSERT statement.
'''


def parse_arguments():
    # initialize argumentparser and arguments
    parser = argparse.ArgumentParser(description='Takes a csv file and a tablename and creates an SQL insert statement')
    parser.add_argument('csvFile', type=argparse.FileType('r'), help='The CSV file to be read')
    parser.add_argument('-t', '--table', dest='tablename', help='The name of the destination SQL table', required=True)
    parser.add_argument('-d', '--delimiter', dest='delimiter', default=',', help='The delimiter used in the CSV')
    parser.add_argument('-o', '--output', dest='output', default='stdout', help='The output of the SQL statement')

    # parse arguments
    args = parser.parse_args()
    return args


def output_statement(args, output=sys.stdout):
    # Open CSV and start output
    with args.csvFile as f:
        reader = csv.reader(f, delimiter=args.delimiter, quoting=csv.QUOTE_ALL)

        # Create the header row, since we may have to repeat it
        header_row = 'INSERT INTO ' + args.tablename + ' ('
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
            for item in row:
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
            with open(args.output, 'w') as f_handler:
                sys.stdout = f_handler
                output_statement(args)
        else:
            output_statement(args)
    except Exception as e:
        raise e


if __name__ == "__main__":
    main()
