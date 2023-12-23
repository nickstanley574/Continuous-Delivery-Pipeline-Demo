FROM python:3.12-alpine as base

ENV PIP_ROOT_USER_ACTION=ignore

RUN \
  apk update && \
  apk upgrade && \
  pip install --upgrade pip

RUN addgroup -S flask && adduser -S flask -G flask

WORKDIR /opt/app/



FROM base as builder

RUN mkdir /opt/app/database/ && chown flask:flask /opt/app/database 

RUN pip install "poetry==1.4.2"
ENV PATH="/home/flask/.local/bin:${PATH}"

COPY --chown=flask:flask poetry.lock pyproject.toml /opt/app/ 

RUN \
  poetry config virtualenvs.create false && \
  poetry install --no-root --no-interaction --no-ansi

COPY --chown=flask:flask app/ /opt/app/ 

RUN black --check --diff .

RUN coverage run -m unittest test_app --verbose

RUN bandit -r -f txt .

RUN \
  poetry export --without-hashes --format=requirements.txt > requirements.txt && \
  pip-audit --strict --progress-spinner off -r requirements.txt

COPY --chown=flask:flask licenses-check.py .approved-dep.csv  /opt/app/ 
RUN python licenses-check.py 

# Internal Pre Scan
# This is scanning all dependencies including dev. We should ensure that all dependencies
# vuaribilies are resloved and uptodate and supported.
# Ref: https://aquasecurity.github.io/trivy/v0.48/docs/advanced/container/embed-in-dockerfile/
# Ignore unfixed since if there is not fix we should not stop development.
# Once there is a fixed everything is blocked until the fix is applied.
COPY --from=aquasec/trivy:latest /usr/local/bin/trivy /usr/local/bin/trivy

COPY --chown=flask:flask trivyignore-check.py .trivyignore /opt/app/ 

RUN trivy rootfs --ignore-unfixed --exit-code 1 --timeout 3m --no-progress /

RUN python trivyignore-check.py

RUN pip wheel --wheel-dir /wheels -r requirements.txt 


FROM base as app

USER flask

ENV PATH=$PATH:/home/flask/.local/bin

ENV PYTHONUNBUFFERED=1

COPY --from=builder /wheels /wheels

RUN pip install --no-cache /wheels/*

COPY --from=builder /opt/app/ /opt/app/

RUN pip install -r requirements.txt

ENV PROD_LIKE TRUE

ENV PORT 8080

CMD ["gunicorn" , "-c", "gunicorn_config.py", "app:gunicorn_app"]
