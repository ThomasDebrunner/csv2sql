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

    # parse arguments
    args = parser.parse_args()
    return args


def main():
    # parse arguments
    args = parse_arguments()

    # Open CSV and start output
    with args.csvFile as f:
        reader = csv.reader(f, delimiter=args.delimiter, quoting=csv.QUOTE_NONE)

        print('INSERT INTO {0} ({1}) VALUES '.format(args.tablename, ','.join(reader.next())))

        first = True
        for row in reader:
            if first:
                first = False
            else:
                sys.stdout.write(',\n')
            sys.stdout.write('(' + ','.join(row) + ')')

        sys.stdout.write(';')


if __name__ == "__main__":
    main()
