# TinyCICD

# Initial Project Description

The goal is to write up a basic functional continuous application for a Flask application. The goal is to show the basic structure along with the key components and basic structures. The application it self will be very minimal, since the goal of this project is not to show case application but the pipeline around it. We will be using sqlite memory database and not worry about database migtions. Again the focus of this project is a cicd outline. 

- Build
- Style Checks
- Unit Tests
- Selenium testing
- Coverage Tests
- Security Scanning
- Load Testing
- Human Review
- Policy Check - (Code Owners)
- Integration
- Deploy

https://realpython.com/python-continuous-integration/

https://blog.inedo.com/python/pypi-package-vulnerabilities/
https://code.likeagirl.io/performance-testing-in-python-a-step-by-step-guide-with-flask-e5a56f99513d
https://itnext.io/how-to-detect-unwanted-licenses-in-your-python-project-c78ebdeb51df
> Licenses can change between versions. Filelock 3.8.2 has “The Unlicense (Unlicense)” as a license, but Filelock 3.8.1 has “Public Domain (Unlicense)”. If you have to deal with a legal department they might need to reevaluate the project if a new license appears.

- GET THE CURRENT JON CONFIG
                sh('''
                curl -O http://localhost:8080/jnlpJars/jenkins-cli.jar
                java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:password123 get-job testing > pipeline.groovy
                cat pipeline.groovy
                ''')

java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin2:admin2 reload-jcasc-configuration


- On Day Build Inspiration 



# Design Philosophy
- Nothing Local
- Security Early