   _     _____                    _           _   
  /_\    \_   \   _ __  _ __ ___ (_) ___  ___| |_ 
 //_\\    / /\/  | '_ \| '__/ _ \| |/ _ \/ __| __|
/  _  \/\/ /_    | |_) | | | (_) | |  __/ (__| |_ 
\_/ \_/\____/    | .__/|_|  \___// |\___|\___|\__|
                 |_|            |__/               

Made by:
	Simão Marto	75326	
	Eric Loewenthal	75848

To run an uninformed search, write in the command line:
	python3 Uninformed_Search.py <input_file_path> <Goal_Cask>

To run an informed search, write in the command line:
	python3 Informed_Search.py <input_file_path> <Goal_Cask>
This is equivalent to running the "Infinite Stacks Heuristic", like so:
	python3 Infinite_Stacks_Heuristic.py <input_file_path> <Goal_Cask>

Note: Informed_Search.py assumes Python 2/3 coexistence. For Python 3-only systems, Informed_Search.py
	may be altered accordingly by commenting one statement and uncommenting the other.

Two other heuristics were implemented:
	To run the "Ghost Robot Heuristic", run:
		python3 Infinite_Stacks_Heuristic.py <input_file_path> <Goal_Cask>
	To run the "Teleporting Robot Heuristic", run:
		python3 Teleporting_Robot_Heuristic.py <input_file_path> <Goal_Cask>

