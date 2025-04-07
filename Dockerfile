# Dockerfile
# Build: docker build -t stockinfo:latest .
# Run: docker run -d -p 8000:8000 --name stockinfo-app stockinfo:latest

# 1. 베이스 이미지 선택
FROM python:3.12-slim

# 2. 작업 디렉토리 생성
WORKDIR /app

# 3. 필요한 패키지 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 소스 코드 복사
COPY app/ app/

# 5. FastAPI + uvicorn 실행 명령
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
