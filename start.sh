sed -i "s/port=8080/port=${PORT}/g" /app/ArcaeaAssetsUpdater/__main__.py;
poetry install && poetry run python3 /app/ArcaeaAssetsUpdater