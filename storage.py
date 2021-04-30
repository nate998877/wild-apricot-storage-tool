from os import write
from dotenv import load_dotenv, main
import json
load_dotenv()
from api import Apricot

# Don't pull live data while developing
dev = True

# BE WARNED! I'm lazy

def read_file(filename='data.json'):
    with open(filename, 'r') as infile:
        return json.load(infile)

def write_file(data, filename='data.json'):
    with open(filename, 'w') as infile:
        json.dump(data, infile)


def calc_used_storage(data):
    unit_state = {
        "taken": {}, # member id and unit taken
        "invalid": [], #Doesn't really matter what the current data is if invalid, so only keep id of invalid users
    }

    for member in data:
        member_data = data[member]["data"]
        unit = member_data["storage_location"]

        if unit:
            try:
                # relying on non-stupidity for manually assigned units...

                # try to split by '-' to see if valid format => x-x-x this is a naive approach. --- would be valid even if it's wrong.
                [row, col, box] = unit.split('-') #test format

                unit_state['taken'][member_data['Id']] = {
                    'unit': '-'.join([row, col, box]),
                    'id': member_data['Id']
                }

            except:
                unit_state["invalid"].append(data[member]['Id'])

    return unit_state


def calc_storage(data):
    unit_state = calc_used_storage(data)
    units = []
    row_range = range(1, 3) # first two rows
    col_range = range(1, 5) # 4 columns per row
    box_range = range(1, 4) # 3 slots per column
    # generate all possible slots
    # inefficient, but small enough I'm not going to be smarter about it.
    for row in row_range:
        for col in col_range:
            for box in box_range:
                units.append(f"{row}-{col}-{box}")
    print("all possible units: ", units)
    for _id, unit in unit_state["taken"].items():
        unit = unit["unit"]
        try:
            units.remove(unit)
        except:
            #Unit out of range
            unit_state["invalid"].append(_id)

    return (units, unit_state)


def assign_storage(data, open_units, unit_state):
    for invalid in unit_state["invalid"]:
        print(invalid)
    index = 0
    for member in data:
        member_data = data[member]['data']
        if not member_data["storage_location"] or member_data["Id"] in unit_state["invalid"]:
            member_data["storage_location"] = open_units[index]
            index += 1

    return data

def print_simplified(data):
    for member in data:
        print(data[member]['data'])
    print(len(data))


def main():
    if not dev:
        apricot = Apricot()
        data = apricot.get_user_list()
        data = apricot.filter_user_data(data)
        write_file(data)
        only_data = []
        for key in data:
            only_data.append(data[key]["data"])
        write_file(only_data, "data_only.json")

    data = read_file()
    [units, unit_state] = calc_storage(data)
    new_data = assign_storage(data, units, unit_state)
    write_file([new_data, unit_state])
    print_simplified(new_data)
    # if not dev:
    #     apricot = Apricot()
    #     apricot.upload_users_storage(new_data)


if __name__ == '__main__':
    main()