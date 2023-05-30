
.PHONY: clear

P_LIBS = /usr/include/python2.7/


scheduler: scheduler.o tasks.o
	g++ scheduler.o tasks.o -o scheduler.exe -I ${P_LIBS} -L ${P_LIBS} -lpython3.8

scheduler.o: scheduler.cpp scheduler.hpp exceptions.hpp
	g++ -I ${P_LIBS} -c scheduler.cpp -o scheduler.o

tasks.o: tasks.cpp tasks.hpp exceptions.hpp
	g++ -I ${P_LIBS} -c tasks.cpp -o tasks.o


clean:
	rm -f *.o *.exe


