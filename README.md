# FileScans
Simulation of file scanning

# Dependecies
The following are mandatory for operating the services:
1. flask (Flask) - for enabling api calls to the services (must be installed)
2. Pickle (dump, load) - for dumping and loading the current state of each service is case of a crash (must be installed)
3. threading (Thread) - allowing to run multiple tasks simultaneously 
4. requests (post) - the services are using this to communicate between them
5. os.path (isfile) - for checking memory dump availabilty
6. socket - checking the services availability 

# Executing the services
To start the program:
1. Execute i_main.py: Starting the Ingest service (In charge of getting new scan requests)
2. Execute p_main.py: Starting the Process service (In charge of managing scans)
4. Execute s_main.py: Starting the Status\Data service (In charge of keeping track of the scans' status)

# Using the services
execute the following (replace [] with data):
1. http://127.0.0.1:8080/addscan/[scan_name] - to add a new scan to the PROCESS queue (will return the id of the scan)
2. http://127.0.0.1:3306/status/[scan_id] - will return the status of the scan (Accepted, Running, Error. Completed, Not-Found)
3. http://127.0.0.1:3306/status - will return the status of all the scans in json format (with the additional info of: id, name, timestamp)
