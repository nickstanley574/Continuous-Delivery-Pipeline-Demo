#!/bin/python

# Trivy Ignore File
#
# See: https://aquasecurity.github.io/trivy/v0.22.0/vulnerability/examples/filter/
# This file has additional format requirements to work with the trivyignore-check.py
#
# Every ignored must have 2 comments above it, the first  is the reason comments
# explaining the reason it was ignored. the send is until with a date in the
# formate YYYY-MM-DD. It recommend not to set the date more then 30 day into the future
# if you do a WARN will be displayed. The MAX future date is 90 days into the future.
# Each entry but have 1 space seprating it from the next one.
#
# For Example:
#
#   # reason No impact in our settings
#   # until: 2022-01-22
#   CVE-2018-14618
#
#   # reason: Is not used in prod app is a build dependency
#   # until: 2022-03-01
#   # CVE-1234-98765

import sys
from itertools import groupby
from datetime import datetime, timedelta
import logging


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


def check_trivyignore_entries():
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

        max_days = 35
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
        if not check_trivyignore_entries():
            sys.exit(1)
    except KeyboardInterrupt:
        logging.info("Operation interrupted by the user.")
    except Exception as e:
        logging.fatal(f"An error occurred: {e}")
