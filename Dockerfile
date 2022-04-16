FROM python:3.9.12-slim
COPY . /app/
WORKDIR /app
RUN pip install poetry && poetry install
EXPOSE 8080
ENTRYPOINT ["poetry","run", "python3", "/app/ArcaeaAssetsUpdater"]