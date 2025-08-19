# Dockerfile
FROM python:3.11-slim

# 최소 패키지 (with-deps가 대부분 해결해줌)
RUN apt-get update && apt-get install -y \
    wget gnupg ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# 앱 의존성
RUN pip install --no-cache-dir -r requirements.txt

# Playwright + 브라우저 + 시스템 deps 한번에
RUN pip install --no-cache-dir playwright \
 && playwright install --with-deps chromium

# 로그 버퍼링 방지 (선택)
ENV PYTHONUNBUFFERED=1

# 중요: shell form으로 PORT 치환
CMD sh -c 'gunicorn -w 2 -k gthread -b 0.0.0.0:$PORT app:app'