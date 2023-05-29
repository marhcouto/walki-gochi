#ifndef SCHEDULER_H
#define SCHEDULER_H

#define MAX_TASKS 10
#define MICRO_CYCLE_TIME 100000


struct Task {
  int period; // in number of cycles
  int delay; // in number of cycles
  bool exec; // if the task is ready to execute
  void (*func)();

  /**
   * @brief Construct a new Task object 
   * 
   * @param period 
   * @param delay 
   * @param exec 
   * @param func 
   */
  Task(int period, int delay, bool exec, void (*func)());
  /**
   * @brief Construct a new default Task object
   * 
   * @param period 
   * @param delay 
   * @param exec 
   * @param func 
  */
  Task();
};

/**
 * @brief Handler for the timer interrupt
 * 
 * @param signum 
 */
void timer_handler(int signum);

/**
 * @brief Initializes the scheduler
 * 
 */
void sched_init(void);

/**
 * @brief Dispatches the current task
 * 
 */
void dispatch_task(void);

/**
 * @brief Updates the schedule
 * 
 */
void update_schedule(void);

/**
 * @brief Adds a task to the task queue
 * 
 * @param period 
 * @param delay 
 * @param func 
 */
void sched_add_task(int period, int delay, void (*func)());

#endif // SCHEDULER_H