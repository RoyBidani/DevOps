CC = gcc -ansi -pedantic-errors -Wall -Wextra -g

all: final

final: foo.o foo_test.o
	@echo "Linking and producting the final application..."
	@$(CC) foo.o foo_test.o -o final 

foo.o: foo.c 
	@echo "Compiling the foo.c file..."
	@$(CC) -c foo.c 

foo_test.o: foo_test.c
	@echo "Compiling the foo_test.c file..."
	@$(CC) -c foo_test.c 

clean:
	@echo "removing object files..."
	@rm *.o final



#CC = gcc
#CFLAGS = -ansi -pedantic-errors -Wall -Wextra -g
#OBJs = foo.c foo_test.c
#TARGET = myprogram

#$(TARGET): $(OBJs)
#	@echo "Linking and producting the final application..."
#	@$(CC) $(CFLAGS) $(OBJs) -o $(TARGET)
	
