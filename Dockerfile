FROM mcr.microsoft.com/playwright/python:v1.54.0-jammy
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["gunicorn", "-w", "2", "-k", "gthread", "-b", "0.0.0.0:${PORT}", "app:app"]
