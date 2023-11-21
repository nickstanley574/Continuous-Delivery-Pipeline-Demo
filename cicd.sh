#/bin/bash

cd app

echo
echo
echo "========= Static Code Analyzer ========="
echo
# The primary goal of a static code analyzer is to find and flag programming
# errors, security vulnerabilities, and coding style issues in the codebase
# before the program is run. This analysis is performed without  actually
# executing the program, hence the term static.

echo
echo "=> flake8"
flake8 --version
flake8 --statistics

echo
echo "=> black changes"
black --check --diff .
echo

echo
echo "=> Wily"
# Wily is an application for tracking the complexity of Python code in tests
# and applications. Wily uses git to go through each revision (commit) in a
# branch and run complexity and code-analysis metrics over the code. You can
# use this to limit your code or report on trends for complexity, length etc.
# https://wily.readthedocs.io/en/latest/
wily --version
echo TODO
echo

echo 
echo "=> bandit"
# Bandit is a tool designed to find common security issues in Python code.
# To do this Bandit processes each file, builds an AST from it, and runs
# appropriate plugins against the AST nodes. Once Bandit has finished
# scanning all the files it generates a report.
# https://github.com/PyCQA/bandit/tree/main
bandit --version
bandit -r .

echo
echo
echo "========= Unit Tests ========="
echo

echo
echo "=> unittest"
python -m unittest test_app.py --verbose

echo
echo "=> coverage"
python -m coverage report

echo
echo
echo "========= Dependacy Review Scanning ========="

echo
echo "=> poetry dependecy tree"
poetry --version
poetry show --tree --no-interaction

echo
echo "=> pip-audit"
# pip-audit is a tool for scanning Python environments for packages with known
# vulnerabilities. It uses the Python Packaging Advisory Database
# https://github.com/pypa/advisory-database via the PyPI JSON API as a source
# of vulnerability reports. This project is maintained in part by Trail of
# Bits with support from Google. This is not an official Google or Trail of
# Bits product.
# https://pypi.org/project/pip-audit/
rm -f requirements.txt
poetry export --without-hashes --format=requirements.txt > requirements.txt
# cat requirements.txt
pip-audit --version
pip-audit --strict --progress-spinner off -r requirements.txt
rm -f requirements.txt


echo
echo "=> pip-licenses"
pip-licenses --version
pip-licenses


# # echo
# # echo
# echo "=> Safety"
# # https://github.com/pyupio/safety
# # safety check


echo
echo "=== Selenium ==="
echo


# python -m unittest test_selenium.py
















echo
echo "Done"