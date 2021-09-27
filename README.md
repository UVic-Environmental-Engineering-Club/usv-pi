# UVic Environmental Engineering Club - USV-Pi

This is the software that is going to run inside the Raspberry Pi on the unmanned surface vehicle (USV).

## Setting up Docker

- To build the docker image
  - `docker build -t usv-pi .`
- To run the docker container and open the shell
  - `docker run -it --name usv-pi --rm --volume $(pwd):/usr/usv-pi --net=host usv-pi:latest sh`
  - Then in the shell use `pipenv shell` to start the python environment

## Makefile

If you are running a unix system, these commands are available to use

- `make lint`
- `make test_all`

Alternatively, use the commands

- `python3 scripts/lint.py`
- `python3 -m tests`
