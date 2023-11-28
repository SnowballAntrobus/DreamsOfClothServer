# Dreams Of Cloth Backend
## Running
### Docker
```
docker build -t dreams-of-cloth .
docker run --rm -it -p 8000:8000 dreams-of-cloth
```
### Local
- get python environment setup
```
    sudo apt install python3.9
    python3.9 -m venv dreams-of-cloth-env
    source dreams-of-cloth-env/bin/activate
    pip install -r requirements.txt
```
- add local address from `ifconfig` to settings.py
- run commands in entrypoint.sh
