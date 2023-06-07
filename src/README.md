
## Instructions

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

## File Structure

- **scheduler.cpp and scheduler.hpp:** scheduler program
- **tasks.cpp and tasks.hpp:** functions to call python tasks
- **exceptions.hpp:** custom exceptions
- **stats.cpp:** program to measure execution times
- **tasks folder:** all tasks
  - **server folder:** server for streaming and remote commands
  - **movement:** infrared sensor measurement and movement of robot
  - **camera_movement:** movement of the camera
  - **tamagotchi_state:** state of the tamagotchi - colour detection
  - **tamagotchi_reaction:** beep
- **experiments folder:** scripts for preliminary experiments