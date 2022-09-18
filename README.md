# UVic Environmental Engineering Club - USV-Pi

This is the software that is going to run inside the Raspberry Pi on the unmanned surface vehicle (USV).

[Project Structure for USV](https://github.com/UVic-Environmental-Engineering-Club/USV-Pi/wiki/Project-Structure)

## Configuring config.json

Create a file called `config.json` and fill it out with this data:

```
{
  "env": "dev",
  "port": "/dev/cu.usbserial-0001",
  "baudrate": 115200,
  "bytesize": 8,
  "timeout": 0.5,

  "mongo_url_prod": "mongodb://localhost:27017/",
  "mongo_url_dev": "mongodb+srv://uveec:<password>@cluster0.tewjo.mongodb.net/sensors",
  "mongo_dev_password": ""
}
```

**_After filling out config.json run
`git update-index --assume-unchanged config.json`_**

This prevents this file accidentally being uploaded to git with our database password!

Note: mongo prod just uses a mongo database on the pi as it serves as a backup.
The mongo dev is a link to a mongo instance running on mongodb atlas so that it doesn't need to be setup locally.

## Docker

- To build the docker image
  - `docker build -t usv-pi .`
- To run the docker container and open the shell
  - On Unix: `docker run -it --name usv-pi --rm --volume $(pwd):/usr/usv-pi --net=host usv-pi:latest sh`
  - On Windows: `docker run -it --name usv-pi --rm --volume ${pwd}:/usr/usv-pi --net=host usv-pi:latest sh`
  - Then in the shell use `pipenv shell` to start the python environment

## Running the app

_(Can be run without docker, just install pipenv `pip install pipenv`, `pipenv install`)_

1. `pipenv shell`
2. `cd usv-pi`
3. `python3 -m src`

## Makefile

If you are running a unix system, these commands are available to use

- `make lint`
- `make test_all`

Alternatively, use these commands

- `python3 scripts/lint.py`
- `python3 -m tests`

## Structure of the database

The database is using mongodb and has a main database with these collections:

```
  "accelerometer_data",
  "gyroscope_data",
  "magnetometer_data",
  "lidar_data",
  "battery_data",
  "rpm_data",
  "temperature_data",
  "wet_data",
  "gps_data",
  "gps_stats_data",
```

Each sensor gets its own collection.

## Structure of the repo

This repo is built using an main async loop started in `app.py`. It's built using subscriber/publisher model to handle in coming events.

### Coroutines

There are 4 coroutines that are started from the app:

1. driver loop
2. collision detection loop
3. serial loop
4. event loop

#### Driver loop

The driver loop is responsible for driving and follows this loop:
https://miro.com/welcomeonboard/WGdMY0VhWmpwdnhXUnVBaDQ1b2EwM0RyemdsS1cxeHMyZ3dPSVRmOVZEUWFaYnpiQkhaMXRzaE5kdU9jQWJxbnwzNDU4NzY0NTE4MjE1OTAwNzg4?share_link_id=440261643667

#### Collision detection

The driver loop can be interrupted at anytime by this collision detection when an object is detected by the LIDAR when it is X meters in front of the USV. The collision detection follows this loop:
https://miro.com/welcomeonboard/MVdTRzU4VW5QQjN1QzNUS0tSWlg2R1FoUElSdnR6eU91UmVoeDRDRnA2WXN3Z1BHMktLc1lpOTg0VjlKZVc3YXwzNDU4NzY0NTE4MjE1OTAwNzg4?share_link_id=123379736643

#### Serial loop

The serial loop constantly listens on the port that the esp32 (microcontroller) is connected to via USB. All data that is received is pushed as an event into the event loop. It is later picked up and sent to the usv-server (usvNamespace).

### Event loop

This is an infinite loop that is being poled every X ms to see if there are any events and runs the handlers if one exists.

### Subscriber/Publisher

For each event, handlers are setup and anytime that event is put into the event loop. These handlers can be found inside a folder and will the file will be `XXX_listener.py` (ex. `seria/serial_listener.py`)
