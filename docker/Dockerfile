FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-pip

COPY requirements.txt /app/requirements.txt
COPY static /static
COPY templates /templates
COPY app/core /app/core
COPY app/routes /app/routes
COPY app/schemas /app/schemas
COPY app/utils /app/utils
COPY app/main.py /app/main.py

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000
# Run the FastAPI service and background process
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000"]