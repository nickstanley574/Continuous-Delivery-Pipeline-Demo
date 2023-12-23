# TinyCICD

From a paranoia perspective 

# Initial Project Description

The goal is to write up a basic functional continuous application for a Flask application. The goal is to show the basic structure along with the key components and basic structures. The application it self will be very minimal, since the goal of this project is not to show case application but the pipeline around it. We will be using sqlite memory database and not worry about database migtions. Again the focus of this project is a cicd outline. 

- SecurityScanning 
- Load Testing
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


# Design Decisions
- Single Jenkins Agent

- Docker-in-Docker


# Benifits of approvaed_dependcies.vsv

Viability - The awarnes of knowing all of the software your application uses is very good to understand. see all the software your software uses


# Design Philosophy
- Run Locally

- Security Early

- Avoid root 

- Highlight Unsecure Settings and Reasoning

- Dependence and app should be diff images.

- The best alerts are the ones before Prod.



Why is_environment_ready()?

When I was first developing this process at one point I noticed that my computer was starting to slow down. Running docker ps reviled I have 30+ contaiers running all from the selenium tests. This we because of a bug I had where the tearDown wasn't correctly deleting the containers. To prevent this from happening in the future I added the MAX_APP_CONTAINER value and defaulted it to 3, if more the 3 app containers where running at the same time this would indicate something isn't getting cleanup up consistently correctly. Every system and usage case is defirrent so I made this value confuvrable. I at first attempted to put a sys.exit or a raise into the tearDown to handle the original exception but TearDown ignores all exceptions (TODO Find documentation). This way if the env is in a bad state all test will abort without affecting the systems. I also added remove orphans and FORCE_GRID_RESET at this point to prevent orphan and old grids from staying arond on the host machine. 


# How to scale? 
- parallelization 


# Building
    - https://github.com/NarayanAdithya/Flask-Poetry 
    - https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
    - https://github.com/hultner-technologies/unpack-python-packages/blob/main/sandbox/pyproject.toml
    - https://www.youtube.com/watch?v=DThFxooHEJk



I think every build should be a --no-cache build this will ensure every build get the latest values and will not hide issue later on and ensures the latest image updates, os updates (RUN apk updates) and security scan and run every time. For development builds I see the benefits which is why they can test locally and on their own runs, but for final integration build and test before deploy `--no-cache` is required.

Strategy that could be used to speed up build and still keep all the above benifits
    - multi Docker Images 
        - Docker Application Dependency images
        - Docker Application Image
    - Issues 
        - Complexly, overhead management
    - Benefits
        - Separation of Dependency Build times Application build times 
        - If the Dependency Base Image is build Hourly Application builds

    - I personally would only start to explore this if `--no-cache` prod builds take over 10minutes and all other avenues have been explored. 