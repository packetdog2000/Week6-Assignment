## Submited by Edwin Garcia
## Lewis University - MS Data Science
## Distributed Computing Systems - CPSC - 55500 - 002
## Professor Manoj Bhat
## Week 6 Assignment

# coding: utf-8

# IMPORT STATEMENT
import sys
import zmq
import time

# CREATE CONTEXT
context = zmq.Context()

# CREATE SOCKETS
socket = context.socket(zmq.SUB) # For subscribing to grade changes

ip_addr ="10.0.0.12"
port = "5560"

# CONNECT SOCKETS
socket.connect ("tcp://%s:%s" %(ip_addr, port))

# VARIABLES
counter = 0
topicfilter = "Fracking" # Default filter , use command line argument to change
socket.setsockopt(zmq.SUBSCRIBE, topicfilter) # set socket option using filter

## SET ARGV WHEN USED IN COMMAND LINE
sys.argv = sys.argv[1:]
if sys.argv and sys.argv[0]:
    topicfilter = str(sys.argv[0])

# Init array with a student

course_arr = ['john doe']
print("\nListening for %s...\n" % topicfilter)

## LOOP and Listen for REQ/PUB
while True:
    counter += 1

    # sys.stdout.write("")
    print("Ping#:%d, Current Students: %s\n" %(counter,course_arr))
    string = str(socket.recv())
    print "string %s" %string


    course, fname, lname = string.split()
    name_str = " %s %s" %(fname.lower(), lname.lower())
    if any(name_str == i.lower() for i in course_arr):
        # sys.stdout.write("\r")
        sys.stdout.write("\rListening for students in course: %s , ping #%s" %(topicfilter,counter))
        sys.stdout.flush()
    else:
        course_arr.append(name_str)
        sys.stdout.write("\radded %s to list" %name_str)
        sys.stdout.flush()
    time.sleep(1)

# In[ ]:
