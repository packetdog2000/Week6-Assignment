
# coding: utf-8

# IMPORT STATEMENT
import sys
import zmq
import time

# http://localhost:8888/notebooks/gradeclient.ipynb#
# CREATE CONTEXT
context = zmq.Context()

# CREATE SOCKETS
socket = context.socket(zmq.SUB) # For subscribing to grade changes
# socket_student = context.socket(zmq.REQ) # For getting student info

ip_addr ="10.0.0.12"
port = "5560"

# CONNECT SOCKETS
socket.connect ("tcp://%s:%s" %(ip_addr, port))
# VARIABLES
total_value = 0
count = 0
topicfilter = "Fracking"
loops = 30

## SET ARGV WHEN USED IN COMMAND LINE
sys.argv = sys.argv[1:]
if sys.argv and sys.argv[0]:
    topicfilter = str(sys.argv[0])


socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

def get_student():
    # GETS THE STUDENT INFO FROM PROT 5555
    # THIS IS A REQUEST/REPLY SERVICE
    print "\nSUBSCRIBED TO WORD: %s" %(topicfilter)
val = 0
# for update_nbr in range (loops):
course_arr = ['john doe']
print("\nListening for %s...\n" % topicfilter)
while True:
    val += 1

    # sys.stdout.write("")
    print("Ping#:%d, Current Students: %s\n" %(val,course_arr))
    string = str(socket.recv())
    print "string %s" %string


    course, fname, lname = string.split()
    name_str = " %s %s" %(fname.lower(), lname.lower())
    if any(name_str == i.lower() for i in course_arr):
        # sys.stdout.write("\r")
        sys.stdout.write("\rListening for students in course: %s , ping #%s" %(topicfilter,val))
        sys.stdout.flush()
    else:
        course_arr.append(name_str)
        sys.stdout.write("\radded %s to list" %name_str)
        sys.stdout.flush()
    time.sleep(1)

# In[ ]:
