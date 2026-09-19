""" Log File Summarizer - Parses a log file, counts error types, prints a summary. Core skills: file I/O, regex, argparse.
 Parses a log file, counts error types, prints a summary. Core skills: file I/O, regex, argparse.  """

import re # for regex.
import argparse # for input of log files.
import sys # for exiting if wrong file format.
from datetime import datetime # for checking valid date time.

def checkFile(file) : 
    if not file :
        return False
    log = file.endswith((".log",".txt")) 
    return(log)

def valid_date(date_string) : 
    try : 
       datetime.strptime(date_string, "%d-%m-%Y")
       return True 
    except ValueError : 
        return False 


parser = argparse.ArgumentParser()
parser.add_argument('-f','--filename', type=str, help='input log file for summary')

args = parser.parse_args()
if checkFile(args.filename) == False : 
    print("Error : Unexpected file type - need .log or .txt")
    sys.exit(1)
    
    

def main() :   
    # malformed_lines = []
    pattern = r"(?:WARNING|ERROR|INFO)\s+\"[^\"]*\"\s+(\d{2}-\d{2}-\d{4})\s+(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$"
    err = 0
    info = 0
    warn = 0
    try : 
        with open(args.filename, "r", encoding="utf-8") as file : 
            line_number = 0
            for line_number, line in enumerate(file, start=1): 
                clean_line = line.rstrip("\r\n")

                match = re.match(pattern, clean_line)

                if not match : 
                    # malformed_lines.append(line_number) save the line_numbers which are malformed, later do not count them in the final reading.
                    print(f"Error - Line {line_number} : {clean_line} - Does not follow log format")
                    continue

                date_string = match.group(1)

                if not valid_date(date_string) :
                    print(
                        f"Error - Line {line_number} : {clean_line} - Invalid date format"
                    )
                    continue

                if line.lstrip().startswith("WARNING") : 
                    warn = warn + 1
                elif line.lstrip().startswith("ERROR") : 
                    err = err + 1
                elif line.lstrip().startswith("INFO") : 
                    info = info + 1

            if line_number == 0 : 
                print("Error : Empty file.")
                return 0
    

        #     file.seek(0)
        #     content = file.read()


        # if not content : 
        #     print("Error : empty file.")
        #     return 0
        
        # # k = 0    pointer traversal method in comments. 
        # for line_number, line in enumerate(content.splitlines(),start=1): # before counting, if its a malformed line, skip it. 
        #     if line_number in malformed_lines : 
        #         continue
        #     # if k < len(malformed_lines) and line_number == malformed_lines[k] :
        #     #     if k < len(malformed_lines) :
        #     #         k = k + 1
        #     #     continue

        #     if line.lstrip().startswith("WARNING") : 
        #         warn = warn + 1
        #     elif line.lstrip().startswith("ERROR") : 
        #         err = err + 1
        #     elif line.lstrip().startswith("INFO") : 
        #         info = info + 1

        print(f"Found {err} ERRORS, {warn} WARNINGS, {info} INFOS")
               
    except FileNotFoundError as e:
        print("Error:", e)
        

if __name__ == "__main__":
    main()