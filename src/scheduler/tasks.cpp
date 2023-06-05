#include <string>
#include <iostream>

#include "tasks.hpp"
#include "exceptions.hpp"


void call_task(std::string module_name, std::string function_name) {
  
  // Best way
  setenv("PYTHONPATH", ".", 1);
  
  PyObject *p_name, *p_module, *p_func;
  PyObject *p_args, *p_value;
  int i;

  Py_Initialize();
  // p_name = PyUnicode_DecodeFSDefault(module_name.c_str());
  p_name = PyUnicode_FromString(module_name.c_str());
  p_module = PyImport_Import(p_name);
  Py_DECREF(p_name);

  if (p_module == NULL) {
    PyErr_Print();
    throw InvalidPythonModuleException();
  }

  p_func = PyObject_GetAttrString(p_module, function_name.c_str());

  if (p_func && PyCallable_Check(p_func)) {
    p_args = PyTuple_New(0);
    p_value = PyObject_CallObject(p_func, p_args);
    Py_DECREF(p_args);
    if (p_value != NULL) {
      Py_DECREF(p_value);
    }
    else {
      Py_DECREF(p_func);
      Py_DECREF(p_module);
      PyErr_Print();
    }
  }
  else {
    if (PyErr_Occurred())
      PyErr_Print();
  }

}