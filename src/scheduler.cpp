#include <iostream>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <sys/time.h>
#include <Python.h>

#include "exceptions.hpp"
#include "scheduler.hpp"
#include "tasks.hpp"


/**
 * @brief Construct a new Task object  
 * 
 * @param period 
 * @param delay 
 * @param exec 
 * @param func 
 */
Task::Task(int period, int delay, bool exec, void (*func)()) {
  this->period = period;
  this->delay = delay;
  this->exec = exec;
  this->func = func;
}

/**
 * @brief Construct a new default Task object  
 * 
 */
Task::Task() {
  this->period = 2;
  this->delay = 2;
  this->exec = false;
  this->func = NULL;
}

Task tasks[MAX_TASKS]; // Task queue
unsigned int curr_task = MAX_TASKS; // Current task

/**
 * @brief Handler for the timer interrupt
 * 
 * @param signum 
 */
void timer_handler(int signum) {
  if (!interrupts_enabled) return;
  interrupts_enabled = false;
  update_schedule();
  dispatch_task();
  interrupts_enabled = true;
}

/**
 * @brief Handler for keyboard interrupt
 * exits program
 * 
 * @param signum 
 */
void kill_handler(int signum) {
  std::cout << "\n\nKILLING SCHEDULER\n";
  exit(1);
}

/** 
 * @brief Initializes the scheduler
*/
void sched_init(void) {
  interrupts_enabled = false;

  struct sigaction sa_alrm, sa_int;
  struct itimerval timer;

  memset(&sa_int, 0, sizeof(sa_int));
  memset(&sa_alrm, 0, sizeof(sa_alrm));
  sa_int.sa_handler = &kill_handler;
  sa_alrm.sa_handler = &timer_handler;
  // sa_alrm.sa_flags = SA_NODEFER; // Comment line to turn off preemption
  sigaction(SIGINT, &sa_int, NULL);
  sigaction(SIGALRM, &sa_alrm, NULL);

  getitimer(ITIMER_REAL, &timer);

  timer.it_value.tv_sec = 0;
  timer.it_value.tv_usec = MICRO_CYCLE_TIME;

  timer.it_interval.tv_sec = 0;
  timer.it_interval.tv_usec = MICRO_CYCLE_TIME;

  setitimer(ITIMER_REAL, &timer, NULL);
}

/**
 * @brief Adds a task to the scheduler
 * 
 * @param period 
 * @param delay 
 * @param func 
 */
void sched_add_task(int period, int delay, void (*func)()) {
  for(int x = 0; x < MAX_TASKS; x++) {
    if (!tasks[x].func) {
      tasks[x].period = period;
      tasks[x].delay = delay;
      tasks[x].exec = false;
      tasks[x].func = func;
      return;
    }
  }
  throw TaskQueueFullException();
}

/**
 * @brief Updates the schedule of tasks with the new delays
 * 
 */
void update_schedule(void) {
  for (unsigned int i = 0; i < MAX_TASKS; i++) {
    if (!tasks[i].func) continue;
    if (tasks[i].delay) {
      tasks[i].delay--;
    } else {
      // std::cout << "Task " << i << " ready to execute" << std::endl;
      tasks[i].exec = true;
      tasks[i].delay = tasks[i].period - 1;
    }
  }
}

/**
 * @brief Dispatches the task with the highest priority
 * 
 */
void dispatch_task(void) {
  int prev_task = curr_task;
  for(int i = 0; i < curr_task; i++) {
    if(tasks[i].func && tasks[i].exec) {
      tasks[i].exec = false;
      curr_task = i;
      interrupts_enabled = true;
      tasks[i].func();
      interrupts_enabled = false;
      curr_task = prev_task;
      /* Delete task if one-shot */
      if(!tasks[i].period) tasks[i].func = NULL;
    }
  }
}

int main(int argc, char **argv) {

  sched_init();

  try {
    // Need to add tasks by increasing order of period, decreasing order of priority
    sched_add_task(1, 0, []() { call_task("tasks.movement", "main"); });
    sched_add_task(1, 0, []() { call_task("tasks.camera_movement", "main"); });
    sched_add_task(3, 0, []() { call_task("tasks.tamagotchi_state", "main"); });
    sched_add_task(3, 0, []() { call_task("tasks.tamagotchi_reaction", "main"); });
    // sched_add_task(0, 0, []() { call_task("tasks.server.main_server", "start"); }); // Server task
  } catch (TaskQueueFullException e) {
    std::cout << e.what() << std::endl;
  }

  interrupts_enabled = true;
  while(1); // Infinite loop

  return 0;

}