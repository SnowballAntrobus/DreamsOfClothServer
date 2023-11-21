# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the relevant directory contents into the container at /app
COPY dreams_of_cloth/ /app/

# Expose the port that Django runs on
EXPOSE 8000

# Copy the custom entrypoint script into the container
COPY entrypoint.sh /app/

# Grant execute permissions to the entrypoint script
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint script as the default command
ENTRYPOINT ["/app/entrypoint.sh"]
