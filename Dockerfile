FROM python:3.12.0
WORKDIR /app

# Копируем файлы проекта
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY src/ .

# Запуск приложения
CMD ["python", "main.py"]