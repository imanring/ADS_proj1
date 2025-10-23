from min_heap import MinHeap
from max_pairing_heap import PairingHeap

class Flight:
    def __init__(self, flightID, airlineID, submitTime, priority, duration):
        self.flightID = flightID
        self.airlineID = airlineID
        self.submitTime = submitTime
        self.priority = priority
        self.duration = duration
        self.statue = "PENDING" # PENDING, SCHEDULED, COMPLETED
        self.startTime = -1 
        self.ETA = -1


class Scheduler:
    def __init__(self, n):
        self.pending_flights = None # PairingHeap
        self.runway_pool = MinHeap()
        self.active_flights = {} # flightID: Flight
        self.time_table = MinHeap() # ((eta, flightID), (runwayID))
        self.airline_index = {}#airlineID: [flightID]
        self.handles = {}#flightID: PairingHeap
        
        if n <= 0:
            print("Invalid input. Please provide a valid number of runways.")
        else:
            for i in range(1,n+1):
                self.runway_pool.insert((0,i), (i,0))
            self.currentTime = 0
            self.numRunways = n
            print(f"{n} runways are now available")

    def settle(self):
        while self.time_table.get_min()[0][0] >= self.currentTime:
            key, payload = self.time_table.pop_min()
            self.active_flights[key[1]].state = "COMPLETED"
            # possibly remove from other data structures
            self.active_flights[key[1]] = None
            print(f"Flight {key[1]} has complete at time {self.currentTime}")
        # promotion of pending flights to active flights if possible

    

    def reschedule(self):
        # pop all flights from pending and push into new pending heap
        new_pending = None
        # create new next available runway heap based on old one.
        new_runway_pool = self.runway_pool.copy()
        # schedule all pending flights
        while self.pending_flights is not None:
            # get next available runway
            runwayID, nextFreeTime = self.new_runway_pool.pop_min()
            # get highest priority flight
            key, flight = self.pending_flights.pop_max()

            start_time = self.currentTime if self.currentTime > nextFreeTime else nextFreeTime
            eta = start_time + flight.duration
            flight.ETA = eta
            flight.state = "SCHEDULED"
            flight.startTime = start_time
            print(f"Flight {flight.flightID} scheduled on Runway {runwayID} - ETA: {eta}")
            # update data structures
            self.time_table.insert((eta, flight.flightID), runwayID)
            self.new_runway_pool.insert((eta, runwayID), (runwayID, eta))
            self.active_flights[flight.flightID] = flight
            # add to new pending heap with updated key
            new_fligt = PairingHeap(key, flight)
            if new_pending is None:
                new_pending = new_fligt
            else:
                new_pending = new_pending.meld(new_fligt)
            self.handles[flight.flightID] = new_fligt
        self.pending_flights = new_pending

    
    def submitFlight(self, flightID, airlineID, submitTime, priority, duration):
        # TODO: settle
        # TODO: reschedule
        self.currentTime = submitTime
        if flightID in self.handles:
            print("Duplicate flight")
        else:
            # new flight
            f = Flight(flightID, airlineID, submitTime, priority, duration)
            new_flight = PairingHeap((priority, -submitTime, -flightID), f)
            self.handles[flightID] = new_flight
            if self.pending_flights is not None:
                self.pending_flights.meld(new_flight)
            else:
                self.pending_flights = new_flight
            # TODO: reschedule
            print(f"Flight {flightID} scheduled - ETA: {self.handles[flightID].payload[5]}")
            # TODO: print updated ETAs

    
    def cancelFlight(self, flightID, currentTime):
        # TODO: settle, reschedule
        self.currentTime = currentTime
        if flightID not in self.handles:
            print("Flight does not exist.")
        elif flightID in self.active_flights:
            print(f"Cannot cancel: Flight {flightID} has already departed.")
        else:
            self.pending_flights.remove(self.handles[flightID])
            # shouldn't be in active_flights
            self.time_table.arbitrary_remove((self.handles[flightID].payload.eta, flightID))
            # TODO: inefficient method of removing from airline_index
            self.airline_index[self.handles[flightID].payload.airlineID] = [c for c in self.airline_index[self.handles[flightID].payload.airlineID] if c != self.handles[flightID].payload.flightID]
            self.handles[flightID] = None
            
            # TODO: reschedule
            print(f"Flight {flightID} has been canceled.")

            # TODO: print updated ETAs


    def reprioritize(self, flightID, currentTime, newPriority):
        # TODO: settle, reschedule
        self.currentTime = currentTime
        if flightID not in self.handles:
            print("Flight does not exist.")
        elif flightID in self.active_flights:
            print(f"Cannot reprioritize: Flight {flightID} has already departed.")
        else:
            # TODO: what if newPriority < oldPriority
            self.pending_flights.increase_key(self.handles[flightID], newPriority)
            # TODO: reschedule
            print(f"Priority of Flight {flightID} has been updated to {newPriority}")
            # TODO: print updated ETAs


    def addRunways(self, count, currentTime):
        # TODO: settle, reschedule
        self.currentTime = currentTime
        if count <= 0:
            print("Invalid input. Please provide a valid number of runways.")
        else:
            for i in range(self.numRunways + 1,self.numRunways + 1 + count):
                self.runway_pool.insert((currentTime,i), (i,currentTime))
            # TODO: reschedule
            print(f"Additional {count} runways are now available")
            # TODO: print updated ETAs

    def groundHold(self, airlineLow, airlineHigh, currentTime):
        # TODO: settle, reschedule
        self.currentTime = currentTime
        if airlineHigh < airlineLow:
            print("Invalid input. Please provide a valid airline range.")
        else:
            # TODO: remove flights from data structures
            # TODO: reschedule
            print(f"GroundHold applied to airlines[{airlineLow},{airlineHigh}].")
            # TODO: print updated ETAs


    def printActive(self):
        i = 0
        for key in sorted(self.active_flights.keys()):
            print(self.active_flights[key])
            i = 1
        if i == 0:
            print("No active flights")

    def printSchedule(self, t1, t2):
        flights = [f for f in self.active_flights.values() if f.state == "SCHEDULED" and f.startTime < self.currentTime and t1 <= f.ETA and t2 >= f.ETA]
        for f in sorted(flights, key=lambda f: (f.ETA, f.flightID)):
            print(f"[{f.fligtID}]")
        if len(flights) == 0:
            print("There are no flights in that time period")


    def tick(self, t):
        self.currentTime = t
        # TODO: settle, reschedule
        # TODO: print updated ETAs

    def parseCommand(self, command):
        cmd = command.split()
        if cmd[0] == "submitFlight":
            self.submitFlight(int(cmd[1]), int(cmd[2]), int(cmd[3]), int(cmd[4]), int(cmd[5]))
        elif cmd[0] == "cancelFlight":
            self.cancelFlight(int(cmd[1]), int(cmd[2]))
        elif cmd[0] == "reprioritize":
            self.reprioritize(int(cmd[1]), int(cmd[2]), int(cmd[3]))
        elif cmd[0] == "addRunways":
            self.addRunways(int(cmd[1]), int(cmd[2]))
        elif cmd[0] == "groundHold":
            self.groundHold(int(cmd[1]), int(cmd[2]), int(cmd[3]))
        elif cmd[0] == "printActive":
            self.printActive()
        elif cmd[0] == "printSchedule":
            self.printSchedule(int(cmd[1]), int(cmd[2]))
        elif cmd[0] == "tick":
            self.tick(int(cmd[1]))
        else:
            print("Invalid command")


if __name__ == "__main__":
    scheduler = Scheduler(3)
    commands = [
        "submitFlight 101 1 0 5 30",
        "submitFlight 102 2 1 3 20",
        "submitFlight 103 1 2 4 25",
        "printActive",
        "tick 10",
        "reprioritize 102 10 6",
        "cancelFlight 103 15",
        "addRunways 2 20",
        "groundHold 1 2 25",
        "printSchedule 0 50",
        "tick 30"
    ]
    for command in commands:
        print(f"Command: {command}")
        scheduler.parseCommand(command)
        print()