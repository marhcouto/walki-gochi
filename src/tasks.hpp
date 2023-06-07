#ifndef TASKS_H
#define TASKS_H

#include <string>
#include <Python.h>

/**
 * @brief Calls a task from a Python module
 * 
 * @param module_name 
 * @param function_name 
 */
void call_task(std::string module_name, std::string function_name);


#endif // TASKS_H