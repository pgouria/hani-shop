FROM python:3.12-slim

WORKDIR /app


COPY requirements.txt .

# # install zlib dependency manually for pillow 
# RUN apt-get update && apt-get install -y \
#     zlib1g-dev \
#     libjpeg-dev \
#     libpng-dev \
#     && rm -rf /var/lib/apt/lists/*

RUN pip install --trusted-host https://mirror-pypi.runflare.com -i https://mirror-pypi.runflare.com/simple/ --upgrade pip

# Use a cache mount for pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --trusted-host https://mirror-pypi.runflare.com -i https://mirror-pypi.runflare.com/simple/ --no-cache-dir -r requirements.txt



COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
