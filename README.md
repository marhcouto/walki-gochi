# walki-gochi
Real time system to control an Alpha bot with Raspberry pi and a display, emulating a walking tamagochi with an embeded colour game. 

## Overview

The robot runs a HTTP server in the local network that allows the user to control the robot remotely and access footage of the camera. The webpage provides information on the colour the robot mascot wants to see and the one he is currently seeing. The user must direct the robot to have its camera point at an object of such colour within the time given, or else the mascot will be sad and make a long beep. If the user completes the task, the mascot will be happy and emit short beeps.

## Instructions

To run the program, first:
```sh
cd src
```

On the first shell, run the server:
```sh
cd tasks/server
python3 main_server.py
```

On the second shell, compile and run scheduler:
```sh
make
./scheduler
```

To compile and run the time measurement program:
```sh
make stats
./stats
``` 

## Authors

- [Marcelo Couto](https://github.com/marhcouto/)
- [Lucas Santos](https://github.com/lucascalvet)
- [José Ferreira](https://github.com/josepedropf) 
