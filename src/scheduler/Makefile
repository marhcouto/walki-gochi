
.PHONY: clear

scheduler: scheduler.o
	g++ scheduler.o -o scheduler.exe

scheduler.o: scheduler.cpp
	g++ -c scheduler.cpp -o scheduler.o


clean:
	rm -f *.o *.exe


