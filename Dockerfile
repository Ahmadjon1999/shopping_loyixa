# Python oxirgi versiyasidan foydalanamiz
FROM python:3.11-slim

# Ishchi papkani belgilaymiz
WORKDIR /app

# Tizim uchun zarur kutubxonalar (PostgreSQL uchun libpq-dev)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Kutubxonalar ro'yxatini ko'chiramiz va o'rnatamiz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyihaning qolgan qismini ko'chiramiz
COPY . .

# Statik fayllarni yig'amiz
RUN python manage.py collectstatic --noinput

# Portni ochamiz
EXPOSE 8000

# Serverni ishga tushirish (Gunicorn orqali)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]