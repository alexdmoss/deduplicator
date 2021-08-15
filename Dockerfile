FROM python:3.7.2-slim AS requirements
ADD main.py /app/main.py
ADD test_main.py /app/test_main.py
ADD Pipfile /app/Pipfile
ADD Pipfile.lock /app/Pipfile.lock
ADD tests/ /app/tests/
WORKDIR /app
RUN pip install pipenv=='2018.11.26'
RUN pipenv lock -r > requirements.txt
RUN pipenv lock --dev -r > requirements-dev.txt

FROM python:3.7.2-slim AS runtime-pips
COPY --from=requirements /app /app
WORKDIR /app
RUN apt-get update -y && apt-get upgrade -y && \
    pip install -r requirements.txt --no-use-pep517

FROM python:3.7.2-slim AS pytest
COPY --from=runtime-pips /app /app
COPY --from=runtime-pips /usr/local /usr/local
WORKDIR /app
RUN pip install -r requirements-dev.txt
RUN /usr/local/bin/pytest -s -v --disable-pytest-warnings --junit-xml junit-report.xml  

FROM python:3.7.2-slim
COPY --from=runtime-pips /app /app
COPY --from=runtime-pips /usr/local /usr/local
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/python", "/app/main.py"]