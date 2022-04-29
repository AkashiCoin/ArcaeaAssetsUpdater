FROM python:3.9.12-slim
COPY . /app/
WORKDIR /app
RUN pip install poetry
CMD bash start.sh