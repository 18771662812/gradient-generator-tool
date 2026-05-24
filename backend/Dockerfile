FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

COPY backend/run.py .
COPY backend/app/ ./app/
COPY init.sql .

EXPOSE 5000

CMD ["python", "run.py"]
