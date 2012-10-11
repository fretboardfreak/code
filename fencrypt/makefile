###
#
#  Makefile for %%%%%
#
#  Written By Curtis Sand
#
###

#Fill in the OBJECTS, EXECUTABLE, 
# and optionally the CFLAGS Lists to finish 

CC = gcc
CFLAGS = -g -O2
OBJECTS = fencrypt.o 
EXECUTABLE = fencrypt
LIBRARIES = 

$(EXECUTABLE) : $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJECTS) $(LIBRARIES) -o $(EXECUTABLE)

%.o : %.c
	$(CC) $(CFLAGS) -c $<

clean :
	rm -f $(OBJECTS) $(EXECUTABLE)
