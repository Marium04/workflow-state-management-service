FROM python:3.11-slim

WORKDIR /app

#Install system deps

RUN apt-get update && apt-get install -y build-essential


#Copy requirements first (for caching)

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy app

COPY . /app

ENV TESTING=0

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "reload"]