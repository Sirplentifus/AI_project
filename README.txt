# AI_project

Made by:
	Simão Marto	75326	
	Eric Loewenthal	75848

To run an uninformed search, write in the command line:
	python3 Uninformed_Search.py <input_file_path> <Goal_Cask>

To run an informed search, write in the command line:
	python3 Informed_Search.py <input_file_path> <Goal_Cask>
This is equivalent to doing, which runs the "Infinite Stacks Heuristic":
	python3 Infinite_Stacks_Heuristic.py <input_file_path> <Goal_Cask>

Two other heuristics were implemented:
	To run the "Ghost Robot Heuristic", run:
		python3 Infinite_Stacks_Heuristic.py <input_file_path> <Goal_Cask>
	To run the "Teleporting Robot Heuristic", run:
		python3 Teleporting_Robot_Heuristic.py <input_file_path> <Goal_Cask>