#include <exception>

class TaskQueueFullException : public std::exception {
  public: 
    const char* what() const throw() {
      return "Error: Task queue is full";
    }
};