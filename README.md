# Continuous Delivery Pipeline Demo

Continuous Delivery demo focusing on demonstrating different steps in a Continuous Delivery Pipeline for a very basic flask application.
 

## Initial Project Objective

The goal is to write up a functional continuous delivery pipeline for a Flask application. The goal is to show the structure along with the key components real world pipeline showcasing the variety of steps in the pipeline that various stockholders from within a company might want and the reasoning behind them.

The application it self will be very minimal, since the goal of this project is not to show case application but the pipeline around it. We will be using sqlite database and not worry about database migrations or persistence. Again the focus of this project is a CD Pipeline outline. 


## Project Design Philosophy

### Run Locally

The commands and scripts employed in the Continuous Delivery process should be capable of running locally in the same manner as they would in the CD process. This enables local debugging, reduces coupling between external tooling, and enhances process visibility and understanding. 

### Mitigation of Risk

Everything in security and compliance is not the prevention of risk, but the mitigation of risk. Similar how you can't prove their isn't a bug in your code, you can't ensure a application or process is secure. All that can be done is take steps to reasonably assume you have reasonably mitigated the risk around your application and process. 

### Highlight Unsecure Settings and Reasoning

The process should enforce the documentation and justification of changes, updates, and security Settings. Users must thoroughly document these exceptions and undergo additional reviews to ensure transparency and accountability in the decision-making process.

### Documentation Lives in the Code

Core documentation, concepts, and reasoning should be documented within the code with the use of docstrings and comments, ensuring a single source of truth. If additional information is required in the documentation, it should be referenced to the corresponding code using links.

## Continuous Delivery Overview

### Steps 

Keeping to Documentation Lives in Code - Please see [build.yaml]

### Internal Process scrit 

`trivyignore-checks.py` and `licenses-check.py` are example of what I generally call "internal process scripts". This script are independent of the application but are used for some process. Generally, I fine this script are written in the same language as the application keep the the process to a single language or some shell script, since shell script is often the glue that hold things together.  



## Todos
* Save testing logs and reports as artifacts
* Load Testings
* Setup periotic security scans of the development image
* Setup a A/B deployment demo using Heroku 
* Setup the app and testing process with a proper database
* Move the testing code to its own folder so its not in the application image. 
* Move selenium grid management logic out of the `test_selenium.py` and into it's own file.
* Move each step into a management script so the logic lives in the script that can be called locally vs having to look up the testing and build command from the `build.yaml` file.
* Add githooks to do more validation before allowing for commits and pushes to repo repo.
* add CODOWNERS to show how a process needs a review before each change.