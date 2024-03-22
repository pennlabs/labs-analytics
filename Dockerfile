FROM python:3.11-buster

LABEL maintainer="Penn Labs"

# Install build dependencies
RUN apt-get update && apt-get install --no-install-recommends -y gcc libpq-dev libc-dev \
  && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install pipenv

WORKDIR /app/

# Copy project dependencies
COPY Pipfile* /app/

# Install project dependencies
RUN pipenv install --deploy --system

# Copy project files
COPY . /app/

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]