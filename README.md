# Dreams Of Cloth Backend
## Running
### Docker
```
docker build -t dreams-of-cloth .
docker run --rm -it -p 8000:8000 dreams-of-cloth
```
### Local
- get python environment setup with pytorch (conda recommended)
- `pip install -r requirements.txt`
- add local address from `ifconfig` to settings.py
- run commands in entrypoint.sh
## Connecting
`cloth.gay:8000`