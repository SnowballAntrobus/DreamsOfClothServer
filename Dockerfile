FROM nvidia/cuda:12.3.1-runtime-ubuntu22.04

# Set up python and basic utilities
RUN apt-get update && \
    apt-get install -y \
        git \
        python3-pip \
        python3-dev \
        python3 \
        libglib2.0-0 \
        wget \
        libgl1-mesa-glx \
        ffmpeg \
        libsm6 \
        libxext6

RUN python3 -m pip install --upgrade pip

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Install Pytroch and torchvision
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

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
