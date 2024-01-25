FROM python:3.8
WORKDIR /code
RUN pip install --upgrade pip
COPY . .
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN pip install --no-cache-dir -r requirements.txt