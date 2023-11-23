# Use an official Python runtime as a parent image
FROM python:3.12-alpine

RUN pip install "poetry==1.4.2"

# # Create a non-root user and switch to it
# RUN addgroup -S flask && adduser -S flask -G flask
# USER flask

# Set the working directory to /app
WORKDIR /home/flask/app

COPY pyproject.toml /home/flask/app/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

COPY app/ /home/flask/app/

# Run app.py when the container launches
CMD ["python", "app.py"]
