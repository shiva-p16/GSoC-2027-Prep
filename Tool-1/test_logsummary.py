import subprocess
import sys
import re
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
SCRIPT_PATH = BASE_DIR / "logsummary.py"
TESTCASES_DIR = BASE_DIR / "testcases"

# Test definitions with expected behavior based on the log specification:
# Format: [LEVEL] "<text goes here>" dd-mm-yyyy hh:mm:ss
TESTCASES = [
    {
        "name": "test_valid.log",
        "expected_exit_code": 0,
        "expected_summary": "Found 1 ERRORS, 1 WARNINGS, 2 INFOS",
        "expected_malformed_lines": [],
    },
    {
        "name": "test_empty.txt",
        "expected_exit_code": 0,
        "expected_summary": "Error : Empty file.",
        "expected_malformed_lines": [],
    },
    {
        "name": "test_wrong_file_format.csv",
        "expected_exit_code": 1,
        "expected_summary": "Error : Unexpected file type - need .log or .txt",
        "expected_malformed_lines": [],
    },
    {
        "name": "test_mixed_levels.txt",
        "expected_exit_code": 0,
        "expected_summary": "Found 2 ERRORS, 1 WARNINGS, 0 INFOS",
        "expected_malformed_lines": [],
    },
    {
        "name": "test_whitespace_leading.log",
        "expected_exit_code": 0,
        "expected_summary": "Found 0 ERRORS, 1 WARNINGS, 0 INFOS",
        "expected_malformed_lines": [2, 3],
    },
    {
        "name": "test_malformed.log",
        "expected_exit_code": 0,
        "expected_summary": "Found 0 ERRORS, 0 WARNINGS, 1 INFOS",
        "expected_malformed_lines": [2, 3, 4, 5],
    },
    {
        "name": "test_timestamp_formats.log",
        "expected_exit_code": 0,
        "expected_summary": "Found 2 ERRORS, 1 WARNINGS, 2 INFOS",
        "expected_malformed_lines": [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
    },
    {
        "name": "test_quote_and_message_edge_cases.log",
        "expected_exit_code": 0,
        "expected_summary": "Found 4 ERRORS, 3 WARNINGS, 3 INFOS",
        "expected_malformed_lines": [4, 5, 6, 7, 8, 9, 10, 11, 13],
    },
    {
        "name": "test_level_variants_and_typos.log",
        "expected_exit_code": 0,
        "expected_summary": "Found 1 ERRORS, 1 WARNINGS, 2 INFOS",
        "expected_malformed_lines": list(range(4, 39)),
    },
    {
        "name": "test_spacing_delimiters_and_structure.log",
        "expected_exit_code": 0,
        "expected_summary": "Found 2 ERRORS, 3 WARNINGS, 3 INFOS",
        "expected_malformed_lines": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
    },
    {
        "name": "test_boundary_unicode_and_stress.txt",
        "expected_exit_code": 0,
        "expected_summary": "Found 7 ERRORS, 6 WARNINGS, 10 INFOS",
        "expected_malformed_lines": [],
    },
]


def run_testcase(test_case):
    test_file = TESTCASES_DIR / test_case["name"]
    if not test_file.exists():
        return False

    proc = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "-f", str(test_file)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if proc.returncode != test_case["expected_exit_code"]:
        return False

    combined_output = (proc.stdout + "\n" + proc.stderr).strip()

    if test_case["expected_summary"] not in combined_output:
        return False

    reported_malformed_lines = set()
    for line in combined_output.splitlines():
        match = re.search(r"Error - Line (\d+) :", line)
        if match:
            reported_malformed_lines.add(int(match.group(1)))

    expected_lines = set(test_case["expected_malformed_lines"])
    if reported_malformed_lines != expected_lines:
        return False

    return True


def main():
    passed_count = 0
    total_count = len(TESTCASES)
    failed_testcases = []

    for test_case in TESTCASES:
        name = test_case["name"]
        passed = run_testcase(test_case)

        if passed:
            passed_count += 1
            print(f"{name}: PASS")
        else:
            failed_testcases.append(name)
            print(f"{name}: FAIL")

    print("\n" + "=" * 40)
    print(f"Total passed: {passed_count} / {total_count}")

    if failed_testcases:
        print("\nTestcases that did not pass:")
        for failed_name in failed_testcases:
            print(f"  - {failed_name}")
    print("=" * 40)


if __name__ == "__main__":
    main()
