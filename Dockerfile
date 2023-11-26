# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Create a non-root user and switch to it
RUN addgroup -S flask && adduser -S flask -G flask

ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install "poetry==1.4.2"
ENV PATH="/home/flask/.local/bin:${PATH}"

# Set the working directory to /app
WORKDIR /home/flask/app

RUN ls -al /usr/local/bin/pip

COPY --chown=flask:flask poetry.lock pyproject.toml /home/flask/app/ 

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
# $(test "$YOUR_ENV" == production && echo "--no-dev")


COPY --chown=flask:flask app/ cicd.sh /home/flask/app/ 

USER flask

# Run app.py when the container launches
CMD ["python", "app.py"]
