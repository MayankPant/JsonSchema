FROM python:3.9-buster

# Update package list and install necessary packages
# installing netcat for debugging and monitoring the network
# here used to check whether the postgres service  is listening in port 5432
RUN apt-get update && apt-get install -y libpq-dev netcat

# Upgrade pip
RUN pip install --upgrade pip

# Set working directory
WORKDIR /usr/src/app

# Copy and install dependencies
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy application code
COPY . .

# Copy the entrypoint script
COPY entrypoint.sh ./

# Ensure the entrypoint script is executable
RUN chmod +x entrypoint.sh
RUN chmod -R +x /usr/src/app/editor/static
RUN chmod -R +x /usr/src/app/media

# Expose port 8000
EXPOSE 8000

# Set the entrypoint to the script
ENTRYPOINT ["./entrypoint.sh"]

#  Use gunicorn to start the Django application
# CMD ["gunicorn", "--config", "gunicorn.conf.py", "JsonSchema.asgi:application"]
