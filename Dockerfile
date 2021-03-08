# Using this docker image with pre-compiled pandas
FROM amancevice/pandas:1.2.3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY pyscheduler/ ./pyscheduler/
COPY tests/ ./tests/

CMD [ "python", "-m", "pyscheduler" ]