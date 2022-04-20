# KeysVizu

KeysVizu is a work-in-progress open-source application that visualizes MIDI files meant to be played on a piano. Notes are shown above the corresponding keys and fall down onto the keybed.

## Getting started
The easiest way to run this project is to build the provided [docker](https://www.docker.com/) image and run the container. Simply run the following commands from the root of this repository:

```bash
docker build -t keysvizu .
docker run --rm -it --net=host --ipc=host -e DISPLAY=$DISPLAY --env="_X11_NO_MITSHM=1" -v $(pwd):/KeysVizu keysvizu
```

## Demo
A demo of what the application can generate can be found below and on the corresponding channel

<a href="http://www.youtube.com/watch?feature=player_embedded&v=vIfca9RSyOE
" target="_blank"><img src="http://img.youtube.com/vi/vIfca9RSyOE/0.jpg" 
alt="ATC - Blood Like Gasoline - KeysVizu" width="320" height="180" border="1" /></a>
