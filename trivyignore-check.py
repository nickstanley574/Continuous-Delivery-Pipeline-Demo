#!/bin/python

# trivyignore-check.py
#
# See: https://aquasecurity.github.io/trivy/v0.22.0/vulnerability/examples/filter/
# This file has additional format requirements to work with the trivyignore-check.py
#
# Every ignored vulnerability must have 2 comments above it. The first is the reason comment,
# explaining the reason it was ignored. The second is until with a date in the
# format YYYY-MM-DD.
#
# Note this script doesn't enfore the ignore themselves that is done by the trivy command, 
# this is script validating before the trivy command is run that the ignores are up-to-date
# and are still valid.
#
# For Example:
#
#   # reason: No impact in our settings
#   # until: 2022-01-22
#   CVE-2018-14618
#
#   # reason: Not used in prod app; it is a build dependency
#   # until: 2022-03-01
#   CVE-1234-98765

import sys
from itertools import groupby
from datetime import datetime
import logging
import argparse


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()],
)


def split_list(original_list, split_value):
    result, sublist = [], []

    for item in original_list:
        if item == split_value:
            if sublist:  # Avoid empty sublists if there are consecutive split values
                result.append(sublist)
                sublist = []
        else:
            sublist.append(item)

    result.append(sublist) if sublist else None
    return result


def check_trivyignore_entries(max_days):

    logging.info(f"Checking validity of '.trivyignore'")

    current_datetime = datetime.now()

    with open(".trivyignore", "r") as file:
        lines = file.readlines()

    # Using groupby from itertools to remove consecutive duplicates
    lines = [key for key, _group in groupby(lines)]

    # Splitting the list of lines into sublists based on the newline character ("\n")
    triviy_ignored_groups = split_list(lines, "\n")

    for group in triviy_ignored_groups:
        group = [string.replace("\n", "") for string in group]

        if "reason:" not in group[0]:
            logging.critical("Invalid entry: 'reason:' not found.")
            return False
        else:
            reason = group[0].split(":")[-1].strip()

        if "until:" not in group[1]:
            logging.critical(f"Invalid entry: 'until' not found for reason: {reason}.")
            return False
        else:
            until = group[1].split(":")[-1].strip()

        vuls = ",".join(group[2:])
        if vuls == "":
            logging.critical(f"Invalid entry: no vulnerability entries for {reason}.")
            return False

        # Calculate the differences in days
        until_datetime = datetime.strptime(until, "%Y-%m-%d")
        until_day = (until_datetime - current_datetime).days
        days_in_past = (current_datetime - until_datetime).days

        if until_day > max_days:
            logging.critical(f"{vuls} until date should not exceed {max_days} days.")
            return False
        elif days_in_past > 0:
            logging.critical(f"{vuls}. Ignore beyond {until}. Investigate ignores.")
            return False

        logging.info(f"Ignoring {vuls} until {until} ({until_day}d). Reason: {reason}")

    return True


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Check trivyignore entries based on the specified maximum days.")
        parser.add_argument("--max-days", type=int, help="Maximum number of days for trivyignore entries", required=True)
        args = parser.parse_args()

        if not check_trivyignore_entries(args.max_days):
            logging.critical("Invalid trivyignore entires found.")
            sys.exit(1)
        else:
            logging.info("All trivyignore entires valid.")

    except KeyboardInterrupt:
        logging.info("Operation interrupted by the user.")
    except Exception as e:
        logging.fatal(f"An error occurred: {e}")
