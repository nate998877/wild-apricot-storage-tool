from dotenv import load_dotenv, main
import json
load_dotenv()
from api import Apricot

# Don't pull live data while developing
dev = True

# BE WARNED! I'm lazy

def get_current_storage(filename='new_data.json'):
    with open(filename, 'r') as infile:
        return json.load(infile)

def save_storage(data, filename='new_data.json'):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def save_parsed_storage(data, filename='new_data.json'):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def get_parsed_storage(data, filename='output.json'):
    with open(filename, 'r') as infile:
        json.dump(data, infile)

def get_full_member_data(filename='storage.json')
    with open(filename, 'r') as infile:
        return json.load(infile)

def calc_used_storage(data):
    unit_state = {
        "taken": {}, # member id and unit taken
        "invalid": [], #Doesn't really matter what the current data is if invalid, so only keep id of invalid users
    }

    for member in data:
        unit = member["storage_location"]

        if unit:
            try:
                # relying on non-stupidity for manually assigned units...

                # try to split by '-' to see if valid format => x-x-x this is a naive approach. --- would be valid even if it's wrong.
                [row, col, box] = unit.split('-')
                unit = unit.split('-') # have to split first to validate
                unit_state['taken'][member["id"]] = {
                    'unit': '-'.join(unit),
                    'id': member["id"]
                }

            except:
                unit_state["invalid"].append(member['id'])

    return unit_state


def calc_storage(data):
    unit_state = calc_used_storage(data)
    units = []
    row_range = range(1, 3) # first two rows
    col_range = range(1, 5) # 4 columns total
    box_range = range(1, 4) # 3 slots per column
    # generate all possible slots
    # inefficient, but small enough I'm not going to be smarter about it.
    for row in row_range:
        for col in col_range:
            for box in box_range:
                units.append(f"{row}-{col}-{box}")

    for _, unit in unit_state["taken"].items():
        unit = unit["unit"]
        try:
            units.remove(unit)
        except:
            unit_state["invalid"].append(_)

    return (units, unit_state)


def assign_storage(data, open_units, unit_state):
    for invalid in unit_state["invalid"]:
        print(invalid)
    for i, member in enumerate(data):
        if not member["storage_location"] or member["id"] in unit_state["invalid"]:
            member["storage_location"] = open_units[i]

    return data

def main():
    if not dev:
        apricot = Apricot()
        data = apricot.get_user_list()
        data = apricot.filter_user_data(data)
        save_storage(data)
    data = get_current_storage()
    [units, unit_state] = calc_storage(data)
    new_data = assign_storage(data, units, unit_state)
    save_storage([new_data, unit_state], 'new_data.json')
    # if not dev:
    #     apricot = Apricot()
    #     apricot.upload_users_storage(new_data)


if __name__ == '__main__':
    main()