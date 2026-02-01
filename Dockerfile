# Use a newer, supported Python version (Debian Bookworm)
FROM python:3.10-slim-bookworm

# Set the working directory inside the container
WORKDIR /app

# Update system tools and install git
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (to cache dependencies)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the bot's code
COPY . .

# Expose the port for Render
EXPOSE 8080

# The command to start the bot
CMD ["python", "bot.py"]
