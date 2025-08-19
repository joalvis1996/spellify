FROM python:3.11-slim

# 필수 패키지 설치
RUN apt-get update && \
    apt-get install -y wget gnupg \
    libnss3 libxss1 libasound2 libatk1.0-0 libatk-bridge2.0-0 \
    libgbm1 libgtk-3-0 libdrm2 libxcomposite1 libxdamage1 libxrandr2 \
    libpango-1.0-0 libharfbuzz0b libcups2 libx11-xcb1 \
    fonts-liberation fonts-unifont fonts-ubuntu \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir playwright \
 && playwright install chromium

ENV PYTHONUNBUFFERED=1

# 프로덕션용 실행
CMD sh -c 'gunicorn -w 2 -k gthread -b 0.0.0.0:$PORT app:app'
