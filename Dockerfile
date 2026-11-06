# INTENTIONALLY VULNERABLE demo target -- FOR AUTHORIZED SECURITY TESTING ONLY.
# Do not deploy this anywhere reachable. Intended to run inside an isolated sandbox.
FROM python:3.12-slim
WORKDIR /app
COPY app.py /app/app.py
EXPOSE 8000
CMD ["python", "app.py", "8000"]
