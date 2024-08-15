# Use a base image that supports both ARM64 and AMD64
FROM --platform=$BUILDPLATFORM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8501
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "qkview.py", "--server.port=8501", "--server.address=0.0.0.0"]
