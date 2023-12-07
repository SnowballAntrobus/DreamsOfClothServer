# Dreams Of Cloth Backend
## Running
### Docker
Make sure you have docker configured with nvidia-container
```
docker build -t dreams-of-cloth .
docker run --rm -it --gpus all -p 8000:8000 dreams-of-cloth
```
### Local
- get python environment setup with pytorch (conda recommended)
- `pip install -r requirements.txt`
- add local address from `ifconfig` to env
- run commands in entrypoint.sh
## Connecting
`cloth.gay:8000`