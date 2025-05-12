# 2. Python 3.13-alpine 기반 이미지 (경량화, 취약점 없음)
FROM python:3.13-alpine

# 2. 필수 패키지 설치 (Playwright가 필요로 함)
RUN apt-get update && apt-get install -y \
    wget gnupg ca-certificates \
    fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 \
    libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    xdg-utils libu2f-udev libvulkan1 libxss1 --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. 코드 복사
COPY . .

# 5. Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 6. Playwright 브라우저 설치
RUN playwright install chromium

# 7. 포트 환경 변수
ENV PORT=5000

# 8. Flask 실행 명령
CMD ["python", "app.py"]
