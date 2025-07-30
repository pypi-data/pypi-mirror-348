import os

from datetime import datetime

from report.cli import create_parser


def build_report(folder_path, order='asc', driver=None):
    """
    Builds a report based on the logs in the folder_path.

    Args:
        folder_path (str): The path to the folder containing the logs.
        order (str, optional): The order of the report. Defaults to 'asc'.
        driver (str, optional): The driver to include in the report. Defaults to None.

    Returns:
        list: A list of tuples containing the racer's name, team, and time.

    Raises:
        TypeError: If the time for a racer is empty.
        ValueError: If the driver is not found in the logs.
    """

    path_start = os.path.join(folder_path, 'start.log')
    path_end = os.path.join(folder_path, 'end.log')
    path_abb = os.path.join(folder_path, 'abbreviations.txt')

    with open(path_start, 'r') as f:
        read_start = f.readlines()
    with open(path_end, 'r') as f:
        read_end = f.readlines()
    with open(path_abb, 'r') as f:
        read_abb = f.readlines()

    racers_list = {}

    for line in read_abb:
        clean_line = line.strip()
        parts = clean_line.split('_')
        abbreviations = parts[0]
        full_name = parts[1]
        team_name = parts[2]

        racers_list[abbreviations] = {
            'name': full_name,
            'team': team_name
        }

    for line in read_start:
        abbr_str, time_str = line[:3], line[3:].strip()
        if time_str:
            start_time = datetime.strptime(time_str, '%Y-%m-%d_%H:%M:%S.%f')
            racers_list[abbr_str]['start_time'] = start_time
        else:
            raise TypeError(f'The empty time for {abbr_str}')

    for line in read_end:
        abbr_str, time_str = line[:3], line[3:].strip()
        if time_str:
            end_time = datetime.strptime(time_str, '%Y-%m-%d_%H:%M:%S.%f')
            start_time = racers_list[abbr_str]['start_time']
            if not start_time:
                print(f'The start time for {abbr_str} is missing.')
                continue
            if start_time > end_time:
                print(f'The start time for {abbr_str} is later than the end time.')
                continue
            best_time = (end_time - start_time).total_seconds()
            racers_list[abbr_str]['best_time'] = best_time
        else:
            raise TypeError(f'The empty time for {abbr_str}')

    result = []
    for abbr, data in racers_list.items():
        if 'best_time' not in data:
            continue
        if driver is None or driver == data['name']:
            result.append((data['name'], data['team'], data['best_time']))
    reverse = order == 'desc'
    result.sort(key=lambda x: x[2], reverse=(order == 'desc'))

    if driver is not None and not result:
        raise ValueError(f'Driver {driver} not found in the logs.')

    return result

def print_report(folder_path, order='asc'):
    """
    Prints a report based on the logs in the folder_path.
    """
    report = build_report(folder_path, order)
    top_15 = report[:15]
    the_rest = report[15:]
    i = 1
    for name, team, time in top_15:
        minutes = time // 60
        seconds = time % 60
        print(f'{i:>2}. {name:<20} | {team:<30} | {minutes}:{seconds:06.3f}')
        i += 1
    print('-' * 70)
    i = 16
    for name, team, time in the_rest:
        minutes = time // 60
        seconds = time % 60
        print(f'{i:>2}. {name:<20} | {team:<30} | {minutes}:{seconds:06.3f}')
        i += 1

def main():
    parser = create_parser()
    args = parser.parse_args()

    print_report(folder_path=args.path, order=args.order)

if __name__ == '__main__':
    main()
