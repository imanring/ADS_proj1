from min_heap import MinHeap
from pairing_heap import PairingHeap
import copy

class Flight:
    def __init__(self, flightID, airlineID, submitTime, priority, duration):
        self.flightID = flightID
        self.airlineID = airlineID
        self.submitTime = submitTime
        self.priority = priority
        self.duration = duration
        self.state = "PENDING" # PENDING, SCHEDULED, INPROGRESS, COMPLETED
        self.startTime = -1 
        self.ETA = -1
        self.runwayID = -1


class Scheduler:
    def __init__(self, n):
        # Pending and scheduled flights
        self.pending_flights = None # PairingHeap
        self.runway_pool = MinHeap()
        # only flights in progress
        self.active_flights = {} # flightID: Flight
        self.time_table = MinHeap() # ((eta, flightID), (runwayID))
        self.airline_index = {}#airlineID: [flightID]
        self.handles = {}#flightID: (PairingHeap, MinHeapNode)
        
        if n <= 0:
            print("Invalid input. Please provide a valid number of runways.")
        else:
            for i in range(1,n+1):
                self.runway_pool.insert((0,i), (i,0))
            self.currentTime = 0
            self.numRunways = n
            print(f"{n} runways are now available")

    def settle(self):
        while self.time_table.get_min().key[0] <= self.currentTime:
            node = self.time_table.pop_min()
            if node.key[1] in self.active_flights:
                self.active_flights[node.key[1]].state = "COMPLETED"
            # possibly remove from other data structures
            self.active_flights[node.key[1]] = None
            print(f"Flight {node.key[1]} has complete at time {self.currentTime}")
        # promotion of pending flights to active flights if possible
        while self.pending_flights is not None and self.pending_flights.payload.startTime <= self.currentTime:
            # can no longer be rescheduled
            rslt, self.pending_flights = self.pending_flights.pop_max()
            rslt[1].state = "INPROGRESS"
            self.active_flights[rslt[1].flightID] = rslt[1]
        new_runway_pool = MinHeap()
        runwayIDs = set(range(1, self.numRunways + 1))
        for key, value in self.active_flights.items():  # new runway heap
            new_runway_pool.insert((value.startTime + value.duration, value.runwayID), (value.runwayID, value.startTime + value.duration))
            runwayIDs.remove(value.runwayID)
        for rid in runwayIDs:
            new_runway_pool.insert((self.currentTime, rid), (rid, self.currentTime))
        return new_runway_pool

            
    def reschedule(self, new_runway_pool, restart_changes=True, exclude=[]):
        # pop all flights from pending and push into new pending heap
        new_pending = None
        self.runway_pool = copy.deepcopy(new_runway_pool)
        if restart_changes:
            self.updated_flights = {}
        # schedule all pending flights
        while self.pending_flights is not None:
            # get next available runway
            mhn = self.runway_pool.pop_min()
            runwayID, nextFreeTime = mhn.payload
            # get highest priority flight
            flight, self.pending_flights = self.pending_flights.pop_max()

            start_time = self.currentTime if self.currentTime > nextFreeTime else nextFreeTime
            eta = start_time + flight[1].duration
            #print(start_time, eta)
            if eta != flight[1].ETA and flight[1].flightID not in exclude:
                self.updated_flights[flight[1].flightID] = eta
            flight[1].ETA = eta
            old_state = flight[1].state
            flight[1].state = "SCHEDULED"
            flight[1].startTime = start_time
            flight[1].runwayID = runwayID
            #print(f"Flight {flight[1].flightID} scheduled on Runway {runwayID} - ETA: {eta}")

            # update data structures
            if old_state == "PENDING":
                node = self.time_table.insert((eta, flight[1].flightID), runwayID)
            else:
                node = self.handles[flight[1].flightID][1]
                self.time_table.change_key(node.idx, (eta, flight[1].flightID))
            # update runway pool with new next free time
            self.runway_pool.insert((eta, runwayID), (runwayID, eta))
            # add to new pending heap with updated key
            new_flight = PairingHeap(flight[0], flight[1])
            if new_pending is None:
                new_pending = new_flight
            else:
                new_pending = new_pending.meld(new_flight)
            self.handles[flight[1].flightID] = (new_flight, node)
        self.pending_flights = new_pending

    def print_updated_etas(self):
        l = [f"{k}: {v}" for k,v in sorted(self.updated_flights.items())]
        if len(l) > 0:
            print(f"Updated ETAs: [{", ".join(l)}]")
    
    def submitFlight(self, flightID, airlineID, submitTime, priority, duration):
        # settle
        # reschedule
        self.currentTime = submitTime
        rt = self.settle()
        self.reschedule(rt)

        if flightID in self.handles:
            print("Duplicate flight")
        else:
            # new flight
            f = Flight(flightID, airlineID, submitTime, priority, duration)
            new_flight = PairingHeap((priority, -submitTime, -flightID), f)
            
            if airlineID in self.airline_index:
                self.airline_index[airlineID].append(flightID)
            else:
                self.airline_index[airlineID] = [flightID]
            self.handles[flightID] = (new_flight, None)
            if self.pending_flights is not None:
                self.pending_flights = self.pending_flights.meld(new_flight)
            else:
                self.pending_flights = new_flight
            # reschedule
            self.reschedule(rt, restart_changes=False, exclude=[flightID])
            print(f"Flight {flightID} scheduled - ETA: {self.handles[flightID][0].payload.ETA}")
            # print updated ETAs
            self.print_updated_etas()

    
    def cancelFlight(self, flightID, currentTime):
        # settle, reschedule
        self.currentTime = currentTime
        rt = self.settle()
        self.reschedule(rt)
        
        if flightID not in self.handles:
            print("Flight does not exist.")
        elif flightID in self.active_flights:
            print(f"Cannot cancel: Flight {flightID} has already departed.")
        else:
            self.pending_flights = self.pending_flights.arbitrary_delete(self.handles[flightID][0])
            # shouldn't be in active_flights
            self.time_table.arbitrary_delete(self.handles[flightID][1].idx)
            # TODO: inefficient method of removing from airline_index
            self.airline_index[self.handles[flightID][0].payload.airlineID] = [c for c in self.airline_index[self.handles[flightID][0].payload.airlineID] if c != self.handles[flightID][0].payload.flightID]
            self.handles[flightID] = None

            # reschedule
            self.reschedule(rt, restart_changes=False)
            print(f"Flight {flightID} has been canceled.")

            # print updated ETAs
            self.print_updated_etas()


    def reprioritize(self, flightID, currentTime, newPriority):
        # settle, reschedule
        self.currentTime = currentTime
        rt = self.settle()
        self.reschedule(rt)

        if flightID not in self.handles:
            print("Flight does not exist.")
        elif flightID in self.active_flights:
            print(f"Cannot reprioritize: Flight {flightID} has already departed.")
        else:
            # TODO: what if newPriority < oldPriority
            oldPriority = self.handles[flightID][0].key[0]
            if newPriority >= oldPriority:
                self.pending_flights = self.pending_flights.increase_key(
                    self.handles[flightID][0],
                    newPriority
                    )
            else:
                self.pending_flights = self.pending_flights.arbitrary_delete(self.handles[flightID][0])
                self.handles[flightID][0].key[0] = newPriority
                self.pending_flights = self.pending_flights.meld(self.handles[flightID][0])
            # reschedule
            self.reschedule(rt, restart_changes=False)
            print(f"Priority of Flight {flightID} has been updated to {newPriority}")
            # print updated ETAs
            self.print_updated_etas()


    def addRunways(self, count, currentTime):
        # settle, reschedule
        self.currentTime = currentTime
        rt = self.settle()
        self.reschedule(rt)

        if count <= 0:
            print("Invalid input. Please provide a valid number of runways.")
        else:
            for i in range(self.numRunways + 1,self.numRunways + 1 + count):
                rt.insert((currentTime,i), (i,currentTime))
            # reschedule
            self.reschedule(rt, restart_changes=False)
            self.numRunways += count
            print(f"Additional {count} runways are now available")
            # print updated ETAs
            self.print_updated_etas()

    def groundHold(self, airlineLow, airlineHigh, currentTime):
        # settle, reschedule
        self.currentTime = currentTime
        rt = self.settle()
        self.reschedule(rt)

        if airlineHigh < airlineLow:
            print("Invalid input. Please provide a valid airline range.")
        else:
            # TODO: remove flights from data structures
            # reschedule
            self.reschedule(rt)
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
        # get all scheduled flights
        flights = self.pending_flights.dfs_list([])
        flights = [f for f in flights if f.state == "SCHEDULED" and f.startTime > self.currentTime and t1 <= f.ETA and t2 >= f.ETA]
        for f in sorted(flights, key=lambda f: (f.ETA, f.flightID)):
            print(f"[{f.flightID}]")
        if len(flights) == 0:
            print("There are no flights in that time period")


    def tick(self, t):
        self.currentTime = t
        # settle, reschedule
        rt = self.settle()
        self.reschedule(rt)
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
    scheduler = Scheduler(2)
    commands = [
        "submitFlight 401 11 0 8 4",
        "submitFlight 402 12 0 7 5",
        "submitFlight 403 13 0 6 3",
        "submitFlight 404 14 0 5 4",
        "printSchedule 3 9",
        "reprioritize 404 1 10",
        "addRunways 1 1",
        "submitFlight 405 15 2 6 2",
        "submitFlight 406 16 3 7 5",
        "groundHold 16 16 3",
        "cancelFlight 405 3",
        "tick 4",
        "submitFlight 407 17 4 6 3"
        "reprioritize 407 4 9"
    ]
    for command in commands:
        #print(f"Command: {command}")
        scheduler.parseCommand(command)
        #print()