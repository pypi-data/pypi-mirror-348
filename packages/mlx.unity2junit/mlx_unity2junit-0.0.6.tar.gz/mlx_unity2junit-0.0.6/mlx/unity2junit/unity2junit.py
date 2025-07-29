#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import argparse
from datetime import datetime
from importlib.metadata import version
import os
import re
import xml.etree.ElementTree as ET


__version__ = version("mlx-unity2junit")


def parse_unity_output(log_file):
    test_cases = []
    total_tests = 0
    failures = 0
    default_suite_name = "EMPTY"

    with open(log_file, "r") as f:
        for line in f:
            match = re.match(r"(.+):(\d+):(.+):(\w+)", line)
            if match:
                file_path, line_number, test_name, result = match.groups()
                total_tests += 1

                # Extract filename without extension
                filename = os.path.basename(file_path).replace("utest_", "").split('.')[0].upper()
                default_suite_name = filename  # Set the default testsuite name

                # Modify the test name: replace the underscore between SWUTEST_ and the next part with a hyphen
                formatted_test_name = f"SWUTEST_{filename}-{test_name.upper()}"

                test_case = {
                    "name": formatted_test_name,
                    "classname": f"{filename}.{formatted_test_name}",
                    "file": file_path.strip(),
                    "line": line_number.strip(),
                    "result": result.strip(),
                    "suite": filename
                }
                if result.strip() != "PASS":
                    failures += 1
                test_cases.append(test_case)

    return test_cases, default_suite_name


def generate_junit_xml(test_cases, default_suite_name, output_file):
    testsuites = ET.Element("testsuites")
    timestamp = datetime.utcnow().isoformat()

    # Create a default testsuite using extracted filename
    ET.SubElement(testsuites, "testsuite", name=default_suite_name, errors="0", tests="0",
                  failures="0", skipped="0", timestamp=timestamp)

    for case in test_cases:
        testsuite = ET.SubElement(
            testsuites, "testsuite",
            name=case["classname"],
            timestamp=timestamp,
            time="0.0",
            errors="0",
            tests="1",
            failures="1" if case["result"] != "PASS" else "0",
            skipped="0"
        )

        ET.SubElement(
            testsuite, "testcase",
            name=case["name"],
            classname=case["classname"],
            time="0.0"
        )

    tree = ET.ElementTree(testsuites)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"JUnit XML report generated: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Convert Unity test output to JUnit XML.")
    parser.add_argument("log_file", help="Path to the Unity test output log file.")
    parser.add_argument("output_file", help="Path to the output JUnit XML file.")
    parser.add_argument("--version", "-v", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args()

    test_cases, default_suite_name = parse_unity_output(args.log_file)
    generate_junit_xml(test_cases, default_suite_name, args.output_file)


if __name__ == "__main__":
    main()
