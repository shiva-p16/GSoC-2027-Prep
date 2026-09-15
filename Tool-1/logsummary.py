# Log File Summarizer - Parses a log file, counts error types, prints a summary. Core skills: file I/O, regex, argparse.
#Parses a log file, counts error types, prints a summary. Core skills: file I/O, regex, argparse.

# Takes input log/text file, counts error types(malformed line, empty file), prints that. 

# show errors while its happening. 

import re # for regex.
import argparse # for input of log files.

def checkFile(file) : 
    log = file.endswith((".log",".txt")) 
    return(log)


parser = argparse.ArgumentParser()
parser.add_argument('-f','--filename', type=str, help='log file for summary')

args = parser.parse_args()
while (checkFile(args.filename) == False) : 
    print("Error : Unexpected file type - need .log or .txt")

def main() :   
    pattern = r"(?:WARNING|ERROR|INFO)\s+\"[^\"]*\"\s+\d{2}-\d{2}-\d{4}\s+\d{2}:\d{2}:\d{2}"
    try : 
        with open(args.filename, "r", encoding="utf-8") as file : 
            for line_number, line in enumerate(file, start=1):
                clean_line = line.rstrip("\r\n")
                if not re.search(pattern, clean_line) : 
                    print(f"Error - Line {line_number} : {clean_line} - Does not follow log format")
            file.seek(0)
            content = file.read()
        err = 0
        info = 0
        warn = 0

        if not content : 
            print("Error : empty file.")
            return 0
        
        for line_number, line in enumerate(content.splitlines(),start=1):
            if line.lstrip().startswith("WARNING") : 
                warn = warn + 1
            elif line.lstrip().startswith("ERROR") : 
                err = err + 1
            elif line.lstrip().startswith("INFO") : 
                info = info + 1

        print(f"Found {err} ERRORS, {warn} WARNINGS, {info} INFOS")
               
    except FileNotFoundError as e:
        print("Error:", e)
        

if __name__ == "__main__":
    main()