# Ex#1
Client-Server solution.
Requires python 3.6+

## Usage

Step 1: `python server.py`
* Start the server on the default port 3000

Step 2: `python client.py`
* Start the client

The server is configured by default to run on host=127.0.0.1 and port=3000 and the client is configured to connect to that address.
The host and the port can be configured in both the client and the server as well as several parameters to alter the generated strings on the client

## Server usage
```
usage: server.py [-h] [-s HOST] [-p PORT]

options:
  -h, --help            show this help message and exit
  -s HOST, --host HOST  IP/Hostname to serve on
  -p PORT, --port PORT  Port to serve on
```

## Client usage
```
usage: client.py [-h] [-s HOST] [-p PORT] [-a AMOUNT] [-ln MIN_LENGTH] [-lm MAX_LENGTH] [-sn MIN_SPACES]
                 [-sm MAX_SPACES] [-c CHARS] [-f FILENAME]

Client process

options:
  -h, --help            show this help message and exit
  -s HOST, --host HOST  IP/Hostname of the server
  -p PORT, --port PORT  Port of the server
  -a AMOUNT, --amount AMOUNT
                        Amount of strings to generate
  -ln MIN_LENGTH, --min-length MIN_LENGTH
                        Minimum size of the generated strings
  -lm MAX_LENGTH, --max-length MAX_LENGTH
                        Maximum size of the generated strings
  -sn MIN_SPACES, --min-spaces MIN_SPACES
                        Minimum amount of spaces (" ") to be included in the generated strings
  -sm MAX_SPACES, --max-spaces MAX_SPACES
                        Maximum amount of spaces (" ") to be included in the generated strings
  -c CHARS, --chars CHARS
                        List of characters to pick randomly from when creating the string
  -f FILENAME, --filename FILENAME
                        Name of the file where the strings will be stored
```
