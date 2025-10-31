# Flight Scheduler

`min_heap.py` contains the min heap implementation. `pairing_heap.py` contains the max pairing heap implementation. `scheduler.py` contains the operators, while `command_parser.py` parses the commands from the text file.

An example run is shown below:
```$ python3 command_parser.py input1.txt
2 runways are now available
Flight 401 scheduled - ETA: 4
Flight 402 scheduled - ETA: 5
Flight 403 scheduled - ETA: 7
Flight 404 scheduled - ETA: 9
[403]
[404]
Priority of Flight 404 has been updated to 10
Updated ETAs: [403: 8, 404: 8]
Additional 1 runways are now available
Updated ETAs: [403: 7, 404: 5]
Flight 405 scheduled - ETA: 7
Flight 406 scheduled - ETA: 9
Updated ETAs: [403: 8]
Flights of the airlines in the range [16,16] have been grounded
Updated ETAs: [403: 7]
Flight 405 has been canceled.
Flight 401 has landed at time 4
Flight 407 scheduled - ETA: 8
Priority of Flight 407 has been updated to 9
Flight 408 scheduled - ETA: 7
Flight 402 has landed at time 5
Flight 404 has landed at time 5
Additional 1 runways are now available
[flight403, airline13, runway1, start4, ETA7]
[flight407, airline17, runway2, start5, ETA8]
[flight408, airline18, runway3, start5, ETA7]
Flight 403 has landed at time 7
Flight 408 has landed at time 7
Flight 407 has landed at time 8
There are no flights in that time period
Program Terminated!!```