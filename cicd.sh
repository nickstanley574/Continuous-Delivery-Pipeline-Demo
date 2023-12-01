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
    echo ""
    echo "Running flake8..."
    echo "flake8 version: $(flake8 --version)"
    flake8 --statistics
}


run_black() {
    echo ""
    echo "Running black..."
    black --version
    black --check .
}


run_bandit() {
    echo 
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

    installed_chrome_version=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1,2,3)
    echo "Chrome Verion: $installed_chrome_version"
    driver_version=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/latest-patch-versions-per-build.json \
        | jq -r ".builds[\"$installed_chrome_version\"].version") 

    echo "Chrome Driver Version: $driver_version"

    driver_download_url="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$driver_version/linux64/chrome-linux64.zip"

    selenium_directory="../.selenium"
    echo
    rm -rf $selenium_directory/*
    mkdir -p $selenium_directory

    echo "Downloading driver: $driver_download_url"
    wget -q -P $selenium_directory $driver_download_url
    zipfile=$selenium_directory/$(basename "$driver_download_url")
    unzip -q $zipfile -d $selenium_directory

    python app.py &
    app_pid=$!

    sleep 2
    
    python -m unittest test_selenium.py
    
    kill $app_pid

    rm -rf $selenium_directory/*
}


run_security_tests() {

    run_bandit

    echo
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

    echo
    echo "=> pip-licenses"
    pip-licenses --version
    pip-licenses   
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
