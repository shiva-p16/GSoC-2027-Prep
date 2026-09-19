## Log File Summarizer
- Summarizes a given log (.log or .txt) file with this format -  [LEVEL] "<text goes here>" dd-mm-yyyy hh:mm:ss. Gives the amount of WARNINGS, ERRORS or INFOs that a log file has. 
- Also checks for various errors like empty file, malformed lines, wrong file format. 

# Running 
- Run `python3 logsummary.py -f input.log`. Use `python3` or `python` based on which version you have. 
- `python3 logsummary.py -h` for help, and can use either `-f` or `--filename` as flag before your input file. 
- Run `python3 test_logsummary.py` in the same directory, has 11 testcases for validity of main program. 