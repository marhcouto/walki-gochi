#include <sched.h>
#include <stdio.h>
int main(int argc, char **argv)
{
  printf("Setting SCHED_FIFO and priority to %d\n",atoi(argv[1]));
  struct sched_param param;
  param.sched_priority = atoi(argv[1]);
  sched_setscheduler(0, SCHED_FIFO, &param);
  int n = 0;
  while(n < 2000000000) {
    n++;
    printf("%d\n", n);
  }
  printf("End\n");
}