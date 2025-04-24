# Step 1: Use a base image with Python 3.11
FROM python:3.11-slim

# Step 2: Set the working directory to /app inside the container
WORKDIR /app

# Step 3: Copy the requirements.txt into the container
COPY requirements.txt .

# Step 4: Install the dependencies from the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the entire project (except files listed in .dockerignore) into the container
COPY . .

# Step 6: Expose port 8080 (required by Cloud Run)
EXPOSE 8080

# Step 7: Set the command to run your Flask app
CMD ["python", "main.py"]
