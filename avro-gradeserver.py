## Submited by Edwin Garcia
## Lewis University - MS Data Science
## Distributed Computing Systems - CPSC - 55500 - 002
## Professor Manoj Bhat
## Week 6 Assignment

# coding: utf-8

# GRADE SERVER  -This uses the zeroMQ publish socket and a request socket.
# the 2 ports are store in variables port and add_port. This app requests from
# matching replysocket in the AVRO app (student_write.py) using the same port number.
# This app also publishes to port variable. The subribers filters published messages.
#
#   GRADE SERVER
#   Binds PUB socket to tcp://*:5557
#   PUBLISHES RANDOM GRADES
#

import sys,os,json
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import time
import zmq
from random import randrange


# In[2]:
schema = avro.schema.parse(open("student_schema.avsc", "rb").read())

### VARIABLES
sys.argv = sys.argv[1:]

seconds = 2 # DELAY
if sys.argv and sys.argv[0]:
    seconds = float(sys.argv[0])
    print ("interval changed to %.2f " % (seconds))

ip_addr = "10.0.0.12"
port = 5560 # TCP PORT TO BIND
add_port = 5570 # PORT FOR ADDING STUDENTS
grade_range_min = 65 # MINIMUM GRADE RANGE
grade_range_max = 100 # MAXIMUM GRADE RANGE
total_students = 6 # TOTAL STUDENTS IN THE JSON ARRAY

student_arr = []

# METHODS
def get_all_students():
    print ("\nAVRO SERVER STUDENT REGISTRAR SERVICE RUNNING...")
    # msg = socket.recv() # PARAM RECEIVED
    # socket.send(msg) # PARAM SENT BACK

    ## GETS THE LIST OF STUDENTS FROM THE AVRO FILE
    ## IT FIRST READS THE AVRO FILE IF IT EXISTS,
    ## THEN, THE RECORDS ARE WRITTEN TO THE 'student_arr' ARRAY.
    ## RECORDS WITH 'Inactive' STATUS ARE FILTERED OUT FROM THE DISPLAY
    if os.path.isfile('./student_bin.avro') :
        print "\nCurrent List of Students:"
        students = DataFileReader(open("student_bin.avro", "rb"), DatumReader())
        for student in students:
            if student['student_status']=='Active':
                print "ID: %s, Name: %s, Course: %s, Grade: %d, Status: %s" %(student['student_id'],student['student_name'],student['course'], student['grade'],student['student_status'])
                student_arr.append(student)
        students.close()
        return student_arr
    else:
        return "false"


print("PUBLISHING GRADES >>>")
print("\rGenerating random grades every %.f seconds" % (seconds))


### CREATE CONTEXT, SOCKETS THEN BIND TO PORT
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" %(port))

# ADD STUDENT SOCKET
add_socket = context.socket(zmq.REQ)
add_socket.connect('tcp://%s:%s' %(ip_addr,add_port))

# In[ ]:
counter = 0
while True:
    counter += 1
    print "\ncounter : %d" %counter
    # if len(student_arr)<= 0:
    arr = get_all_students()
    latest_num = len(student_arr) - 1
    if len(student_arr) > 0:
        socket.send_string("%s %s" % (student_arr[latest_num]['course'],student_arr[latest_num]['student_name']))
        sys.stdout.write("\rPublishing PUB ID:%d: Student Name : %s,  course: %s" % (counter, student_arr[latest_num]['student_name'],student_arr[latest_num]['course']))
        sys.stdout.flush()
    else:
        print"\nStudent_arr is eq or less than zero"

    add_socket.send('listening for new student...')
    new_student = add_socket.recv()
    time.sleep(seconds)
