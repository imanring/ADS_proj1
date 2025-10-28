import re
from scheduler import Scheduler

def parse_commands(filename):
    with open(filename, 'r') as f:
        commands = f.readlines()

    # Initialize regex patterns for each command type
    initialize_pattern = re.compile(r'Initialize\((\d+)\)')
    submit_flight_pattern = re.compile(r'SubmitFlight\((\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)')
    print_schedule_pattern = re.compile(r'PrintSchedule\((\d+),\s*(\d+)\)')
    reprioritize_pattern = re.compile(r'Reprioritize\((\d+),\s*(\d+),\s*(\d+)\)')
    add_runways_pattern = re.compile(r'AddRunways\((\d+),\s*(\d+)\)')
    ground_hold_pattern = re.compile(r'GroundHold\((\d+),\s*(\d+),\s*(\d+)\)')
    cancel_flight_pattern = re.compile(r'CancelFlight\((\d+),\s*(\d+)\)')
    tick_pattern = re.compile(r'Tick\((\d+)\)')
    print_active_pattern = re.compile(r'PrintActive\(\)')
    quit_pattern = re.compile(r'Quit\(\)')

    scheduler = None

    for command in commands:
        command = command.strip()
        #print(command)
        # Initialize
        if match := initialize_pattern.match(command):
            n_runways = int(match.group(1))
            scheduler = Scheduler(n_runways)
            continue

        if scheduler is None:
            print("Error: Scheduler not initialized")
            break

        # SubmitFlight
        if match := submit_flight_pattern.match(command):
            flight_id, airline_id, submit_time, priority, duration = map(int, match.groups())
            scheduler.submitFlight(flight_id, airline_id, submit_time, priority, duration)
            continue

        # PrintSchedule
        if match := print_schedule_pattern.match(command):
            t1, t2 = map(int, match.groups())
            scheduler.printSchedule(t1, t2)
            continue

        # Reprioritize
        if match := reprioritize_pattern.match(command):
            flight_id, current_time, new_priority = map(int, match.groups())
            scheduler.reprioritize(flight_id, current_time, new_priority)
            continue

        # AddRunways
        if match := add_runways_pattern.match(command):
            count, current_time = map(int, match.groups())
            scheduler.addRunways(count, current_time)
            continue

        # GroundHold
        if match := ground_hold_pattern.match(command):
            airline_low, airline_high, current_time = map(int, match.groups())
            scheduler.groundHold(airline_low, airline_high, current_time)
            continue

        # CancelFlight
        if match := cancel_flight_pattern.match(command):
            flight_id, current_time = map(int, match.groups())
            scheduler.cancelFlight(flight_id, current_time)
            continue

        # Tick
        if match := tick_pattern.match(command):
            time = int(match.group(1))
            scheduler.tick(time)
            continue

        # PrintActive
        if print_active_pattern.match(command):
            scheduler.printActive()
            continue

        # Quit
        if quit_pattern.match(command):
            print("Program Terminated!!")
            break

if __name__ == "__main__":
    parse_commands("input2.txt")