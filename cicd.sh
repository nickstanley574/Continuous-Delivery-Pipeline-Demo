#!/bin/sh
set -e

print_help() {
    echo "Usage: $0 {flake8|unittest|pip-licenses|all} [flake8|unittest|pip-licenses] ..."
    echo "  flake8         Run flake8 command"
    echo "  unittest       Run unittest command"
    echo "  security       Run pip-licenses command"
    echo "  all            Run all commands"
}

if [ "$#" -eq 0 ]; then
    print_help
    exit 1
fi

run_flake8() {
    echo "Running flake8..."
    echo "flake8 version: $(flake8 --version)"
    flake8 --statistics
}


run_black() {
    echo "Running black..."
    black --version
    black --check --diff  .
}


run_bandit() {
    echo "=> bandit"
    # Bandit is a tool designed to find common security issues in Python code.
    # To do this Bandit processes each file, builds an AST from it, and runs
    # appropriate plugins against the AST nodes. Once Bandit has finished
    # scanning all the files it generates a report.
    # https://github.com/PyCQA/bandit/tree/main
    bandit --version
    bandit -r -f txt .
}

run_unittest() {
    echo
    echo "Running unittest..."
    PYTHONPATH=$(pwd)/app coverage run -m unittest test_app --verbose

    echo
    echo "Coverage Report ..."
    python -m coverage report
}


run_selenium() {
    cd app/
    # python -m unittest test_selenium.SeleniumTestCase.test_task_order  --verbose
    python -m unittest test_selenium.py --verbose
}


run_security_tests() {

    run_bandit

    echo "=> pip-audit"
    # pip-audit is a tool for scanning Python environments for packages with known
    # vulnerabilities. It uses the Python Packaging Advisory Database
    # https://github.com/pypa/advisory-database via the PyPI JSON API as a source
    # of vulnerability reports. This project is maintained in part by Trail of
    # Bits with support from Google. This is not an official Google or Trail of
    # Bits product.
    # https://pypi.org/project/pip-audit/
    pip-audit --version
    rm -f requirements.txt
    poetry export --without-hashes --format=requirements.txt > requirements.txt
    pip-audit --strict --progress-spinner off -r requirements.txt
    rm -f requirements.txt

    echo "=> pip-licenses"
    pip-licenses --version
    pip-licenses   

    # docker run -v /run/user/1000/docker.sock:/var/run/docker.sock aquasec/trivy image --no-progress cicd-demo-webapp:local

    # docker run -v /run/user/1000/docker.sock:/var/run/docker.sock aquasec/trivy image --no-progress --exit-code 1 --exit-on-eol 1 cicd-demo-webapp:local
}

run_build() {
    already_installed=false
    if [ "$already_installed" = false ]; then
        docker build -t cicd-demo-webapp:local .
    fi 
}

# run_build


for cmd in "$@"; do
    case "$cmd" in
        build)
            run_build
            ;;
        flake8)
            run_flake8
            ;;
        black)
            run_black
            ;;
        unittest)
            run_unittest
            ;;
        security)
            run_security_tests
            ;;
        selenium)
            run_selenium
            ;;
        help)
            print_help
            exit 0
            ;;
        *)
            echo "Invalid option: $cmd."
            exit 1
            ;;
    esac
done

echo
echo "Done."
