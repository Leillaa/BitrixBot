FROM python:3.8-slim-buster

WORKDIR /app

COPY . ./

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "main.py"]