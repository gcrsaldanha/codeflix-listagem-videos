FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src /app/src

CMD ["fastapi", "run", "src/api/fastapi/app.py", "--port", "8000"]
