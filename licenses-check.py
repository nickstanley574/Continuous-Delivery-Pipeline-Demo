#!/bin/python

import subprocess
from collections import defaultdict
import csv
import sys

# This is where paranoia and legal lives.

# Lawyers are like beavers: They get in the mainstream and damn it up - John Naisbitt
# The lawyer’s truth is not Truth, but consistency or a consistent expediency. - Henry David Thoreau

# There are direct dependencies and then there are dependencies for the dependencies, layers and layers
# The question is do we trust our top level dependencies that all of its dependencies match a organization's
# licensee requirements?

# In my experience there have been time teams or loan wolf developers have developed a solution only to find out
# their solution can't be used due to license issues. Additionally, just because something might be allowed to be
# used locally doesn't mean it could be used in productions or in a development pipeline.

# Define top level dependencies in the pyproject.toml using poetry commands

# After a dependency as been approved doesn't mean it will remain approved for every. Software can change license
# this can happen at any time but generally it happens during major version release i.e. 1.x to 2.x


# If someone whats to add a new depeancy the workflow is this
# 1. add the direct dependency via poetry locally: poetry add

# Policy
# 1.

# why not just have a list of ok Lienses and move on .... Awareness everyone should be aware.

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()],
)


def run(cmd):
    """Execute a command in the system shell and capture results.

    Parameters:
    - cmd (str): The command to be executed.

    Returns:
    - CompletedProcess: A named tuple containing information about the completed process.

    Raises:
    - subprocess.CalledProcessError: If the command exits with a non-zero status.
    """
    try:
        logging.info(f"Running: {cmd}")
        return subprocess.run(cmd.split(), capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Command output: {e.output}")
        sys.exit(2)


def get_dependency_chain(dependency):
    """Retrieve the dependency chain for a given Python package using Poetry.

    This function takes a package name as input and returns a list representing
    the dependency chain, starting from the provided package and going up through
    its direct and transitive dependencies.

    Parameters:
    - dependency (str): The name of the Python package for which to retrieve the dependency chain.

    Returns:
    - list: A list containing the dependency chain, with the provided package at the beginning
      and its direct and transitive dependencies following in order.
    """
    chain = [dependency]

    # Continue querying the dependency tree until a direct dependency is found
    while True:
        pkg_line = run(f"poetry show --tree --why {dependency} --no-ansi").stdout

        # Check if the current package is a direct dependency
        if "direct dependency" in pkg_line:
            break

        # Get the first word from the first line of pkg_line, this should be the upper dependency pkg name
        dependency = pkg_line.split(" ", 1)[0]
        chain = [dependency] + chain

    return chain


def run_pip_licenses():
    """Check and compare licenses of installed Python packages with an approved list.

    Reads an '.approved-dep.csv' file containing approved packages and their licenses.
    Retrieves the current licenses of installed Python packages using 'pip-licenses'. Compares
    the current licenses with the approved licenses. Prints discrepancies and the corresponding
    dependency chains. Exits with a non-zero code if there are discrepancies.

    Note:
    - The '.approved-dep.csv' file format should be 'package_name,license' per line.
    - The 'pip-licenses' tool must be installed for the function to work.
    """

    exit_code = 0

    # Process CSV File for Approved Dependencies

    csv_file_path = ".approved-dep.csv"

    # Using defaultdict to pip_license_cmd automatically create a list for new packages
    # Each package may have multiple licenses, which is why they are stored in a list.

    approved_packages = defaultdict(list)

    # Read CSV file and populate approved_packages with package-license
    with open(csv_file_path, "r") as file:
        for pkg, license in csv.reader(file):
            approved_packages[pkg].append(license)

    # Fetching Current Python Package Licenses

    current_packages = {}

    # Retrieves the licenses of currently installed packages using 'pip-licenses'
    result = run("pip-licenses --format=csv --no-version")

    # Split the stdout of'result' into lines and use the csv.reader to create a list of packages
    current_packages_csv = list(csv.reader(result.stdout.splitlines()))

    # Iterate through the list of current packages
    for pkg, license in current_packages_csv:
        current_packages[pkg] = license

    # Print keys present in current but not in approved
    extra_keys_current = current_packages.keys() - approved_packages.keys()
    for pkg in extra_keys_current:
        logging.critical(f"{pkg} is not in {csv_file_path}")
        logging.critical(f'  └── Add to file: "{pkg}","{current_packages[pkg]}" ')
        del current_packages[pkg]
        exit_code = 2

    for pkg, license in current_packages.items():
        approved_licenses = approved_packages[pkg]
        if license not in approved_licenses:
            logging.critical(
                f"{pkg} uses {license} this differs from "
                f"approved licenses ({','.join(approved_licenses)})."
            )
            exit_code = 2
            chain = get_dependency_chain(pkg)
            logging.critical(f"  └── Dependency chain: {' -> '.join(chain)}")

    # If there is a package in approved but not in current
    missing_keys_current = approved_packages.keys() - current_packages.keys()
    for key in missing_keys_current:
        logging.info(f"{key} missing in current dependencies; {csv_file_path}.")

    return exit_code


if __name__ == "__main__":
    exitcode = 1
    logging.info(f"Starting dependency licenses check...")
    try:
        exitcode = run_pip_licenses()
    except KeyboardInterrupt:
        logging.info("Operation interrupted by the user.")
    except Exception as e:
        logging.fatal(f"An error occurred: {e}")
    logging.info("Licenses check completed.")
    sys.exit(exitcode)
