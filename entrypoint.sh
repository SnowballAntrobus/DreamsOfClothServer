#!/bin/bash

# Get and setup SAM model
cd image_upload_processing
git clone https://github.com/facebookresearch/segment-anything.git
cd segment-anything
pip3 install -e .
cd ../..
mkdir models
cd models
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth
cd ..

# Perform database migrations and start Django server
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000