FROM python:3.12.0
LABEL maintainer="memkari666@gmail.com"
WORKDIR /app

# Копируем файлы проекта
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY ./src src/
COPY .env .

# Запуск приложения
CMD ["python", "-m", "src.main"]

#docker build -t telespy-new -f Dockerfile .