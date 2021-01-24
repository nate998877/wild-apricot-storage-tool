from dotenv import load_dotenv, main
import json
load_dotenv()
from api import Apricot


def get_current_storage(filename='storage.json'):
    with open(filename, 'r') as infile:
        return json.load(infile)

def save_storage(data, filename='storage.json'):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def calc_used_storage(data):
    unit_state = {
        "taken": {},
        "invalid": [],
    }

    for member in data:
        unit = member["storage_location"]

        if unit:
            try:
                [row, col, pos] = unit.split('-')
                unit = unit.split('-')
                unit_state['taken'][member["id"]] = unit

            except:
                unit_state['invalid'].append(member['id'])

    return unit_state


def calc_storage(data):
    unit_state = calc_used_storage(data)
    units = []
    row_range = range(1, 5)
    col_range = range(1, 11)
    pos_range = range(1, 4)
    for row in row_range:
        for col in col_range:
            for pos in pos_range:
                units.append([row,col,pos])

    for _, unit in unit_state["taken"].items():
        unit = [int(unit[0]), int(unit[1]), int(unit[2])]
        units.remove(unit)

    return units



# 1,3,m
# 3,1,m
# 1,1,m

def assign_storage(open_units):
    data = get_current_storage()
    for i, member in enumerate(data):
        if not member["storage_location"]:
            member["storage_location"] = open_units[i]
    return data

def main():
    if False:
        apricot = Apricot()
        data = apricot.get_user_list()
        data = apricot.filter_user_data(data)
        save_storage(data)
    data = get_current_storage()
    units = calc_storage(data)
    new_data = assign_storage(units)
    save_storage(new_data, 'new_data.json')


if __name__ == '__main__':
    main()