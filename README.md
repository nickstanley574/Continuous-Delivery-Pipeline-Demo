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




Why is_environment_ready()?

When I was first developing this process at one point I noticed that my computer was starting to slow down. Running docker ps reviled I have 30+ contaiers running all from the selenium tests. This we because of a bug I had where the tearDown wasn't correctly deleting the containers. To prevent this from happening in the future I added the MAX_APP_CONTAINER value and defaulted it to 3, if more the 3 app containers where running at the same time this would indicate something isn't getting cleanup up consistently correctly. Every system and usage case is defirrent so I made this value confuvrable. I at first attempted to put a sys.exit or a raise into the tearDown to handle the original exception but TearDown ignores all exceptions (TODO Find documentation). This way if the env is in a bad state all test will abort without affecting the systems. I also added remove orphans and FORCE_GRID_RESET at this point to prevent orphan and old grids from staying arond on the host machine. 






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
