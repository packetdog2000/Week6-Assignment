## CREATED BY : EDWIN GARCIA
## SEPTEMBER 13, 2016
## COURSE: CPSC 55500-02, DISTRIBUTED COMPUTING SYSTEMS
## LEWIS UNIVERSITY
## DEMO PROGRAM TO SIMULATE APACHE AVRO IN LINUX/CENTOS 7 AND PYTHON 2.7

import os,sys
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import json
import time
import zmq

##  ZEROMQ COMPONENTS

context = zmq.Context()
socket = context.socket(zmq.REQ)
add_socket = context.socket(zmq.REP)
socket.connect('tcp://10.0.0.12:5551')
add_socket.bind("tcp://*:5570")

#

#
# socket_list = context.socket(zmq.REQ)
# socket_list.connect('tcp://10.0.0.12:5552')


schema = avro.schema.parse(open("student_schema.avsc", "rb").read())

student_arr = []

def task_selector(task='0'):
    ## PROMPTS USER TO CHOOSE AN ACTION.
    ## ONCE AN ACTION IS SELECTED, IT CALLS THE CORRESPONDING METHOD
    print "**********\n  MENU:  \n**********"
    task = raw_input('[0] Exit\n[1] Display All Students\n[2] Create New Student\n[3] Drop Student\n\n** Select the menu number: ')
    if task=='1':
        show_students()
    elif task=='2':
        add_student()
    elif task=='3':
        drop_student()
    else:
        show_students()

def remove_student():
    ## REMOVES A RECORD BY MARKING THE 'student_status' Inactive.
    ## THIS DOES NOT DELETE RECORD BUT MARKS IT INACTIVE.
    ## THE SHOW_STUDENT_LIST FILTERS OUT INACTIVE STATUS
    print "\nRemoving a student...\n"
    _id = raw_input('Enter Student ID: ')
    dropped_student = ''
    for i in student_arr:
        if i['student_id'] ==int(_id):
            dropped_student = "%s %s " %(i['student_name'], i['course'])
            i['student_status'] = 'Inactive'

    # save back to avro
    writer = DataFileWriter(open("student_bin.avro", "wb"), DatumWriter(), schema)
    for s in student_arr:
        writer.append(s)


    writer.close()

    # SHOW TASK SELECTOR
    task_selector()


def drop_student():
    ## REMOVES A RECORD BY MARKING THE 'student_status' Inactive.
    ## THIS DOES NOT DELETE RECORD BUT MARKS IT INACTIVE.
    ## THE SHOW_STUDENT_LIST FILTERS OUT INACTIVE STATUS
    print "\nDroppping a student...\n"
    _id = raw_input('Enter Student ID: ')
    for i in student_arr:
        if i['student_id'] ==int(_id):
            i['student_status'] = 'Dropped'

    # save back to avro
    writer = DataFileWriter(open("student_bin.avro", "wb"), DatumWriter(), schema)
    for s in student_arr:
        writer.append(s)

    writer.close()

    # SHOW TASK SELECTOR
    task_selector()


def add_student():
    ## ADDS A RECORD TO THE ARRAY,
    ## THEN THE ARRAY IS LOOPED THROUGH AND AVRO FILE IS REFRESHED.
    ## INPUT PROMPTS THE USER TO ENTER FIELDS
    print "Creating a student...\n\n"
    student_name = raw_input('Enter Student Full Name: ')
    course = raw_input('Enter Course Name: ')
    student_phone = raw_input('Enter Phone Number: ')
    student_email = raw_input('Enter Email Address...')
    student_address = raw_input('Enter Mailling Address: ')
    grade = int(raw_input('Enter Grade '))

    student_id = len(student_arr) # length of array used as sequntial student id
    student_obj = {
        "student_id": student_id,
        "student_name": student_name,
        "course" : course,
        "student_phone" : student_phone,
        "student_email" : student_email,
        "student_address" : student_address,
        "grade": grade,
        "student_status": "Active"
    }
    student_arr.append(student_obj)
    add_socket.recv()
    # time.sleep(1)
    add_socket.send_string("%s" %(student_obj))



    writer = DataFileWriter(open("student_bin.avro", "wb"), DatumWriter(), schema)
    for s in student_arr:
        writer.append(s)
    writer.close()

    # socket.send_string("%s %s %s %s" %(student_id, student_name, course,grade))
    # print socket.recv()

    # SHOW TASK SELECTOR
    task_selector()


def get_all_students():
    print ("STUDENT REGISTRAR SERVICE STARTED >>>")
    # msg = socket.recv() # PARAM RECEIVED
    # socket.send(msg) # PARAM SENT BACK


    ## GETS THE LIST OF STUDENTS IN THE AVRO FILE
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



        print "End of List\n"
        # data_socket.send("true")
        # print data_socket.recv()
    else:
        print "No students found\n"


def show_students():
    ## GETS THE LIST OF STUDENTS IN THE AVRO FILE
    ## IT FIRST READS THE AVRO FILE IF IT EXISTS,
    ## THEN, THE RECORDS ARE WRITTEN TO THE 'student_arr' ARRAY.
    ## RECORDS WITH 'Inactive' STATUS ARE FILTERED OUT FROM THE DISPLAY

    if os.path.isfile('./student_bin.avro') :
        print "\nCurrent List of Students:\n"
        students = DataFileReader(open("student_bin.avro", "rb"), DatumReader())
        # socket.send_string("students") # SEND TO ZEROMQ
        for student in students:
            if student['student_status']=='Active':
                student_str = "ID: %s, Name: %s, Course: %s, Grade: %d, Status: %s" %(student['student_id'],student['student_name'],student['course'], student["grade"], student['student_status'])
                print student_str

        students.close()
        print "End of List\n"
    else:
        print "No students found\n"
    # SHOW TASK SELECTOR
    task_selector()

get_all_students()
task_selector()










## END OF PROGRAM
