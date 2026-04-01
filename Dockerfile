FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (for WeasyPrint)
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpango-1.0-0 \
#     libpangoft2-1.0-0 \
#     libcairo2 \
#     libffi-dev \
#     shared-mime-info \
#     fonts-dejavu-core \
#     && rm -rf /var/lib/apt/lists/*


RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libffi-dev \
    shared-mime-info \
    fonts-dejavu-core \
    libgdk-pixbuf-2.0-0 \
    libxml2 \
    libxslt1.1 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

# CMD ["gunicorn", "ops_system.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["sh", "-c", "python manage.py migrate && gunicorn ops_system.wsgi:application --bind 0.0.0.0:8000"]