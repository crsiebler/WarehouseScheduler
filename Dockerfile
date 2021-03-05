FROM python:3.9.2-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY pyscheduler/ ./pyscheduler/
COPY tests/ ./tests/

CMD [ "python", "-m", "pyscheduler" ]