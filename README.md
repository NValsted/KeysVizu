# KeysVizu

## What is KeysVizu?

KeysVizu is a work-in-progress open-source application that visualizes MIDI files meant to be played on a piano. Notes are shown above the corresponding keys and fall down onto the keybed.

## Dependencies
The application is Python-based and has only been tested on Python 3.8.5 so far. Certain heavy-lifting is done in C++ where Cython is used to create Python bindings.
- Kivy 2.0.0
- mido 1.2.9
- OpenCV 4.0.1 *might migrate to ffmpeg for video export
- Cython 3.0

## Results
A demo of what the application can generate can be found below and on the corresponding channel

<a href="http://www.youtube.com/watch?feature=player_embedded&v=vIfca9RSyOE
" target="_blank"><img src="http://img.youtube.com/vi/vIfca9RSyOE/0.jpg" 
alt="ATC - Blood Like Gasoline - KeysVizu" width="320" height="180" border="1" /></a>
