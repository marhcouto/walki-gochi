#include <iostream>
#include <chrono>
#include <string>

#include "tasks.hpp"

int average_time(std::string module_name, std::string function_name)
{
    long int sum = 0;
    std::chrono::time_point<std::chrono::high_resolution_clock> chrono_start, chrono_end;
    for (int i = 0; i < 500; i++)
    {
        chrono_start = std::chrono::high_resolution_clock::now();
        call_task(module_name, function_name);
        chrono_end = std::chrono::high_resolution_clock::now();
        sum += std::chrono::duration_cast<std::chrono::microseconds>(chrono_end - chrono_start).count();
    }
    return sum / 500;
}

int main()
{
    std::cout << "Movement task Time: " << average_time("movement", "main") << "us" << std::endl;
    std::cout << "Camera movement task Time: " << average_time("camera_movement", "main") << "us" << std::endl;
    std::cout << "Tamagotchi task Time: " << average_time("tamagotchi", "tamagotchi_task") << "us" << std::endl;
    std::cout << "Reaction task Time: " << average_time("reaction", "reaction_task") << "us" << std::endl;

    return 0;
}