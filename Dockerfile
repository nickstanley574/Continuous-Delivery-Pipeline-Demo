# Use an official Python runtime as a parent image
FROM python:3.12-alpine as base

# Create a non-root user and switch to it
RUN addgroup -S flask && adduser -S flask -G flask

ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install "poetry==1.4.2"
ENV PATH="/home/flask/.local/bin:${PATH}"

# Set the working directory to /app
WORKDIR /home/flask/app

COPY --chown=flask:flask poetry.lock pyproject.toml /home/flask/app/ 
COPY --chown=flask:flask app/ cicd.sh /home/flask/app/ 

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --without dev

FROM base as tester
RUN poetry install --no-interaction --no-ansi

RUN black --check --diff .

RUN coverage run -m unittest test_app --verbose

RUN bandit --version \
  && bandit -r -f txt .

RUN pip-audit --version \
  && poetry export --without-hashes --format=requirements.txt > requirements.txt \
  && pip-audit --strict --progress-spinner off -r requirements.txt

COPY --chown=flask:flask licenses-check.py approved-dependencies.csv /home/flask/app/ 

RUN python licenses-check.py 

# This is scanning all dependencies including dev. We should ensure that all dependencies
# vuaribilies are resloved and uptodate and supported.
# Ref: https://aquasecurity.github.io/trivy/v0.48/docs/advanced/container/embed-in-dockerfile/
COPY --from=aquasec/trivy:latest /usr/local/bin/trivy /usr/local/bin/trivy
RUN trivy rootfs --exit-code 1 --no-progress /

FROM base as app

ENV FLASK_HOST="0.0.0.0"

USER flask

# Run app.py when the container launches
CMD ["python", "app.py"]
