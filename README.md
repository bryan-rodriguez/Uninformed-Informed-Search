# Uninformed-Informed-Search

if a heuristic file is provided then the program will perform an informed search. the heuristic file gives the estimate of what the cost could be to get to the given destination from any start state

Programming language: Python 3.9, tested on a linux-based OS running Python 3.8.5, and Windows 10 running Python 3.9.2

(Linux)
in terminal on a linux based OS where find_route.py and input_filename are in the same directory, run

python3 find_route.py input_filename origin_city destination_city
python3 find_route.py input_filename origin_city destination_city heuristic_filename

(Windows 10)
in command prompt on Windows 10 where find_route.py and input_filename are in the same directory, run

python find_route.py input_filename origin_city destination_city
python find_route.py input_filename origin_city destination_city heuristic_filename
