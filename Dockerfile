FROM python:3.11-slim-buster

WORKDIR /app

COPY ./app

# run the app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0", "--port", "8000"]

# Build the Docker image

# docker custom  image 
docker build -t shovo/my-fastapi-app .
docker run -d -p 8000:8000 shovo/my-fastapi-app
docker run -d -p 8000:8000 --name shovo/my-fastapi-container shovo/my-fastapi-app


