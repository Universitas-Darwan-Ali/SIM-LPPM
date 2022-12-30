FROM python:3.11

# Install dependencies
RUN apt-get update && apt-get install -y libpq-dev

# Copy project files
COPY . /app
WORKDIR /app

# Install project dependencies
RUN pip install -r requirements.txt


# Expose port 8001 for Gunicorn
EXPOSE 8002

# Run Gunicorn
CMD ["gunicorn", "--bind", ":8002", "simlppm.wsgi.application"]
