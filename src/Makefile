
.PHONY: clear

P_LIBS = /usr/include/python3.9/


scheduler: scheduler.o tasks.o
	g++ scheduler.o tasks.o -o scheduler -I ${P_LIBS} -L ${P_LIBS} -lpython3.9

stats: stats.o tasks.o
	g++ stats.o tasks.o -o stats -I ${P_LIBS} -L ${P_LIBS} -lpython3.9

scheduler.o: scheduler.cpp scheduler.hpp exceptions.hpp
	g++ -I ${P_LIBS} -c scheduler.cpp -o scheduler.o

tasks.o: tasks.cpp tasks.hpp exceptions.hpp
	g++ -I ${P_LIBS} -c tasks.cpp -o tasks.o

stats.o: stats.cpp
	g++ -I ${P_LIBS} -c stats.cpp -o stats.o

clean:
	rm -f *.o *.exe


