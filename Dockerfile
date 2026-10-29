FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY phone_number_interpretator.py ./
COPY test_cases.py ./

CMD ["python", "-u", "phone_number_interpretator.py"]