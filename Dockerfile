# Use the official Python base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY . .

ENV PORT 8080

# Expose the port on which the application will run
# EXPOSE from environment variable
EXPOSE $PORT

# Run the FastAPI application using uvicorn server
CMD ["fastapi", "run", "app.py", "--port", "${PORT}"]

