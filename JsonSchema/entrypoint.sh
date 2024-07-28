#!/bin/sh

echo "Starting entrypoint script..."

# Wait for PostgreSQL to be ready
while ! nc -z postgresql 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

echo "PostgreSQL is ready. Running migrations..."

# Run database migrations
python3 manage.py makemigrations
python3 manage.py migrate

echo "Migrations complete. Starting application server..."


# Start the application server explicitly
gunicorn --config gunicorn.conf.py JsonSchema.asgi:application