# Use a lightweight Python version
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Update system tools (Install git just in case plugins need it)
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (this caches the installation step)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your bot's code
COPY . .

# Expose the port (Render/VPS needs this)
EXPOSE 8080

# The command to start your bot
CMD ["python", "bot.py"]
