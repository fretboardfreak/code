###
#
#  Makefile for %%%%%
#
#  Written By Curtis Sand
#
###

#Fill in the OBJECTS, EXECUTABLE,
# and optionally the CFLAGS Lists to finish

CC = g++
CFLAGS = -g -O2
OBJECTS = binary-decoder.o
EXECUTABLE = test_decoder
LIBRARIES =

$(EXECUTABLE) : $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJECTS) $(LIBRARIES) -o $(EXECUTABLE)

%.o : %.cc
	$(CC) $(CFLAGS) -c $<

clean :
	rm -f $(OBJECTS) $(EXECUTABLE)
