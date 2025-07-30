import argparse

def create_parser():
    parser = argparse.ArgumentParser(description='Report generator.')
    parser.add_argument('-o', '--order', default='asc', choices=['asc', 'desc'], type=str, help='Sort the report by the given column.')
    parser.add_argument('-d', '--driver', type=str, help='Driver to use for the report.')
    parser.add_argument('-p', '--path', required=True, type=str, help='Path to the data.')
    return parser
