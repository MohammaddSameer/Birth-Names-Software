#!/usr/bin/env python3

# Run the code with the following command
# ./albertaNames.py -i baby-names-frequency_1980_2020.csv -o albertaOut

# Libraries
import os
import sys
import getopt
import csv
import pandas as pd


def main(argv):

    # Check for correct number of command line arguments
    if len(argv) < 4:
        print("Usage: ./albertaNames.py -i <input file name> -o <output file name>")
        sys.exit(2)

    # Parse command line arguments
    try:
        (opts, args) = getopt.getopt(argv, "i:o:", ["input=", "output="])
    except getopt.GetoptError:
        print("Usage: ./albertaNames.py -i <input file name> -o <output file name>")
        sys.exit(2)

    input_file_name = ""
    output_file_name_base = ""

    for opt, arg in opts:
        if opt == '-h':
            print("Usage: ./albertaNames.py -i <input file name> -o <output file name>")
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file_name = arg
        elif opt in ("-o", "--output"):
            output_file_name_base = arg

    # Initialize data lists
    year_list = []
    sex_list = []
    name_list = []
    count_list = []

    # Open input CSV file and read data
    with open(input_file_name) as csv_file:
        next(csv_file)  # skip the header line
        for i in range(3):
            next(csv_file)  # skip the next three lines
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            name_list.append(row[1].upper())
            count_list.append(int(row[2]))
            sex_list.append("M" if row[3] == "Boy" else "F")
            year_list.append(int(row[4]))

    # Combine data lists into dataframe and format output
    data = {'YEAR': year_list, 'SEX': sex_list, 'FIRST NAME': name_list, 'COUNT': count_list}
    df = pd.DataFrame(data)


    print(df)

    # Output data to CSV file
    output_file_name = output_file_name_base + ".csv"
    df.to_csv(output_file_name, sep=',', index=False, encoding='utf-8')


if __name__ == "__main__":
    main(sys.argv[1:])
